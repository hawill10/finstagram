#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_cors import CORS
import pymysql.cursors
import os
import hashlib
import datetime

# For Logging on Console
import sys

SALT = 'cs3083'

#Initialize the app from Flask
app = Flask(__name__)

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
@app.route('/login', methods=['GET', 'POST'])
def loginAuth():
    response = {}
    status = 200

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
    errorMsg = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        response['username'] = username
    else:
        #returns an error message to the html page
        errorMsg = 'Invalid username or password'
        status = 401
        response['errMsg'] = errorMsg

    result = jsonify(response)
    result.status_code = status
    return result

#Authenticates the register
@app.route('/register', methods=['POST'])
def registerAuth():
    response = {}
    status = 201

    post_data = request.get_json()

    print(post_data, file=sys.stdout)

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

@app.route('/feed')
def home():
    response = {}
    status = 200

    user = session['username']
    # if user logged in
    if (user):
        try:
            with conn.cursor() as cursor:
                # find all photos that can be viewed by the user
                query = """SELECT photoImage, photoPoster, caption, postingdate
                        FROM Photo AS P
                        WHERE (allFollowers = True AND photoPoster IN (SELECT username_followed
                                                                        FROM Follow
                                                                        WHERE username_follower = %s AND
                                                                            username_followed = P.photoPoster AND
                                                                            followstatus = True))
                            OR
                            photoID IN (SELECT photoID
                                        FROM SharedWithWhom
                                        WHERE member_username = %s AND owner_username = P.photoPoster AND photoID = P.photoID
                                        )
                        ORDER BY photoID DESC"""
                cursor.execute(query, (user, user))
                data = cursor.fetchall()
                response['data'] = data
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
@app.route('/feed/<photo_id>')
def specificPhoto_view(photo_id):
    response = {}
    status = 200
    user = session['username']
    if (user):
        # Check if the user has the permission to view the photo
        # Figure out who posted the photo
        try:
            poster = None
            permitted = 0
            with conn.cursor() as cursor:
                query = '''SELECT photoPoster
                            FROM Photo
                            WHERE photoID = %d'''
                cursor.execute(query, (photo_id))
                data = cursor.fetchone()
                poster= data
            # check if the user has permission to access the photo

                query = '''SELECT count(*)
                            FROM Photo
                            WHERE photoID = %d AND (EXISTS (SELECT *
                                                            FROM SharedWithWhom
                                                            WHERE groupOwner = %s AND
                                                            photo_id = %d AND
                                                            member_username = %s)
                                                    OR
                                                    (allFollowers = True AND EXISTS(SELECT *
                                                                                    FROM Follow
                                                                                    WHERE username_followed = %s AND
                                                                                    username_follower = %s AND
                                                                                    followStatus = True))'''
                cursor.execute(query, (photo_id, poster, photo_id, user, poster, user))
                data = cursor.fetchone()
                permitted = data
                # if the user has permissio to access the photo, get info
                if (permitted):
                    # get photo data
                    query = '''SELECT photoImage, photoPoster, firstName, lastName, caption, postingdate
                                FROM Photo JOIN Person ON (photoPoster=username)
                                WHERE photoID = %d'''
                    cursor.execute(query, (photo_id))
                    data = cursor.fetchone()
                    response["data"] = data
                    # get tagged person
                    query = '''SELECT firstName, lastName, username
                                FROM Tagged NATURAL JOIN Person
                                WHERE photoID = %d AND tagstatus = True'''
                    cursor.execute(query, (photo_id))
                    tagged = cursor.fetchall()
                    response["tagged"] = tagged

                    query = '''SELECT username, rating
                                FROM Likes
                                WHERE photoID = %d'''
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

        
@app.route('/post', methods=['GET', 'POST'])
def post():
    request_data = request.get_json()

    #grabs information from the forms
    username = request_data.get('username')
    filepath = request_data.get('password')

    username = session['username']
    cursor = conn.cursor()
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

# @app.route('/select_blogger')
# def select_blogger():
#     #check that user is logged in
#     #username = session['username']
#     #should throw exception if username not found
    
#     cursor = conn.cursor()
#     query = 'SELECT DISTINCT username FROM blog'
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('select_blogger.html', user_list=data)

# @app.route('/show_posts', methods=["GET", "POST"])
# def show_posts():
#     poster = request.args['poster']
#     cursor = conn.cursor()
#     query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
#     cursor.execute(query, poster)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('show_posts.html', poster_name=poster, posts=data)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
