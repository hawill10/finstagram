#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, url_for, flash, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import pymysql.cursors
import os
import hashlib
import datetime
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
                                                                                    followStatus = True))
                                                    OR
                                                    photoPoster = %s)
                                                    '''
                cursor.execute(query, (photo_id, poster, photo_id, user, poster, user, user))
                data = cursor.fetchone()
                permitted = data['cnt']
                print(permitted, file=sys.stdout)
                # if the user has permissio to access the photo, get info
                if (permitted):
                    # get photo data
                    query = '''SELECT photoPoster, firstName, lastName, caption, postingdate, filepath, photoID
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

@app.route('/search-by-poster', methods=['POST'])
@jwt_required
def search_by_poster():
    response = {}
    status = 200

    user = get_jwt_identity()

    poster_data = request.get_json()
    poster = poster_data.get('poster')

    # if user logged in
    if (user):
        try:
            with conn.cursor() as cursor:
                # find all photos that can be viewed by the user
                query = """SELECT photoID, filepath, photoPoster, caption, postingdate
                        FROM Photo AS P
                        WHERE photoPoster = %s AND ((allFollowers = True AND photoPoster IN (SELECT username_followed
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
                            photoPoster = %s)
                        ORDER BY photoID DESC"""
                cursor.execute(query, (poster, user, user, user))
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

@app.route('/feed/<photo_id>/like', methods=['POST'])
@jwt_required
def like(photoID):
    status = 200
    response = {}

    user = get_jwt_identity()

    post_data = request.get_json()

    #grabs information from the forms
    rating = post_data.get('rating')

    if(user):
        try:
            with conn.cursor() as cursor:
                likeQuery = '''
                            INSERT INTO Likes
                            VALUES (%s, %s, NOW(), %s)
                            '''
                cursor.execute(likeQuery, (user, photoID, rating))
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

@app.route('/friendgroups', methods=['GET'])
@jwt_required
def show_friendgroups():
    response = {}
    status = 200

    user = get_jwt_identity()

    if(user):
        try:
            with conn.cursor() as cursor:
                #user is the owner
                query = '''SELECT groupName, description, groupOwner
                           FROM Friendgroup AS F
                           WHERE F.groupOwner = %s'''
                cursor.execute(query,(user))
                friendgroup = cursor.fetchall() 
                if (friendgroup):
                    for group_dict in friendgroup:
                        member_list = []
                        group = group_dict["groupName"]

                        query = '''SELECT member_username
                                FROM BelongTo as B
                                WHERE B.owner_username = %s AND B.groupName = %s'''
                        cursor.execute(query,(user,group))
                        member_dict = cursor.fetchall()
                        for member in member_dict:
                            member_list.append(member["member_username"])
                        
                        group_dict["members"] = member_list

                #user is a member
                query = '''SELECT groupName, owner_username AS groupOwner
                        FROM BelongTo AS B
                        WHERE B.member_username = %s'''
                cursor.execute(query,(user))
                membergroup = cursor.fetchall()
                updatedmembergroup = []
                for group in membergroup:
                    groupname = group["groupName"]
                    groupowner = group["groupOwner"]
                    if (groupowner != user):
                        query = '''SELECT description
                                FROM Friendgroup as F
                                WHERE F.groupName = %s AND F.groupOwner = %s'''
                        cursor.execute(query,(groupname, groupowner))
                        description_dict = cursor.fetchone()
                        group["description"] = description_dict["description"]

                        query = '''SELECT member_username
                                FROM BelongTo as B
                                WHERE B.owner_username = %s AND B.groupName = %s'''
                        cursor.execute(query,(groupowner, groupname))
                        member_dict = cursor.fetchall()

                        member_list = []
                        for i in member_dict:
                            member_list.append(i["member_username"])
                        group["members"] = member_list
                        updatedmembergroup.append(group)

                response["memberGroups"] = updatedmembergroup
                response["ownedGroups"] = friendgroup

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

@app.route('/create_friendgroup', methods=['POST'])
@jwt_required
def CreateFriendGroup():
    response = {}
    status = 200

    user = get_jwt_identity()
    name_data = request.get_json()

    groupname = name_data.get('groupName')
    description = name_data.get('description')

    if(user):
        try:
            with conn.cursor() as cursor:
                query = '''SELECT count(*) AS cnt
                           FROM Friendgroup as F
                           WHERE F.groupOwner = %s and F.groupName = %s'''
                cursor.execute(query, (user, groupname))
                data = cursor.fetchone()
                exists = data['cnt']

                if(exists):
                    response['errMsg'] = "%s is already taken." % (groupname)  
                    status = 400
                else:
                    query = "INSERT INTO Friendgroup(groupOwner, groupName, description) VALUES(%s, %s, %s)"
                    cursor.execute(query, (user, groupname, description))
                    conn.commit()
        except pymysql.err.IntegrityError:
            response['errMsg'] = "%s is already taken." % (username)  
            status = 400
    else:
        response["errMsg"] = "You have to login"
        status = 401

    result = jsonify(response)
    result.status_code = status
    return result

# @app.route('/friendgroups/<groupname>', methods=['GET'])
# @jwt_required
# def showMembers(groupname):
#     response = {}
#     status = 200

#     user = get_jwt_identity()
#     group_data = request.get_json()
#     group_code = group_data.get("group_code") #whether user is the owner(1) or the member(0)
#     owner = group_data.get("owner")

#     if(user):
#         try:
#             with conn.cursor() as cursor:
#                 if(group_code):
#                     query = '''SELECT member_username
#                                FROM BelongTo as B
#                                WHERE B.owner_username = %s AND B.groupName = %s'''
#                     cursor.execute(query,(user,groupname))
#                     members = cursor.fetchall()
#                     response["owner"] = user
#                     response["members"] = members

#                 else:
#                     query = '''SELECT member_username
#                                FROM BelongTo as B
#                                WHERE B.owner_username = %s AND B.groupName = %s'''
#                     cursor.execute(query,(owner,groupname))
#                     members = cursor.fetchall()
#                     response["owner"] = owner
#                     response["members"] = members

#         except Exception as error:
#             errorMsg = error.args
#             response["errMsg"] = errorMsg
#             status = 400

#     else:
#         response["errMsg"] = "You have to login"
#         status = 401

#     result = jsonify(response)
#     result.status_code = status
#     return result


@app.route('/addfriend', methods=['POST'])
@jwt_required
def addFriend():
    response = {}
    status = 200

    user = get_jwt_identity()
    friend_data = request.get_json()

    friendname = friend_data.get('memberName')
    groupname = friend_data.get('groupName')

    if(user):
        try:
            with conn.cursor() as cursor:
                query = '''SELECT count(*) AS cnt
                           FROM BelongTo as B
                           WHERE B.groupName = %s and B.owner_username = %s and B.member_username = %s'''
                cursor.execute(query, (groupname, user, friendname))
                data = cursor.fetchone()
                exists = data['cnt']

                if(exists):
                    response['errMsg'] = "%s is already in the group." % (friendname)  
                    status = 400
                else:
                    query = "INSERT INTO BelongTo(member_username, owner_username, groupName) VALUES(%s, %s, %s)"
                    cursor.execute(query, (friendname, user, groupname))
                    conn.commit()
        except pymysql.err.IntegrityError:
            response['errMsg'] = "%s is not a valid user." % (friendname)  
            status = 400
    else:
        response["errMsg"] = "You have to login"
        status = 401
        
    result = jsonify(response)
    result.status_code = status
    return result


@app.route('/logout', methods=["DELETE"])
def logout():
    return jsonify({ "msg": 'User Logged Out!' }), 200

@app.route('/search', methods=['POST'])
@jwt_required
def search_id():
    response = {}
    status = 200

    user = get_jwt_identity()
    request_data = request.get_json()

    key = request_data.get('username')

    if (user):
        try:
            with conn.cursor() as cursor:
                #check if the person exists
                checkID = '''SELECT *
                            FROM Person 
                            WHERE username = %s
                            '''
                cursor.execute(checkID, (key))
                searchUser = cursor.fetchall()
                if(not searchUser):
                    status = 400
                    response['errMsg'] = 'User does not exist'
                else:
                    # get if the current user is following the searched person
                    query = '''SELECT followstatus
                                FROM Follow
                                WHERE username_follower = %s AND username_followed = %s
                                '''
                    cursor.execute(query, (user, key))
                    followstatus = cursor.fetchone()
                    response["followstatus"] = followstatus

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

@app.route('/create-follow', methods=['PUT'])
@jwt_required
def addFollow():
    response = {}
    status = 201

    user = get_jwt_identity()
    put_request = request.get_json()
    username = put_request.get('username')

    if (user):
        try:
            with conn.cursor() as cursor:
                # insert Follow entity
                query = '''INSERT INTO Follow
                            VALUES (%s, %s, False)
                            '''
                cursor.execute(query, (username, user))
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

@app.route('/follow-request', methods=['GET', 'POST'])
@jwt_required
def follow_request():
    if request.method == 'GET':
        response = {}
        status = 200

        user = get_jwt_identity()
        print(user, file=sys.stdout)

        if (user):
            try:
                with conn.cursor() as cursor:
                    # insert Follow entity
                    query = '''SELECT username_follower
                                FROM Follow
                                WHERE username_followed = %s AND followstatus = False
                                '''
                    cursor.execute(query, (user))
                    follow_requests = cursor.fetchall()
                    response["follow_requests"] = follow_requests

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
    
    if request.method == 'POST':
        response = {}
        status = 200

        user = get_jwt_identity()

        post_data = request.get_json()

        #grabs information from the forms
        accept = post_data.get('accept')
        follower = post_data.get('follower')

        if (user):
            try:
                with conn.cursor() as cursor:

                    if(accept):
                        # accept follow request
                        query = '''UPDATE Follow
                                    SET followstatus = True
                                    WHERE username_followed = %s AND username_follower = %s
                                    '''
                        cursor.execute(query, (user, follower))
                        conn.commit()
                    
                    else:
                        # decline follow request
                        query = '''DELETE FROM Follow
                                    WHERE username_followed = %s AND username_follower = %s
                                    '''
                        cursor.execute(query, (user, follower))
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

@app.route('/feed/<photoID>/addTag', methods=['POST'])
@jwt_required
def addTag(photoID):
    response = {}
    status = 200

    user = get_jwt_identity()

    post_data = request.get_json()

    #grabs information from the forms
    tagged = post_data.get('tagged')

    if (user):
        try:
            with conn.cursor() as cursor:
                # if tagging oneself
                if(user == tagged):

                    query = '''INSERT INTO Tagged
                                VALUES (%s, %s, True)
                                '''
                    cursor.execute(query, (user, photoID))
                    conn.commit()
                else:
                    # check if the tagged person has permission to view the photo
                    poster = None
                    permitted = 0
                    query = '''SELECT photoPoster
                                FROM Photo
                                WHERE photoID = %s'''
                    cursor.execute(query, (photoID))
                    data = cursor.fetchone()
                    poster = data['photoPoster']

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
                    cursor.execute(query, (photoID, poster, photoID, tagged, poster, tagged))
                    data = cursor.fetchone()
                    permitted = data['cnt']
                    # if the user has permissio to access the photo, add tag
                    if (permitted):
                        insertTag = '''INSERT INTO Tagged
                                        VALUES (%s, %s, False)
                                        '''
                        cursor.execute(insertTag, (tagged, photoID))
                        conn.commit()
                    else:
                        status = 400
                        response['errMsg'] = 'This user cannot be tagged to the photo'

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

@app.route('/tag-request', methods = ['GET', 'POST'])
@jwt_required
def tag_request():
    response = {}
    status = 200

    user = get_jwt_identity()
    print(user, file=sys.stdout)

    if (user):
        if request.method == 'GET':
            # show requested tags
            try:
                with conn.cursor() as cursor:
                    requestedTagQuery = '''SELECT photoID
                                    FROM Tagged
                                    WHERE username = %s AND tagstatus = 0
                                    '''
                    cursor.execute(requestedTagQuery, (user))
                    tagRequests = cursor.fetchall()
                    response["tag_requests"] = tagRequests

            except Exception as error:
                errorMsg = error.args
                response["errMsg"] = errorMsg
                status = 400
        
        if request.method == 'POST':
            # user accepts or declines tag
            post_data = request.get_json()

            #grabs information from the forms
            accept = post_data.get('accept')
            photoID = post_data.get('photoID')

            try:
                with conn.cursor() as cursor:
                    if(accept):
                        # user accepts tag
                        acceptTag = '''
                                    UPDATE Tagged
                                    SET tagstatus = True
                                    WHERE username = %s AND photoID = %s
                                    '''
                        cursor.execute(acceptTag, (user, photoID))
                        conn.commit()
                    else:
                        # user declines tag
                        declineTag = '''DELETE FROM Tagged
                                        WHERE username = %s AND photoID = %s
                                        '''
                        cursor.execute(declineTag, (user, photoID))
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

        
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
