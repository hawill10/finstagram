#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, url_for, flash, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import pymysql.cursors
import os
import hashlib
import datetime
import json
import base64
from werkzeug.utils import secure_filename

# For Logging on Console
import sys

SALT = 'cs3083'

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#Initialize the app from Flask
app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "some-random-secret-key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Enable CORS
CORS(app)


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='Finstagram',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def index():
    return render_template('index.html')

#Authenticates the login
@app.route('/login', methods=['POST'])
def loginAuth():
    response = {}
    request_data = request.get_json()

    #grabs information from the forms
    username = request_data.get('username')
    password = request_data.get('password') + SALT
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, hashed_password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    if (data):
        access_token = create_access_token(identity=username)
        response['username'] = username
        response['token'] = access_token
        return jsonify(response), 200
    else:
        #returns an error message to the html page
        response['errMsg'] = 'Invalid username or password'
        return jsonify(response), 401

#Authenticates the register
@app.route('/register', methods=['POST'])
def registerAuth():
    response = {}
    status = 201

    post_data = request.get_json()

    #grabs information from the forms
    username = post_data.get('username')
    password = post_data.get('password') + SALT
    fname = post_data.get('fname')
    lname = post_data.get('lname')
    bio = post_data.get('bio')

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO Person (username, password, firstName, lastName, bio) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, hashed_password, fname, lname, bio))
            conn.commit()
            cursor.close()
    except pymysql.err.IntegrityError:
        response['errMsg'] = "%s is already taken." % (username)  
        status = 400

    result = jsonify(response)
    result.status_code = status
    return result

@app.route('/feed', methods=['GET'])
@jwt_required
def home():
    response = {}
    status = 200

    user = get_jwt_identity()
    # if user logged in
    if (user):
        try:
            with conn.cursor() as cursor:
                # find all photos that can be viewed by the user
                query = """SELECT photoID, filepath, photoPoster, caption, postingdate
                        FROM Photo AS P
                        WHERE (allFollowers = True AND photoPoster IN (SELECT username_followed
                                                                        FROM Follow
                                                                        WHERE username_follower = %s AND
                                                                            username_followed = P.photoPoster AND
                                                                            followstatus = True))
                            OR
                            photoID IN (SELECT photoID
                                        FROM SharedWithWhom
                                        WHERE member_username = %s AND groupOwner = P.photoPoster AND photoID = P.photoID
                                        )
                            OR
                            photoPoster = %s
                        ORDER BY photoID DESC"""
                cursor.execute(query, (user, user, user))
                result_list = cursor.fetchall()
                
                response['data'] = result_list
        except Exception as error:
            errorMsg = error.args
            response["errMsg"] = errorMsg
            status = 400

    else:
        response["errMsg"] = "You have to login"
        status = 401
    
    result = jsonify(response)
    result.status_code = status
    return result

# show photo details
@app.route('/feed/<photo_id>', methods=['GET'])
@jwt_required
def specificPhoto_view(photo_id):
    response = {}
    status = 200

    user = get_jwt_identity()
    print(user, file=sys.stdout)

    if (user):
        # Check if the user has the permission to view the photo
        # Figure out who posted the photo
        try:
            poster = None
            permitted = 0
            with conn.cursor() as cursor:
                query = '''SELECT photoPoster
                            FROM Photo
                            WHERE photoID = %s'''
                cursor.execute(query, (photo_id))
                data = cursor.fetchone()
                poster = data['photoPoster']
            # check if the user has permission to access the photo

                query = '''SELECT count(*) AS cnt
                            FROM Photo
                            WHERE photoID = %s AND (EXISTS (SELECT *
                                                            FROM SharedWithWhom
                                                            WHERE groupOwner = %s AND
                                                            photoID = %s AND
                                                            member_username = %s)
                                                    OR
                                                    (allFollowers = True AND EXISTS(SELECT *
                                                                                    FROM Follow
                                                                                    WHERE username_followed = %s AND
                                                                                    username_follower = %s AND
                                                                                    followStatus = True)))'''
                cursor.execute(query, (photo_id, poster, photo_id, user, poster, user))
                data = cursor.fetchone()
                permitted = data['cnt']
                # if the user has permissio to access the photo, get info
                if (permitted):
                    # get photo data
                    query = '''SELECT photoPoster, firstName, lastName, caption, postingdate, filepath
                                FROM Photo JOIN Person ON (photoPoster=username)
                                WHERE photoID = %s'''
                    cursor.execute(query, (photo_id))
                    data = cursor.fetchone()
                    response["data"] = data
                    # get tagged person
                    query = '''SELECT firstName, lastName, username
                                FROM Tagged NATURAL JOIN Person
                                WHERE photoID = %s AND tagstatus = True'''
                    cursor.execute(query, (photo_id))
                    tagged = cursor.fetchall()
                    response["tagged"] = tagged

                    query = '''SELECT username, rating
                                FROM Likes
                                WHERE photoID = %s'''
                    cursor.execute(query, (photo_id))
                    rating = cursor.fetchall()
                    response["rating"] = rating

        except Exception as error:
            errorMsg = error.args
            response["errMsg"] = errorMsg
            status = 400
        

    else:
        response["errMsg"] = "You have to login"
        status = 401
    
    result = jsonify(response)
    result.status_code = status
    return result

        
@app.route('/post', methods=['POST'])
@jwt_required
def post():
    status = 200
    response = {}

    user = get_jwt_identity()

    #grabs information from the forms
    # filepath = request_data.get('filepath')
    try:
        imageUrl = request.form['imageUrl']
        imageExtension = request.form['imageExtension']
        allFollowers = request.form['allFollowers']
        caption = request.form['caption']
    except Exception as error:
        print("ERROR", file=sys.stdout)
        print(error, file=sys.stdout)

    if (user):
        try:
            # insert value into Photo
            with conn.cursor() as cursor:
                query = '''INSERT INTO Photo (postingdate, allFollowers, caption, photoPoster)
                            VALUES (NOW(), %s, %s, %s)'''
                cursor.execute(query, (allFollowers, caption, user))
                conn.commit()

                query = '''SELECT max(photoID) AS maxID FROM Photo'''
                cursor.execute(query)

                maxID = cursor.fetchone()["maxID"]
                filename = secure_filename(str(maxID) + imageExtension)
                fpath = os.path.join(UPLOAD_FOLDER, filename)

                with open(fpath, "wb") as fh:
                    fh.write(base64.decodebytes(imageUrl.encode()))
                
                query = '''UPDATE Photo SET filepath = %s WHERE photoID = %s'''
                url = url_for('uploaded_file', filename=filename)
                cursor.execute(query, (url, maxID))
                conn.commit()
                
        except Exception as error:
                errorMsg = error.args
                response["errMsg"] = errorMsg
                status = 400
    else:
        response["errMsg"] = "You have to login"
        status = 401
    
    result = jsonify(response)
    result.status_code = status
    return result

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/logout', methods=["POST"])
def logout():
    # session.pop('username')
    return jsonify({ msg: 'User Logged Out!' }), 200
        
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
