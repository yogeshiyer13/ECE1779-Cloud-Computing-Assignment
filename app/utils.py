import hashlib, uuid
from .database import connect_to_database,  get_db, teardown_db
import os
from .ocr import text_detection
from .ocr.thumbnails import thumbnails
from datetime import timedelta
from app import webapp
from flask import session
from mysql.connector import Error
from mysql.connector import errorcode

#the login-in will be expired in 48 hours
@webapp.before_request
def make_session_permanent():
    session.permanent = True
    webapp.permanent_session_lifetime = timedelta(hours=48)

#hashfunction
def hashed_password(word, salt):
    password = hashlib.sha512(word.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return password

#save username and password to database
def save_reg(username,password):
    salt = uuid.uuid4().hex
    hashpswd = hashed_password(password, salt)

    #connect to database
    cnx = get_db()
    try:
        query = ''' INSERT INTO user (username,password,salt) VALUES (%s, %s, %s)'''
        cnx.cursor().execute(query,(username, hashpswd, salt))
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        return 'Failed to Save'

    #make a user dict
    ROOT_PATH = os.path.join(os.path.dirname(__file__),'static')
    PATH_USER = os.path.join(ROOT_PATH,username)
    os.mkdir(PATH_USER)
    PATH_USER_THUMBNAILS = os.path.join(PATH_USER, 'thumbnails')
    PATH_USER_ORIGIN = os.path.join(PATH_USER, 'origin')
    PATH_USER_OCR = os.path.join(PATH_USER, 'ocr')
    os.mkdir(PATH_USER_OCR)
    os.mkdir(PATH_USER_ORIGIN)
    os.mkdir(PATH_USER_THUMBNAILS)
    return 'Successful Registered'

def check_name(username):
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''SELECT * FROM user WHERE username = %s'''
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    return row

def check_password(username, password):
    # Create variables for easy access
    # Check if account exists using MySQL
    cnx = get_db()
    cursor = cnx.cursor()
    query = 'SELECT salt FROM user WHERE (username) = %s'
    cursor.execute(query, (username,))
    salts = cursor.fetchone()
    true_password = hashed_password(password, salts[0])

    query = 'SELECT * FROM user WHERE username = %s AND password = %s'
    cursor.execute(query, (username, true_password))
    # Fetch one record and return result
    return cursor.fetchone()


# If account exists in accounts table in out database

def save_file(username, file, filename):
    #save original file
    app_path = os.path.dirname(__file__)
    stat_path = os.path.join(app_path, 'static')
    USER_PATH = os.path.join(stat_path, username)

    ROOT_PATH = os.path.join(USER_PATH, 'origin')
    ORIGIN_PATH = os.path.join(ROOT_PATH,filename)
    file.save(ORIGIN_PATH)

    #save ocr file
    OCR_PATH = os.path.join(USER_PATH, 'ocr')
    OCR_PATH = os.path.join(OCR_PATH,filename)
    detection_img = text_detection.ap()
    detection_img.img = ORIGIN_PATH
    detection_img.path = OCR_PATH
    detection_img.rectangle_image()

    #save thumbnail file
    THUMBNAILS_PATH = os.path.join(USER_PATH, 'thumbnails')
    THUMBNAILS_PATH = os.path.join(THUMBNAILS_PATH, filename)
    thumbnails(ORIGIN_PATH, THUMBNAILS_PATH)

    # #database savefile:
    cnx = get_db()
    cursor = cnx.cursor()
    query = 'SELECT id FROM user WHERE (username) = %s'
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    user_id = int(row[0])

    try:
        query = ''' INSERT INTO images (id, imagename, origin,ocr,thumbnails) VALUES (%s,%s,%s, %s, %s)'''
        cursor.execute(query, (user_id, filename,ORIGIN_PATH,OCR_PATH,THUMBNAILS_PATH))
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        return 'Failed to Save'
    return 'Successfully Uploaded'



def validator(username, password):
    if check_name(username) is None:
        return 'Username/Password is Invalidated'
    if check_password(username,password) is None:
        return 'Username/Password is Invalidated'