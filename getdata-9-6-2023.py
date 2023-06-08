import argparse
from socket import socket

import cv2
from flask import request, jsonify
import mysql.connector
from numpy import random
from face_detection import select_face, select_all_faces
from face_swap import face_swap
import datetime
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



def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        # print(response.raw ,"****")
    del response


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

#get data simple

@app.route('/getdata', methods=['GET', 'POST'])
def createdata():
    list_API_KEY = [
                    '0648864ce249f9b501bb3ff7735eb1cd', 'ddc51a8c2a1ed5ef16a9faf321c6821a',
                    '9011a7cfd693ed788a0a98814fc7a118', 'ef1cb4ba4157f0abf53fa17447f10fe7',
                    '31aef57415d034fdb2489d3bedf5d6a4', '6374d7c9cfa9f0cb372098bdf76d806e',
                    '21778d638b0d33c5d855729746deba81', '0cb8df6d364699a53973c9a6ce3c4466',
                    'e3a75062a4e22018ad8c3ab8f24eee5c', '7239a119b60707f567ebd17c097f5696',
                    '92cd47cbd5c08f5465d6f5d465bf4f8d']
    list_return_data = []
    index_demo = 0
    random_case = random.randint(0,5)
    
    array_direct = []
    get_id_js = []
    print("random_case", random_case)
    if random_case == 0:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay2', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 1:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 2:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['sknym', 'skGapNhau', 'skhanhphuc', 'skmuasam', 'skkethon', 'sklyhon']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        check_imgbb_api_key(list_API_KEY[i])
                        api_key=list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 3:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['skGapNhau', 'skhanhphuc', 'skmuasam', 'skkethon', 'skchaunoi', 'skvohoacchongchettruoc']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 4:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay2', 'sknym', 'skGapNhau', 'skhanhphuc', 'skkethon', 'skchaunoi']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
    if random_case == 5:
        while (True):
            item1SuKien = {}
            choose_case = 0
            get_id = {}
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')

            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")

            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")

            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                # mycursor.execute(sql, val)
                random_sukien = ['skGapNhau', 'skhanhphuc', 'skkethon', 'skchaunoi', 'sklyhon', 'skmuasam']
                print(random_sukien[index_demo])

                item1SuKien["tensukien"] = random_sukien[index_demo]

                rd = random.randint(1, 25)
                index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
                            random.randint(1, 25), random.randint(1, 25)]
                print("index  sk ", index_sk[index_demo])
                print("index demosk ", index_demo)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)
                item1SuKien["image couple"] = my_string12

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)
                item1SuKien["image husband"] = my_string1

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                item1SuKien["image wife"] = my_string2

                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0" and my_string2 != "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0" and my_string1 != "0":
                    choose_case = 2
                    download_image(my_string1, filename3)
                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                item1SuKien["thongtin"] = my_string

                if choose_case == 1:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if (check_imgbb_update(list_API_KEY, vitri=vitri) == True):
                    #     api_key = list_API_KEY[vitri]
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 2:
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)
                    #

                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output,
                                           args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)
                    # vitri=0
                    # if(check_imgbb_update(list_API_KEY , vitri=vitri)==True):
                    #     api_key=list_API_KEY[vitri]
                    # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    for i in range (0 , 11):
                        if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                    direct_link = upload_image_to_imgbb(output_path, api_key)
                    item1SuKien["Link_img"] = direct_link
                if choose_case == 3:
                    if my_string13 == "namsau":
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"], output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image2, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image1, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'

                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link

                    else:
                        # Swap faces
                        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg',
                                                  out='results/output1.jpg',
                                                  warp_2d=False,
                                                  correct_color=False, no_debug_window=True)
                        src_img = cv2.imread(args.src)
                        dst_img = cv2.imread(args.dst)
                        src_points, src_shape, src_face = select_face(src_img)
                        dst_faceBoxes = select_all_faces(dst_img)

                        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                                   out='results/output2.jpg',
                                                   warp_2d=False,
                                                   correct_color=False, no_debug_window=True)
                        src_img2 = cv2.imread(args1.src)
                        dst_img2 = cv2.imread(args1.dst)
                        src_points2, src_shape2, src_face2 = select_face(src_img2)
                        dst_faceBoxes2 = select_all_faces(dst_img2)
                        # progress_bar.update(6)

                        if dst_faceBoxes is None:
                            print('Detect 0 Face !!!')
                        output = dst_img

                        if dst_faceBoxes2 is None:
                            print('Detect 0 Face !!!')
                            exit(-1)
                        output2 = dst_img2

                        for k, dst_face in dst_faceBoxes.items():
                            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                               dst_face["shape"],
                                               output, args)
                        output_path = 'results/output1.jpg'
                        cv2.imwrite(output_path, output)

                        for k, dst_face2 in dst_faceBoxes2.items():
                            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                                dst_face2["shape"],
                                                output2,
                                                args1)
                        output_path2 = 'results/output2.jpg'
                        cv2.imwrite(output_path2, output2)

                        image1 = Image.open('results/output1.jpg')
                        image2 = Image.open('results/output2.jpg')

                        image_1 = cv2.imread('results/output1.jpg')
                        image_2 = cv2.imread('results/output2.jpg')

                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        max_width = max(width1, width2)
                        max_height = max(height1, height2)
                        new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
                        new_image.paste(image1, (0, 0))
                        # chuyen anh dau vao vi tri (max_width,0)
                        new_image.paste(image2, (max_width, 0))
                        new_image.save('results/output.jpg')

                        result_img = 'results/output.jpg'
                        # hiển thị ảnh đã ghép
                        # api_key = "9011a7cfd693ed788a0a98814fc7a118"
                        vitri = 0
                        for i in range(0, 11):
                            if (check_imgbb_api_key(list_API_KEY[i]) == True):
                                 api_key = list_API_KEY[i]
                        direct_link = upload_image_to_imgbb(result_img, api_key)
                        item1SuKien["Link_img"] = direct_link
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    api_key = "9011a7cfd693ed788a0a98814fc7a118"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    item1SuKien["Link_img"] = direct_link

                list_return_data.append(item1SuKien)
                array_direct.append(direct_link)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                item1SuKien["thongtin"] = my_string
                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            index_demo += 1
            if index_demo == 6:
                break

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            index_vs2 = 0
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
            result_id_sk = mycursor.fetchall()

            while True:
                mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
                result2 = mycursor.fetchall()

                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                result1 = mycursor.fetchall()
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date

                print("***", list_return_data[index_vs2]["image husband"])
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])

                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return jsonify(json1=list_return_data, json2=get_id_js)
# tim theo id Love
@app.route('/lovehistory/<string:idlove>', methods=['GET'])
def getDataLoveHistory(idlove):

    thong_tin = {}
    list_thong_tin = []
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
    try:
        connection = mysql.connector.connect(**config)
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
        index_get_data = 0
        for i in range(0, 6):
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
    noi_dung = request.headers.get('noi_dung_cmt')
    device_cmt = request.headers.get('device_cmt')
    id_toan_bo_su_kien = request.headers.get("id_toan_bo_su_kien")
    ipComment = request.headers.get("ipComment")
    imageattach = request.headers.get("imageattach")
    thong_tin={}
    list_thong_tin=[]
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
    try:
        connection = mysql.connector.connect(**config)
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
        datetimenow = datetime.datetime.utcnow()
        lenhquery = f"INSERT INTO comment(id_Comment,noi_dung_Comment,IP_Comment,device_Comment,id_toan_bo_su_kien,imageattach,thoi_gian_release) VALUES ( {idNext} ,%s,%s,%s, {id_toan_bo_su_kien} ,%s, {datetimenow})"
        # sql = f"INSERT INTO comment VALUES ( {idNext}, %s, %d, %s , %s , %s )"
        print(idNext)
        val = (noi_dung ,ipComment , device_cmt,imageattach)
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
        thong_tin["thoi_gian_release"]= datetimenow.strftime('%Y-%m-%d %H:%M:%S')
        # mycursor.execute("SELECT thong_tin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
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
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
        PhanTuMax = mycursor.fetchall()
        soPhanTu = PhanTuMax[0][0]   
        if trang * 25 > soPhanTu:
            return {"messages" : "vuot qua so phan tu"}
        for idItemPhanTu in range(trang * 25, trang * 25 + 25):
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
    config = {
                'user': 'leooRealman',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove2'
            }
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * FROM comment  LIMIT 50 offset {(trang-1) *50}")
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
            list_thong_tin.append(thong_tin)
            thong_tin = {}
            print(datetime.datetime.utcnow())



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
@app.route("/lovehistory/comment/<int:id_toan_bo_su_kien>")
def getCommentHistory(id_toan_bo_su_kien):

    thong_tin = {}
    list_thong_tin = []
    config = {
        'user': 'leooRealman',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'futureLove2'
    }
    try:
        connection = mysql.connector.connect(**config)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)

