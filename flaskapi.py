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
app=FastAPI()

#origins = ["*"]
#origins = ['http://localhost:3000', 'https://localhost:3000']
origins = ["*",
            "http://localhost:3000",
        "http://localhost:3002"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    mycursor.execute(f"SELECT * FROM user where email={email}")
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
@FLASKapp.route("/login", methods=["POST"])
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
    
@FLASKapp.route("/login", methods=["POST"])
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


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return  result_str

def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        # print(response.raw ,"****")
    del response
    
# get img all
@app.post('/get_img')
async def get_img(request: Request):
    con = engine.connect()
    data=con.execute(cut_change.select()).fetchall()
    con.commit()
    json_list = []
    for i in range(0,len(data)):
        json_one={}
        json_one['id']=data[i][0]
        json_one['name']=data[i][1]
        json_one['link']=data[i][2]
        json_list.append(json_one)
    return json_list

def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }
    # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", payload)
    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = json.loads(response.text)
    direct_link = json_data["data"]["url"]
    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link

#___SONPIPI___LOAD_DATA_POST
@app.post('/change_background')
async def change_background(request: Request):
    imagegoc = request.headers.get('imagegoc')
    imagebackground = request.headers.get('imagebackground')
    print(imagegoc)
    print(imagebackground)
    linkSave1 = "linkgoc_" + get_random_string(8) + ".jpg"
    linkBackground = "link_background_" +  get_random_string(8) + ".jpg"
    output_path = "ketqua_" + get_random_string(8) + ".jpg"
    print(linkSave1)
    print(linkBackground)
    download_image(imagegoc, linkSave1)
    download_image(imagebackground, linkBackground)
    change_bg = alter_bg(model_type = "pb")
    change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
    change_bg.change_bg_img(f_image_path=linkSave1  ,  b_image_path=linkBackground,     output_image_name=output_path)
    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
    direct_link = upload_image_to_imgbb(output_path, api_key)
    os.remove(linkSave1)
    os.remove(linkBackground)
    os.remove(output_path)
    return {"linkreturn" : direct_link}

# get img one to ID
@app.get('/get_img/{id}')
async def get_img(id:int):
    con = engine.connect()
    url=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchone()
    con.commit()
    with open(str(url[2]), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print((encoded_string))
        return {"id":url[0],
                        "name_img": url[1],
                        "url_img": url[2],
                        "base64":str(encoded_string)}

    
# show img input
@app.get("/img_input/{id}")
async def get_file_img_input(id:int):
    link=''
    con = engine.connect()
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchone()
    i = list(data)
    link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
    con.commit()
    img = PIL.Image.open(link)
    img.save(link)
    return FileResponse(link)


#post img to sql
@app.post('/post_img_folder/')
async def post_img(file: UploadFile = File(...)):
    contents = await file.read()
    if (str(file.filename)[-3:] == 'png') or (str(file.filename)[-3:] == 'jpg') or ((str(file.filename)[-4:] == 'jfif')) or (str(file.filename)[-4:] == 'jpeg'):
        # save file to local
        con = engine.connect()
        data=con.execute(cut_change.insert().values(img_name=file.filename, url_name=f"{IMAGEDIR}{file.filename}"))
        con.commit()

        with open(f"{IMAGEDIR}{file.filename}", "wb+") as f:
            f.write(contents)

        con = engine.connect()
        max_id = con.execute(cut_change.select().order_by(desc(cut_change.c.id))).fetchone()
        con.commit()

        return { "filename": file.filename,
                "max_id": max_id[0]
                }
    else:
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename": file.filename,
                "file":str(file.filename)[-3:]
                }


class Item(BaseModel):
    description:bytes

@app.post("/base64_img/")
async def create_item(item: Item):
    encoded_string_cut = item.description[2:-1]
    encoded_string_cut
    print()
    try :
        b64decode = base64.b64decode(encoded_string_cut)
        img = PIL.Image.open(BytesIO(b64decode))
        # img = Image.open(BytesIO(b64decode))
        out_jpg = img.convert("RGB")
        #out_jpg.show()

        # save img to local 
        a = str(encoded_string_cut[6:20])
        filename = a[6:12] + str(random.randrange(0,99))+'.jpg'
        url = f"{IMAGEDIR}{filename}"
        out_jpg.save(url)

        # save img to database
        con = engine.connect()
        data=con.execute(cut_change.insert().values(img_name=filename, url_name=url))
        con.commit()

        # get id max 
        con = engine.connect()
        max_id = con.execute(cut_change.select().order_by(desc(cut_change.c.id))).fetchone()
        con.commit()

        return {"img":" to base64 and save img done !",
                "max_id": max_id[0],
                "url": url
                }
    except:
        return {"Please try again !"
                }


# cut img and show 
@app.get("/cut_img/{id}")
async def cut_file_img(id:int):
    link=''
    con = engine.connect()
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchone()
    data = list(data)
    link = str(data[-1:]).replace("[", "").replace("]", "").replace("'", "")
    name = str(data[1:2]).replace("[", "").replace("]", "").replace("'", "")
    filename = name[-3:]
    img = PIL.Image.open(link)
    img.save(link)
    if (filename == 'png') or (filename == 'jpg') or (filename == 'fif') or (filename == 'peg'):
            output_path = IMAGEDIR_OUT + name
            with open(link, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input = i.read()
                    output = remove(input)
                    o.write(output)
                return FileResponse(output_path)
    else:
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename":filename}
    
    
# cut img and show (base64)
@app.post("/cut_img_base64/")
async def cut_file_img(item:Item):
    encoded_string_cut = item.description[2:-1]
    encoded_string_cut
    try :
        url = 'images/base64/name.png'
        b64decode = base64.b64decode(encoded_string_cut)
        img = PIL.Image.open(BytesIO(b64decode))
        # out_jpg = img.convert("RGB")
        output = remove(img)
       # cvSaveImage(url, output)
        output.save(url)
        return FileResponse(url)
    except:
        return {"Please try again !"
                }
    
# thay img
@app.put('/update_name_input/{id}')
async def update_img(id:int,file: UploadFile = File(...)):
    con = engine.connect()
    url=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchone()
    con.commit()
    os.remove(url[2])

    contents = await file.read()
    if (str(file.filename)[-3:] == 'png') or (str(file.filename)[-3:] == 'jpg') or ((str(file.filename)[-4:] == 'jfif')) or (str(file.filename)[-4:] == 'jpeg'):
        with open(f"{IMAGEDIR}{file.filename}", "wb+") as f:
            f.write(contents)
        con = engine.connect()
        data=con.execute(cut_change.update().values(img_name=file.filename, url_name=f"{IMAGEDIR}{file.filename}").where(cut_change.c.id==id))
        con.commit()
        return {
                "success": True,
                "filename": file.filename,
                "file":str(file.filename)[-3:]
            }
    else:
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename": file.filename,
                "file":str(file.filename)[-3:]
                }    

# xóa img
@app.delete('/delete_img/{id}')
async def delete_img(id:int):
    con = engine.connect()
    url=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchone()
    con.commit()
    os.remove(url[2])

    con = engine.connect()
    data=con.execute(cut_change.delete().where(cut_change.c.id==id))
    con.commit()

    return {
            "success": True,
            "msg":"Student Update Successfully"
        }


#------------------------------------------------------------------------------------------------------------------------------------------------------
#####################                BG                    ##########################


# change bg img
IMAGEDIR_BG = "images/bg/"
IMAGEDIR_OUT_BG = "images/bg/out_put/"

# post img to change
@app.post('/post_img_bg/')
async def post_img(file: UploadFile = File(...)):
    contents = await file.read()
    # save file to local
    if (str(file.filename)[-3:] == 'png') or (str(file.filename)[-3:] == 'jpg') or ((str(file.filename)[-4:] == 'jfif')) or (str(file.filename)[-4:] == 'jpeg'):
        with open(f"{IMAGEDIR_BG}{file.filename}", "wb+") as f:
            f.write(contents)

        img = PIL.Image.open(f"{IMAGEDIR_BG}{file.filename}")
        img.save(f"{IMAGEDIR_BG}{file.filename}")
        
        con = engine.connect()
        data=con.execute(change_img.insert().values(img_name=file.filename, url_name=f"{IMAGEDIR_BG}{file.filename}"))
        max_id = con.execute(change_img.select().order_by(desc(change_img.c.id))).fetchone()
        con.commit()

        with open(str(f"{IMAGEDIR_BG}{file.filename}"), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        return {"filename": file.filename,
                "max_id": max_id[0],
                "base64":encoded_string}
    else:
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename": file.filename,
                "file":str(file.filename)[-3:]
                }


@app.post("/base64_bg/")
async def create_item(item: Item):
    encoded_string_cut = item.description[2:-1]
    encoded_string_cut
    try :
        b64decode = base64.b64decode(encoded_string_cut)
        img = PIL.Image.open(BytesIO(b64decode))
        out_jpg = img.convert("RGB")
        #out_jpg.show()

        # save img to local 
        a = str(encoded_string_cut[6:20])
        filename = a[6:12] + str(random.randrange(0,99))+'.jpg'
        url = f"{IMAGEDIR_BG}{filename}"
        #out_jpg = PIL.Image.open(out_jpg)
        out_jpg.save(url)

        # save img to database
        con = engine.connect()
        data=con.execute(change_img.insert().values(img_name=filename, url_name=url))
        max_id = con.execute(change_img.select().order_by(desc(change_img.c.id))).fetchone()
        con.commit()

        return {"img":" to base64 and save img done !",
                "max_id": max_id[0],
                "url": url
                }
    except:
        return {"Please try again !"}
    
# get img bg all
@app.get('/get_img_bg')
async def get_img():
    con = engine.connect()
    data=con.execute(change_img.select()).fetchall()
    con.commit()
    json_list = []
    for i in range(0,len(data)):
        json_one={}
        json_one['id']=data[i][0]
        json_one['name']=data[i][1]
        json_one['link']=data[i][2]
        json_list.append(json_one)
    return json_list

# show img bg input return des
@app.get("/bg_input/{id}")
async def get_file_img_input(id:int):
    con = engine.connect()
    data=con.execute(change_img.select().where(change_img.c.id==id)).fetchone()
    con.commit()
    with open(str(data[2]), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return {"id":data[0],
            "name_img": data[1],
            "url_img": data[2],
            "base64": encoded_string}


# show img bg input return img
@app.get("/bg_input_img/{id}")
async def get_file_img_input(id:int):
    link=''
    con = engine.connect()
    data=con.execute(change_img.select().where(change_img.c.id==id)).fetchone()
    con.commit()
    i = list(data)
    link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
    img = PIL.Image.open(link)
    img.save(link)
    #name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "")
    return FileResponse(link)


# Thay ảnh bg
@app.put('/update_name_input_bg/{id}')
async def update_img(id:int,file: UploadFile = File(...)):
    con = engine.connect()
    url=con.execute(change_img.select().where(change_img.c.id==id)).fetchone()
    con.commit()
    os.remove(url[2])

    contents = await file.read()
    if (str(file.filename)[-3:] == 'png') or (str(file.filename)[-3:] == 'jpg') or ((str(file.filename)[-4:] == 'jfif')) or (str(file.filename)[-4:] == 'jpeg'):
        with open(f"{IMAGEDIR_BG}{file.filename}", "wb+") as f:
            f.write(contents)
        con = engine.connect()
        data=con.execute(change_img.update().values(img_name=file.filename, url_name=f"{IMAGEDIR_BG}{file.filename}").where(change_img.c.id==id))
        con.commit()
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename": file.filename,
                "file":str(file.filename)[-3:]
                }
    else:
        return {"File :": "select files only .png, .jpg, .jfif",
                "filename": file.filename,
                "file":str(file.filename)[-3:]
                }


# xóa ảnh bg
@app.delete('/delete_img_bg/{id}')
async def delete_img_bg(id:int):
    con = engine.connect()
    url=con.execute(change_img.select().where(change_img.c.id==id)).fetchone()
    con.commit()
    os.remove(url[2])

    con = engine.connect()
    data=con.execute(change_img.delete().where(change_img.c.id==id))
    con.commit()
    return {
            "success": True,
            "msg":"Student Update Successfully"
        }


#--------------------------------------------------------------------------------------------------------------------
# cut ảnh xong thay bg . file done 
@app.get("/cut_change_img/{img}/{bg}")
async def cut_change_img(img:int, bg:int):
    link=''
    path=''
    con = engine.connect()
    data=con.execute(cut_change.select().where(cut_change.c.id==img)).fetchall()
    con.commit()
    for i in data:
        i = list(i)
        link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
        name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "") #.replace(".","_")
        name_img = str(name)[-4:]
        img5 = PIL.Image.open(link)
        img5.save(link)
        if ((name_img == '.png') or (name_img == '.jpg') or (name_img == 'fifj')) or (name_img == 'jpeg'): 
            output_path = IMAGEDIR_OUT + name
            with open(link, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input = i.read()
                    output = remove(input)
                    o.write(output)
            
            con = engine.connect()
            bg_img=con.execute(change_img.select().where(change_img.c.id==bg)).fetchall()
            con.commit()
            for i in bg_img:
                i = list(i)
                link_bg = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
                name_bg = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "") #.replace(".","_")
                name_img_bg = str(name_bg)[-4:]
                img4 = PIL.Image.open(link_bg)
                img4.save(link_bg)

                if ((name_img_bg == '.png') or (name_img_bg == '.jpg') or (name_img_bg == 'fifj')) or (name_img_bg == 'jpeg'):
                    path = IMAGEDIR_OUT_BG + name_bg + '.png'
                    change_bg = alter_bg(model_type = "pb")
                    change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
                    change_bg.change_bg_img(f_image_path=output_path ,b_image_path=link_bg, output_image_name=path)
                    return FileResponse(path)
                else:
                    return {"File img bg :": "select files only .png, .jpg, .jfif"}
        else:
            return {"File img :": "select files only .png, .jpg, .jfif"}


class Item1(BaseModel):
    imgs:bytes
    bg: bytes

@app.post("/cut_change_img_base64/")
async def cut_change_img_base64(item:Item1):
    url_img = 'images/base64/img/img.png'
    url_bg = 'images/base64/img/bg.png'
    url_out = 'images/base64/img/out.png'

    img = item.imgs[2:-1]
    b64decode = base64.b64decode(img)
    img_new = Image.open(BytesIO(b64decode))
    out_img = img_new.convert("RGB")
    rm_img = remove(out_img)
    rm_img.save(url_img)

    img = item.bg[2:-1]
    b64decode = base64.b64decode(img)
    img_new = Image.open(BytesIO(b64decode))
    out_bg = img_new.convert("RGB")
    out_bg.save(url_bg)

    img1 = PIL.Image.open(url_img)
    img1.save(url_img)
    img2 = PIL.Image.open(url_bg)
    img2.save(url_bg)
    img3 = PIL.Image.open(url_out)
    img3.save(url_out)

    change_bg = alter_bg(model_type = "pb")
    change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
    change_bg.change_bg_img(f_image_path=url_img ,b_image_path=url_bg, output_image_name=url_out)

    return FileResponse(url_out)

