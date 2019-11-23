#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_cors import CORS
import pymysql.cursors
import os
import hashlib
import datetime

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
    password = request_data.get('password')

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
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
        errorMsg = 'Invalid login or username'
        status = 401
        response['errMsg'] = errorMsg
        print(response)

    result = jsonify(response)
    result.status_code = status
    return result

#Authenticates the register
@app.route('/register', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    bio = request.form['bio']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This username already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, fname, lname, bio))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/feed', methods=['GET'])
def home():
    response = {}
    status = 200

    user = session['username']
    if (user):
        try:
            with conn.cursor() as cursor:
                query = """SELECT photoImage, photoPoster, caption, postingdate
                        FROM Photo AS P
                        WHERE (allFollowers = True AND photoPoster IN (SELECT username_followed
                                                                        FROM Follow
                                                                        WHERE username_follower = %s AND
                                                                            username_followed = P.photoPoster AND
                                                                            followstatus = True))
                            OR
                            photoID IN (SELECT photoID
                                        FROM SharedWith JOIN BelongTo ON (SharedWith.groupOwner = BelongTo.owner_username
                                                                            AND SharedWith.groupName = BelongTo.groupName)
                                        WHERE member_username = %s AND owner_username = P.photoPoster AND photoID = P.photoID
                                        )
                        ORDER BY postingdate DESC"""
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

@app.route('/feed/<photo_id>')
def specificPhoto_view(photo_id):
    status = 200
    if (user):

    else:
        response["status"] = 0
        response["errMsg"] = "You have to login"

        
# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     username = session['username']
#     cursor = conn.cursor()
#     blog = request.form['blog']
#     query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
#     cursor.execute(query, (blog, username))
#     conn.commit()
#     cursor.close()
#     return redirect(url_for('home'))

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
    home()
