#from schemas.img_schemas import cut_change_schemas,change_img_schemas
from config.db import engine
from models.index import cut_change,change_img
from fastapi.responses import FileResponse
import os #,cv2, uuid, pixellib
#import matplotlib.pyplot as plt
from sqlalchemy import desc
from pixellib.tune_bg import alter_bg
from rembg import remove
#from random import randint
import random
import base64
import io
import PIL.Image
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import Depends, FastAPI, Header, Request, Body, File, UploadFile
import requests
import shutil
import random
import string
import json
from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from flask_cors import CORS, cross_origin

FLASKapp = Flask(__name__)
apiFLASK = Api(FLASKapp)

cors = CORS(FLASKapp)
FLASKapp.config['CORS_HEADERS'] = 'Content-Type'

IMAGEDIR = "images/"
IMAGEDIR_OUT = "images/out_put/"

#______SONPIPI______
from pickle import FALSE
from tkinter import TRUE
import mysql.connector
import smtplib
import hashlib
import requests 
import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from getpass import getpass
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

config = {
    'user': 'root',
    'password': 'S@1989',
    'host': 'localhost',
    'port': 3306,
    'database': 'fakelocation'
}
cred = firebase_admin.credentials.Certificate('fir-sigup-b773e-firebase-adminsdk-anunx-0416c5a276.json')
firebase_admin.initialize_app(cred)

@FLASKapp.route("/signup", methods=["POST"])
def signupAccount(): 
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    user_name = request.form.get('user_name')
    link_avatar = request.form.get('link_avatar')
    ip_register = request.form.get('ip_register')
    device_register = request.form.get('device_register')
    password = request.form.get('password')
    try:
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=True
        )
        send_verification_email(email)
        save_user_to_mysql(email,password,link_avatar,full_name,user_name,ip_register,device_register)
        #save_user_to_mysql(email , passsend, link_avatar,full_name,user_name,ip_register,device_register )
        return {"ketqua" : "Done Account"}
    except firebase_admin.auth.EmailAlreadyExistsError:
        print("Email Exist , Please Change Email")
        return {"ketqua" : "ERROR Email Exist"}
    except Exception as e:
        print("Lỗi: ", e)
        return {"ketqua" : "ERROR"}
    return {"ketqua" : "ERROR"}
	#	Name	Type	Collation	Attributes	Null	Default	Comments	Extra	Action
 
@FLASKapp.route("/login", methods=["POST"])
def loginAccount():
    email = request.form.get('email')
    password = request.form.get('password')
    connection= mysql.connector.connect(**config)
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT * FROM user where email= '$email' ")
    ketquaEmail = mycursor.fetchall()
    phantupro = mycursor.rowcount
    thong_tin = {}
    if phantupro == 0:
        return {"ketqua":"email not register account"}
    for i in range(0, phantupro):
        if ketquaEmail[i][7] != password:
            return  {"ketqua":"password wrong,please try again"}
        thong_tin["id_user"] = ketquaEmail[i][0]
        print(ketquaEmail[i][0])
        thong_tin["link_avatar"] = ketquaEmail[i][1]
        thong_tin["full_name"] = ketquaEmail[i][2]
        thong_tin["user_name"] = ketquaEmail[i][3]
        thong_tin["ip_register"] = ketquaEmail[i][4]
        thong_tin["check_online"] = ketquaEmail[i][5]
        thong_tin["device_register"] = ketquaEmail[i][6]
        thong_tin["password"] = ketquaEmail[i][7]
        thong_tin["email"] = ketquaEmail[i][8]
    return thong_tin
# Gửi email xác minh
def send_verification_email(email):
    #day la gmail mac dinh de gui den tat ca gmail khac va can phai bat xac thuc 2 yeu to
    from_address = "devmobilepro1888@gmail.com" 
    password = "zibzvfmidbmufdso"  

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = email
    msg['Subject'] = "Social Thinkdiff Company"
    linkverify = firebase_admin.auth.generate_email_verification_link(email, action_code_settings=None, app=None)
    body = """
    Thank You
    We appreciate your interest in connecting with us at, you can find related resources mentioned during the presentation on the session resources page.
    Devsenior Thinkdiff Company
    """ + linkverify

    msg.attach(MIMEText(body.format(email), 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, email, msg.as_string())


def save_user_to_mysql(email , passsend, link_avatar,full_name,user_name,ip_register,device_register ):
    connection= mysql.connector.connect(**config)
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT MAX(id_user) from user")
    id_user = mycursor.fetchall() + 1
    sql = f"INSERT INTO user (id_user ,link_avatar , full_name ,user_name , ip_register , device_register  , password , email ) VALUES ( {id_user} , {link_avatar}, {full_name} , {user_name} , {ip_register} , {device_register}, {passsend} , %s )"
    val = (email)
    mycursor.execute(sql, val)
    connection.commit()
    
@FLASKapp.route("/resetpass", methods=["POST"])
def  reset_password():
    username = request.form.get('username')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT email FROM user WHERE username = %s"
    values = (username,)
    
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is not None:
        email = result[0]

        new_password = "new_password"

        update_query = "UPDATE users SET password = %s WHERE username = %s"
        update_values = (new_password, username)
        cursor.execute(update_query, update_values)
        connection.commit()

        send_email(email, new_password)

        print('Đã reset mật khẩu thành công và gửi email!')
    else:
        print('Không tìm thấy người dùng có tên đăng nhập', username)

    cursor.close()
    connection.close()

def send_email(email, new_password):
    smtp_host = 'your_smtp_host'  
    smtp_port = 587  
    smtp_username = 'your_email_username' 
    smtp_password = 'your_email_password' 

    sender = 'your_email_address' 
    receiver = email

    subject = 'Reset mật khẩu'
    body = f'Mật khẩu mới của bạn là: {new_password}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        
@app.post('/upload')
async def upload_image_to_imgbb(request: Request):
    image_path = request.form.get('image_path')

    url = 'https://imgbb.com/1/upload'
    api_key = '4cd53e2de49573f195e1b8b9c8d5d035' # thay doi api_key

    with open(image_path, 'rb') as file:
        payload = {
            'key': api_key,
            'image': file.read()
        }
        response = requests.post(url, payload)
        json_data = response.json()
        
        if json_data['status'] == 200:
            image_url = json_data['data']['url']
            return image_url
        else:
            return None

def save_image_comment(image_url, noidung_comment):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    insert_query = "INSERT INTO comment_image (url, noidung_comment) VALUES (%s, %s)"
    insert_values = (image_url, noidung_comment)
    cursor.execute(insert_query, insert_values)

    connection.commit()

    cursor.close()
    connection.close()

@FLASKapp.route("/getcomment", methods=["POST"])
def get_comments():
    image_id = request.form.get('image_id')

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "SELECT * FROM fakelocation_image WHERE id_image = %s"
    values = (image_id,)
    cursor.execute(sql, values)
    results = cursor.fetchall()

    for comment in results:
        comment_id = comment[0]
        comment_text = comment[1]
        comment_date = comment[2]
        print(f"Comment ID: {comment_id}")
        print(f"Comment Text: {comment_text}")
        print(f"Comment Date: {comment_date}")
        print()
@FLASKapp.route("/get1000comments", methods=["POST"])
def get_1000comments():
    image_id = 1  
    sql = "SELECT * FROM fakelocation_image WHERE image_id = %s ORDER BY comment_date DESC LIMIT 1000"
    connection= mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(sql, (image_id,))

    results = cursor.fetchall()
    for row in results:
        comment_id = row[0]
        comment_text = row[1]
        comment_date = row[2]
    
        print(f"Comment ID: {comment_id}")
        print(f"Comment Text: {comment_text}")
        print(f"Comment Date: {comment_date}")
        print()
@FLASKapp.route("/postcomment", methods=["POST"])
def post_comments():
    connection= mysql.connector.connect(**config)
    cursor = connection.cursor()
    comment = "This is a sample comment."
    timestamp = datetime.now()
    insert_comment_query = "INSERT INTO comment_image (noidung_comment, timestamp) VALUES (%s, %s)"
    cursor.execute(insert_comment_query, (comment, timestamp))
    connection.commit()
    cursor.close()
    connection.close()
    
@FLASKapp.route("/postImange", methods=["POST"])
async def post_image(request: Request):
    connection= mysql.connector.connect(**config)
    cursor = connection.cursor()
    image_link = "https://example.com/image.jpg"
    insert_image_query = "INSERT INTO fakelocation_image (image_link) VALUES (%s)"
    cursor.execute(insert_image_query, (image_link,))
    connection.commit()
    cursor.close()
    connection.close()
# ____END_SONPIPI____


if __name__ == '__main__':
    FLASKapp.run(host='0.0.0.0', port=2989)