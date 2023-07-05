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
import base64
import json
import shutil
from  checkImgbb import check_imgbb_update,check_imgbb_api_key
import requests
from datetime import datetime


# Config database mysql
config = {
        'user': 'leooRealman',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'futureLove2'
         }   
connection = mysql.connector.connect(**config)


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
 
def get_mycursor(config):
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            return cursor
        
def Random_Su_Kien(random_sukien, index_demo, mycursor):
    
    Item_Su_Kien = {}


    Item_Su_Kien["tensukien"] = random_sukien[index_demo]
    index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
            random.randint(1, 25), random.randint(1, 25)]    

    print("index  sk ", random_sukien[index_demo])
    mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    thongtin_sql = mycursor.fetchall()
    print('thongtin_sql', thongtin_sql[0])
    thongtin = ', '.join(thongtin_sql[0])
    print('thong tin ', thongtin)
    Item_Su_Kien["thongtin"] = thongtin


    mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    image_sql = mycursor.fetchall()
    print('image_sql', image_sql[0])
    image = ', '.join(image_sql[0])
    print('image_full ', image)
    Item_Su_Kien["image couple"] = image

    mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    vtrinam_sql = mycursor.fetchall()
    print('vtrinam_sql', vtrinam_sql[0])
    vtrinam = ', '.join(vtrinam_sql[0])
    print('vtrinam ', vtrinam)
    Item_Su_Kien["vtrinam"] = vtrinam


    mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    img_nam_sql = mycursor.fetchall()
    print('img_nam_sql', img_nam_sql[0])
    print("***")
    img_nam = ', '.join(img_nam_sql[0])
    print('img_nam', img_nam)
    Item_Su_Kien["image husband"] = img_nam

    mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    img_nu_sql = mycursor.fetchall()
    print('img_nu_sql', img_nu_sql[0])
    print("***")
    img_nu = ', '.join(img_nu_sql[0])
    print('img_nu', img_nu)
    Item_Su_Kien["image wife"] = img_nu

    return Item_Su_Kien

def choose_case_ne(Item, filename3, filename4):
    choose_case_func = 0
    if Item["image husband"] == "0" and Item["image wife"] == "0" and Item["image couple"] != "0":
        choose_case_func = 4
        download_image(Item["image couple"], "results/output.jpg")
    elif Item["image husband"] == "0" and Item["image wife"] != "0":
        choose_case_func = 1
        download_image(Item["image wife"], filename4)
    elif Item["image wife"] == "0" and Item["image husband"] != "0":
        choose_case_func = 2
        download_image(Item["image husband"], filename3)
    else:
        choose_case_func = 3
        download_image(Item["image husband"], filename3)
        download_image(Item["image wife"], filename4)
        
    return choose_case_func

def Link_Img_Swap_1_Face(filename1, filename2, list_API_KEY, file_name):
    args = argparse.Namespace(
        src=filename1,
        dst=filename2,
        out="results/{file_name}.jpg",
        warp_2d=False,
        correct_color=False,
        no_debug_window=True,
    )
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)
    src_points, src_shape, src_face = select_face(src_img)
    dst_faceBoxes = select_all_faces(dst_img)

    if dst_faceBoxes is None:
        print("Detect 0 Face !!!")

    output = dst_img
    if dst_faceBoxes != None:
        for k, dst_face in dst_faceBoxes.items():
            output = face_swap(
                src_face,
                dst_face["face"],
                src_points,
                dst_face["points"],
                dst_face["shape"],
                output,
                args,
            )
    output_path = "results/output1.jpg"
    cv2.imwrite(output_path, output)

    for i in range(0, 11):
        if check_imgbb_api_key(list_API_KEY[i]) == True:
            api_key = list_API_KEY[i]
    direct_link = upload_image_to_imgbb(output_path, api_key)

    return output_path, output, direct_link

def Link_Img_Swap_2_Face(filename1, filename2, filename3, filename4, list_API_KEY ):
    
    Image1 = Link_Img_Swap_1_Face(filename1, filename3, list_API_KEY, "output1")
    output_path1 = Image1[0]
    output11 = Image1[1]
    cv2.imwrite(output_path1, output11)

    Image2 = Link_Img_Swap_1_Face(filename2, filename4, list_API_KEY, "output2")
    output_path2 = Image2[0]
    output22 = Image2[1]
    cv2.imwrite(output_path2, output22)

    

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

    for i in range(0, 11):
        if (check_imgbb_api_key(list_API_KEY[i]) == True):
              api_key = list_API_KEY[i]

    direct_link = upload_image_to_imgbb(result_img, api_key)


    return direct_link

def randomGenData(random_case,random_sukien, link_full1, link_full2):



    list_API_KEY = [
                    '0648864ce249f9b501bb3ff7735eb1cd', 'ddc51a8c2a1ed5ef16a9faf321c6821a',
                    '9011a7cfd693ed788a0a98814fc7a118', 'ef1cb4ba4157f0abf53fa17447f10fe7',
                    '31aef57415d034fdb2489d3bedf5d6a4', '6374d7c9cfa9f0cb372098bdf76d806e',
                    '21778d638b0d33c5d855729746deba81', '0cb8df6d364699a53973c9a6ce3c4466',
                    'e3a75062a4e22018ad8c3ab8f24eee5c', '7239a119b60707f567ebd17c097f5696',
                    '92cd47cbd5c08f5465d6f5d465bf4f8d']
    list_return_data = []
    index_demo = 0
    get_id_js = []
    
    filename1 = 'imgs/anhtam1.jpg'
    filename2 = 'imgs/anhtam2.jpg'
    image_nam = 'imgs/anhtam3.jpg'
    image_nu = 'imgs/anhtam4.jpg'

        # Tải ảnh từ Link trong header
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)   
    print("random_case", random_case)

    while (True):
            get_id = {}
            try:
                mycursor = get_mycursor(config)
                cursor = connection.cursor
                print(random_sukien[index_demo])

                Item_Su_Kien = Random_Su_Kien(random_sukien, index_demo, mycursor)
                print("thongtin ne", Item_Su_Kien["image husband"])

                choose_case = choose_case_ne(Item_Su_Kien, image_nam, image_nu)
                print("choose_Case ", choose_case)


                if choose_case == 1:
                    link_img = Link_Img_Swap_1_Face(filename2, image_nu, list_API_KEY, "output1")
                    print("Link ne", link_img[2])
                    Item_Su_Kien["Link_img"] = link_img[2]
                    print("Link2 ne", Item_Su_Kien["Link_img"])          
                if choose_case == 2:
                    link_img = Link_Img_Swap_1_Face(filename1, image_nam, list_API_KEY, "output1")
                    print("Link ne", link_img[2])
                    Item_Su_Kien["Link_img"] = link_img[2]
                    print("Link2 ne", Item_Su_Kien["Link_img"])
                if choose_case == 3:
                    if Item_Su_Kien["vtrinam"] == "namsau":
                        link_img = Link_Img_Swap_2_Face(filename1, filename2, image_nam, image_nu, list_API_KEY)
                        print("Link ne", link_img)
                        Item_Su_Kien["Link_img"] = link_img
                        print("Link2 ne", Item_Su_Kien["Link_img"])
                    else:
                        
                        link_img = Link_Img_Swap_2_Face(filename1, filename2, image_nam, image_nu, list_API_KEY)
                        print("Link ne", link_img)   
                        Item_Su_Kien["Link_img"] = link_img    
                        print("Link2 ne", Item_Su_Kien["Link_img"])                
                if choose_case == 4:
                    result_img = 'results/output.jpg'

                    for i in range(0, 11):
                      if (check_imgbb_api_key(list_API_KEY[i]) == True):
                          api_key = list_API_KEY[i]

                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    Item_Su_Kien["Link_img"] = direct_link
                list_return_data.append(Item_Su_Kien)
                # Lưu các thay đổi vào database
                connection.commit()
                print(mycursor.rowcount, "record inserted.")
                connection.commit()
            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            print("index_demo: ", index_demo)
            index_demo += 1
            if index_demo == 6:
                break

    try:
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
                get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                get_id["real_time"] = date
                print(list_return_data[index_vs2]["Link_img"])
                print("hallooooooo")
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
                val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
                       list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
                       get_id["real_time"], list_return_data[index_vs2]["tensukien"],
                       list_return_data[index_vs2]["thongtin"])
                mycursor.execute(sql, val)
                index_vs2 += 1
                if index_vs2 == 6:
                    break

            get_id_js.append(get_id)

            # Lưu các thay đổi vào database
            connection.commit()
            print(mycursor.rowcount, "aloooo record inserted.")
    except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
    finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
    return jsonify(json1=list_return_data, json2=get_id_js)
