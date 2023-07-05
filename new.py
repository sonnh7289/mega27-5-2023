import argparse
from socket import socket

import cv2
from flask import request, jsonify
import mysql.connector
from numpy import random
from face_detection import select_face, select_all_faces
from face_swap import face_swap
from clean import randomGenData
import datetime
import time
import random
from PIL import Image
from datetime import datetime
from tqdm import tqdm
import base64
import json
import shutil
from  checkImgbb import check_imgbb_update,check_imgbb_api_key
import requests
from flask import Flask
from flask_cors import CORS
import socket
from datetime import datetime
import os
import glob

# Config database mysql
config = {
        'user': 'leooRealman',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'futureLove2'
         }      
connection = mysql.connector.connect(**config)

def get_ip_address():
    # Lấy tên máy chủ của máy tính hiện tại
    hostname = socket.gethostname()

    # Lấy địa chỉ IP tương ứng với tên máy chủ
    ip_address = socket.gethostbyname(hostname)

    return ip_address

def get_api_ip(api_url):
    try:
        ip = socket.gethostbyname(api_url)
        return ip
    except socket.gaierror:
        return None


app = Flask(__name__)
cors = CORS(app)



#get data simple
@app.route('/makedata', methods=['GET', 'POST'])
def makeSuKien():
    link_full1 = request.headers.get('Link-img1')
    link_full2 = request.headers.get('Link-img2')
    try:

        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()
            id_toan_bo_su_kien = result_id_sk[0][0] + 1
            print("id toan bo sk:  ", id_toan_bo_su_kien)
            sql = f"INSERT INTO toanbosukien ( id_toan_bo_su_kien ,phantram_loading, sukienhientai , cacsukiendachay , link_nam_goc, link_nu_goc ) VALUES ( {id_toan_bo_su_kien} , 0 , 0 , 0 , %s, %s )"
            val = (link_full1, link_full2)
            print("hallo")
            mycursor.execute(sql, val)
            result1 = mycursor.fetchall()
            connection.commit()
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"ketqua":"Failed to connect to MySQL database: " + str(error)}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return generateData(link_full1,link_full2)

def generateData(link_full1, link_full2):
    random_case = random.randint(0, 5)

    sukien_lists = [
        ['skchiatay', 'skdamcuoi', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon'],
        ['skConLapGiaDinh', 'skSinhConDauLong', 'skhanhphuc', 'skkethon', 'skToTinh', 'sklyhon'],
        ['skSinhConThuHai', 'skGapNhau', 'skhanhphuc', 'skmuasam', 'skkethon', 'sklyhon'],
        ['skGapNhau', 'skhanhphuc', 'skmuasam', 'skkethon', 'skngoaitinh', 'skvohoacchongchettruoc'],
        ['skchiatay', 'skToTinh', 'skGapNhau', 'skhanhphuc', 'skkethon', 'skngoaitinh'],
        ['skGapNhau', 'skhanhphuc', 'skvohoacchongchettruoc', 'skchaunoi', 'sklyhon', 'skmuasam']
    ]

    for i, sukien_list in enumerate(sukien_lists):
        if random_case == i:
            json = randomGenData(random_case, sukien_list, link_full1, link_full2)
            return json

@app.route('/getdata', methods=['GET', 'POST'])
def createdata():
    link_full1 = request.headers.get('Link-img1')
    link_full2 = request.headers.get('Link-img2')
    return generateData(link_full1,link_full2)
    

# tim theo id Love
@app.route('/lovehistory/<string:idlove>', methods=['GET'])
def getDataLoveHistory(idlove):

    thong_tin = {}
    list_thong_tin = []
    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idlove}")
        result2 = mycursor.fetchall()
        print(result2)
        phantupro = mycursor.rowcount
        index_get_data = 0
        for i in range(0, phantupro):
            thong_tin["id"] = result2[i][0]
            thong_tin["link_nam_goc"] = result2[i][1]
            thong_tin["link_nu_goc"] = result2[i][2]
            thong_tin["link_nam_chua_swap"] = result2[i][3]
            thong_tin["link_nu_chua_swap"] = result2[i][4]
            thong_tin["link_da_swap"] = result2[i][5]
            thong_tin["real_time"] = result2[i][6]
            thong_tin["ten_su_kien"] = result2[i][7]
            thong_tin["noi_dung_su_kien"] = result2[i][8]
            thong_tin["so_thu_tu_su_kien"] = result2[i][10]
            list_thong_tin.append(thong_tin)
            thong_tin = {}
            # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thong_tin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_thong_tin

# create comment
@app.route('/lovehistory/comment', methods=['GET', 'POST'])
def createcomment():
    print(request.form.get('noi_dung_cmt'))
    noi_dung = request.form.get('noi_dung_cmt')
    device_cmt = request.form.get('device_cmt') 
    id_toan_bo_su_kien = request.form.get('id_toan_bo_su_kien') 
    print("id tbsk ne: ", id_toan_bo_su_kien)
    ipComment =  request.form.get('ipComment')  
    imageattach = request.form.get('imageattach')  

    thong_tin={}

    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT MAX(id_Comment) from comment")
        result_id_sk = mycursor.fetchall()
        idNext = result_id_sk[0][0]+1
        mycursor.execute(f"SELECT * FROM saved_sukien where id_toan_bo_su_kien={id_toan_bo_su_kien}")

        result_comment = mycursor.fetchall()

        thong_tin["link_da_swap"] = result_comment[0][5]
        thong_tin["toan_bo_su_kien"]=result_comment[0][9]
        thong_tin["so_thu_tu_su_kien"] = result_comment[0][10]
        ts = time.time()
        datetimenow = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        lenhquery = f"INSERT INTO comment(id_Comment,noi_dung_Comment,IP_Comment,device_Comment,id_toan_bo_su_kien,imageattach, thoi_gian_release) VALUES ( {idNext} ,%s,%s,%s, {id_toan_bo_su_kien} ,%s , %s )"
        print(lenhquery)
        val = (noi_dung ,ipComment , device_cmt,imageattach,datetimenow)
        mycursor.execute(lenhquery, val)
        result1 = mycursor.fetchall()
        connection.commit()
        # luu cac thay doi vao trong database
        thong_tin["id_Comment"]=idNext
        thong_tin["noi_dung_cmt"]= noi_dung
        thong_tin["device_cmt"]=device_cmt
        thong_tin["ip_comment"]=ipComment
        thong_tin["imageattach"]=imageattach
        thong_tin["id_toan_bo_su_kien"]=id_toan_bo_su_kien
        #thong_tin["thoi_gian_release"]= datetimenow.strftime('%Y-%m-%d %H:%M:%S')
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"error":f"Failed to connect to MySQL database: {error}"}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return thong_tin
        
# create page for event history
@app.route('/lovehistory/page/<int:trang>', methods=['GET'])
def getPageLoveHistory(trang):
    list_toan_bo_sukien_saved = []

    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
        PhanTuMax = mycursor.fetchall()
        soPhanTu = PhanTuMax[0][0]  + 1 
        if trang * 25 > soPhanTu:
            return {"messages" : "vuot qua so phan tu"}
        if trang < 1:
            return {"messages" : "page start from 1"}
        for idItemPhanTu in reversed(range(soPhanTu - ((trang - 1) * 25) - 25, soPhanTu - ((trang - 1) * 25))):
            Mot_LanQuerryData = []
            print("item phan tu " + str(idItemPhanTu))
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idItemPhanTu}")
            saved_sukien = mycursor.fetchall()
            print(saved_sukien)
            thong_tin = {}
            soPhanTu1List= len(mycursor.fetchall())
            phantupro = mycursor.rowcount
            print(phantupro)
            for i in range(0, phantupro):
                thong_tin["id"] = saved_sukien[i][0]
                print(saved_sukien[i][0])
                print("sao ko vao")
                thong_tin["link_nam_goc"] = saved_sukien[i][1]
                thong_tin["link_nu_goc"] = saved_sukien[i][2]
                thong_tin["link_nam_chua_swap"] = saved_sukien[i][3]
                thong_tin["link_nu_chua_swap"] = saved_sukien[i][4]
                thong_tin["link_da_swap"] = saved_sukien[i][5]
                thong_tin["real_time"] = saved_sukien[i][6]
                thong_tin["ten_su_kien"] = saved_sukien[i][7]
                thong_tin["noi_dung_su_kien"] = saved_sukien[i][8]
                thong_tin["id_toan_bo_su_kien"] = saved_sukien[i][9]
                thong_tin["so_thu_tu_su_kien"] = saved_sukien[i][10]
                
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}
            list_toan_bo_sukien_saved.append(Mot_LanQuerryData)
            # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thong_tin from skhanhphuc")x
        # connection.commit()
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_toan_bo_sukien_saved

# create page for comment history
@app.route('/lovehistory/pageComment/<int:trang>', methods=['GET'])
def getPageCommentHistory(trang):
    thong_tin = {}
    list_thong_tin = []

    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_Comment) from comment")
        result_id_sk = mycursor.fetchall()
        tongsophantu = result_id_sk[0][0]
        print("tong so phan tu: ", tongsophantu)

        tongsotrang = tongsophantu / 50 
        print("tongsophantusau: ", tongsophantu)
        if trang < 1:
            return {"messages" : "page start from 1"} #113 - 50
        phantunguoc = (trang-1) *50 
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT * FROM comment ORDER BY id_Comment DESC LIMIT { phantunguoc } ,50 ")
        result2 = mycursor.fetchall()
        print("kq2" ,result2)
        sophantu = mycursor.rowcount
        for i in range(0, sophantu):
            thong_tin["id_toan_bo_su_kien"] = result2[i][4]
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = result2[i][0]
            thong_tin["imageattach"]= result2[i][5] 
            thong_tin["thoi_gian_release"]= result2[i][6] 
            
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={result2[i][4]}")
            saved_sukien = mycursor.fetchall()
            thong_tin["link_nam_goc"] = saved_sukien[0][1]
            thong_tin["link_nu_goc"] = saved_sukien[0][2]
            list_thong_tin.append(thong_tin)
            thong_tin = {}
            #print(datetime.datetime.utcnow())
        

        # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thong_tin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    
    return {"comment":list_thong_tin,
            "sophantu" : tongsophantu,
            "sotrang": tongsotrang}

@app.route("/lovehistory/comment/<int:id_toan_bo_su_kien>")
def getCommentHistory(id_toan_bo_su_kien):

    thong_tin = {}
    list_thong_tin = []

    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * FROM comment where id_toan_bo_su_kien={id_toan_bo_su_kien}")
        result2 = mycursor.fetchall()
        mycursor.execute(f"SELECT COUNT(*) FROM comment where id_toan_bo_su_kien={id_toan_bo_su_kien}")
        result_toan_bo_su_kien = mycursor.fetchall()
        print(result_toan_bo_su_kien[0][0])
        for i in range(0 , result_toan_bo_su_kien[0][0]):
            thong_tin["id_toan_bo_su_kien"] = result2[i][4]
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = result2[i][0]
            thong_tin["imageattach"]= result2[i][5] 
            thong_tin["thoi_gian_release"] = result2[i][6]
            list_thong_tin.append(thong_tin)
            thong_tin = {}
        # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thong_tin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_thong_tin

@app.route("/lovehistory/add/<int:id_toan_bo_su_kien>" , methods=['GET', 'POST'])
def addThemSuKienTinhYeu(id_toan_bo_su_kien):
    thong_tin = {}
    print(request.form.get('noidung_su_kien'))
    noidung_su_kien = request.form.get('noidung_su_kien')
    so_thu_tu_su_kien = request.form.get('so_thu_tu_su_kien') 
    device_them_su_kien = request.form.get('device_them_su_kien') 
    ip_them_su_kien =  request.form.get('ip_them_su_kien')  
    link_da_swap = request.form.get('link_da_swap')  
    thoigian_sukien = request.form.get('thoigian_sukien')
    ten_su_kien = request.form.get('ten_su_kien')    

    try:
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
        max_sql_id_saved = mycursor.fetchall()
        id_saved_max = max_sql_id_saved[0][0] + 1
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        sql = f"INSERT INTO saved_sukien (id_saved , link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , ip_them_su_kien, device_them_su_kien, thoigian_sukien, id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {id_saved_max}  ,%s  , %s  ,%s,%s, %s, %s,%s, { id_toan_bo_su_kien },{so_thu_tu_su_kien})"
        val = (link_da_swap, date, ten_su_kien,noidung_su_kien,ip_them_su_kien , device_them_su_kien,thoigian_sukien)
        mycursor.execute(sql, val)
        result1 = mycursor.fetchall()
        ketqua = "id_saved , link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , ip_them_su_kien, device_them_su_kien,thoigian_sukien, id_toan_bo_su_kien ,so_thu_tu_su_kien VALUES " + str(id_saved_max) + " " + str(link_da_swap)  + " " +str(date)  + " " +str(ten_su_kien) + " " + str(noidung_su_kien) +  " " + str(ip_them_su_kien)  +  " " + str(device_them_su_kien) +  " " + str(thoigian_sukien) +  " " + str( id_toan_bo_su_kien) +  " " + str(so_thu_tu_su_kien)
        thong_tin = {"ketqua":ketqua }
        connection.commit()
        print(mycursor.rowcount, "record inserted.")
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"ketqua":"Failed to connect to MySQL database: " + str(error)}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return thong_tin
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)


    