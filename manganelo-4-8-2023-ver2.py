from operator import or_
from urllib.parse import urlparse
from flask import Flask, jsonify, make_response, request, url_for
import requests
import uuid
import json
import random
import string
import mysql.connector
import time
from flask_mail import *
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask import current_app

# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import set_access_cookies

# from flask_jwt_extended import JWTManager
from bs4 import BeautifulSoup
from flask_cors import CORS
import bcrypt
from functools import wraps
from datetime import datetime, timedelta
import datetime
import jwt
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "devmobilepro1888@gmail.com"
app.config["MAIL_PASSWORD"] = "zibzvfmidbmufdso"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["JWT_SECRET_KEY"] = "devsenior"
app.config["SECURITY_PASSWORD_SALT"] = "my_salt_value"
app.config["SECRET_KEY"] = "manhdz"
# jwt = JWTManager(app)
mail = Mail(app)
# config = {
#                 'user': 'root',
#                 'password': 'mcso@123#@!',
#                 'host': '14.225.7.221',
#                 'port': 81,
#                 'database': 'huydong'
#                 }
config = {
    "user": "root",
    "password": "mcso@123#@!",
    "host": "localhost",
    "port": 3306,
    "database": "manga1",
}
#### API dki user
# kiem tra email dangki
secret = URLSafeTimedSerializer("mysecretkey")
# YOUR_SECRET_KEY = "keysecret"
YOUR_SECRET_KEY = "keysecret"


@app.route("/register", methods=["POST"])
def Create_account1():
    data = request.get_json()
    email = data.get("email")
    user_name = data.get("user_name")
    password = data.get("password")
    link_avatar = data.get("link_avatar")
    ip_register = data.get("ip_register")
    device_name_register = data.get("device_name_register")
    # TimeOnline = data.get("TimeOnline")

    connection = mysql.connector.connect(**config)
    try:
        # connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users where email=%s", (email,))
            user = cursor.fetchall()
            if not user:
                token = secret.dumps(
                    {
                        "email": email,
                        "user_name": user_name,
                        "password": password,
                        "link_avatar": link_avatar,
                        "ip_register": ip_register,
                        "device_name_register": device_name_register,
                        # "TimeOnline": TimeOnline
                    },
                    salt=app.config["SECURITY_PASSWORD_SALT"],
                )
                msg = Message(
                    "Xác nhận tài khoản",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[email],
                )
                link = url_for(
                    "confirm_email", token=token, _external=True
                )  # link đến route 'confirm_email'
                msg.body = "Your confirmation link is " + link
                mail.send(msg)
                message = {"status": 200, "message": "Please check your email or spam"}

            else:
                message = {"status": 400, "message": "Account or email already exists"}

            cursor.close()

    except Exception as e:
        print("Error while connecting to MySQL", e)
        message = {"status": 500, "message": "Error connecting to the database"}

    finally:
        if connection.is_connected():
            connection.close()

    return jsonify(message)


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        data = secret.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=300
        )  # max_age = 1 day
        email = data["email"]
        user_name = data["user_name"]
        password = data["password"]
        link_avatar = data["link_avatar"]
        ip_register = data["ip_register"]
        device_name_register = data["device_name_register"]
        # TimeOnline = data["TimeOnline"]

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM users where email=%s", (email,))
                user = cursor.fetchall()
                if not user:
                    hashed_password = bcrypt.hashpw(
                        password.encode("utf-8"), bcrypt.gensalt()
                    )
                    cursor.execute(
                        "INSERT INTO users (email, user_name, password, link_avatar, ip_register, device_name_register) VALUES (%s,%s,%s, %s,%s, %s)",
                        (
                            email,
                            user_name,
                            hashed_password,
                            link_avatar,
                            ip_register,
                            device_name_register,
                        ),
                    )
                    connection.commit()
                    cursor.close()
                    message = {
                        "status": 200,
                        "message": "Account created and email confirmed. Please check your email or spam.",
                    }
                else:
                    message = {
                        "status": 400,
                        "message": "Account or email already exists",
                    }
        except Exception as e:
            print("Error while connecting to MySQL", e)
            message = {
                "status": 500,
                "message": "Error while adding account to the database",
            }

    except SignatureExpired:
        message = {
            "status": 400,
            "message": "The confirmation link is invalid or has expired.",
        }

    return jsonify(message)

    ####   API Đăng nhập tài khoản


@app.route("/login", methods=["POST"])
def loginAccount():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Kiểm tra thông tin email trong cơ sở dữ liệu
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        user_info = mycursor.fetchone()

        if user_info:
            # Verify the password using bcrypt
            hashed_password = user_info[3]  # The hashed password stored in the database
            if bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            ):
                user = {
                    "id_user": user_info[0],
                    "email": user_info[1],
                    "user_name": user_info[2],
                    "link_avatar": user_info[4],
                    "ip_register": user_info[5],
                    "device_name_register": user_info[6],
                }

                # token_payload = {
                #     "user_id": user["id_user"],
                #     "exp": datetime.datetime.utcnow()
                #     + datetime.timedelta(days=1),  # Thời gian hết hạn của token
                # }
                # token = jwt.encode(token_payload, YOUR_SECRET_KEY, algorithm="HS256")

                return {"ketqua": "Đăng nhập thành công!", "user": user}
            else:
                return {"ketqua": "Email hoặc mật khẩu không đúng."}
        else:
            return {"ketqua": "Email hoặc mật khẩu không đúng."}

    except Exception as e:
        return {"ketqua": "Lỗi khi kết nối đến cơ sở dữ liệu."}


# def authenticate_user(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         auth_header = request.headers.get("Authorization")
#         if auth_header:
#             try:
#                 token = auth_header.split(" ")[1]
#                 token_payload = jwt.decode(token, YOUR_SECRET_KEY, algorithms=["HS256"])
#                 request.user_id = token_payload["user_id"]  # Thêm user_id vào request
#                 return func(*args, **kwargs)
#             except jwt.ExpiredSignatureError:
#                 return {"ketqua": "Token đã hết hạn, vui lòng đăng nhập lại."}
#             except jwt.InvalidTokenError:
#                 return {"ketqua": "Token không hợp lệ, vui lòng đăng nhập lại."}
#         else:
#             return {"ketqua": "Vui lòng cung cấp token trong tiêu đề Authorization."}
#
#     return wrapper


@app.route("/resetpass", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    user_name = data.get("user_name")

    try:
        # Kiểm tra xem email và user_name có tồn tại trong cơ sở dữ liệu không
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        mycursor.execute(
            "SELECT * FROM users WHERE email = %s AND user_name = %s",
            (email, user_name),
        )
        account = mycursor.fetchone()
        mycursor.close()
        connection.close()

        if not account:
            return {"ketqua": "Email hoặc user_name không tồn tại trong hệ thống."}

        # Tạo mật khẩu mới ngẫu nhiên
        new_password = generate_random_password()
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

        # Cập nhật mật khẩu mới vào cơ sở dữ liệu
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        mycursor.execute(
            "UPDATE users SET password = %s WHERE email = %s AND user_name = %s",
            (hashed_password, email, user_name),
        )
        connection.commit()
        mycursor.close()
        connection.close()

        # Gửi email chứa mật khẩu mới đến người dùng
        send_email(email, new_password)

        return {
            "ketqua": "Đã gửi yêu cầu đặt lại mật khẩu. Vui lòng kiểm tra email để tạo mật khẩu mới."
        }

    except Exception as e:
        return {"ketqua": "Đã xảy ra lỗi khi thực hiện yêu cầu đặt lại mật khẩu."}


# @app.route('/reset', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     email = data.get("email")
#     # email = '20021388@vnu.edu.vn'
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     query = "SELECT email FROM users WHERE email = %s"
#     values = (email,)
#     cursor.execute(query, values)
#     result = cursor.fetchone()
#
#     if result is not None:
#         email = result[0]
#         new_uuid = uuid.uuid4()
#
#         # Chuyển đổi giá trị UUID sang chuỗi
#         uuid_str = str(new_uuid)
#         new_password = uuid_str
#         update_query = "UPDATE users SET password = %s WHERE email = %s"
#         update_values = (new_password, email)
#         cursor.execute(update_query, update_values)
#         connection.commit()
#
#         send_email(email, new_password)
#
#         return jsonify({'message': 'Đã reset mật khẩu thành công và gửi email!'})
#     else:
#         return jsonify({'message': 'Không tìm thấy người dùng có tên đăng nhập {}'.format(email)})
#
#     cursor.close()
#     connection.close()


def generate_random_password():
    # Tạo mật khẩu ngẫu nhiên có 8 ký tự bằng cách sử dụng thư viện random
    letters = string.ascii_letters + string.digits + string.punctuation
    new_password = "".join(random.choice(letters) for i in range(8))
    return new_password


# gưi mail reset
def send_email(email, new_password):
    from_address = "nguyentienmanh181102@gmail.com"  # Thay bằng địa chỉ email của bạn
    password = "avsmfkqcjouesezo"  # Thay bằng mật khẩu email của bạn

    to_address = email
    subject = "Reset mật khẩu"

    # Nội dung email
    body = f"""
    Xin chào,

    Mật khẩu mới của bạn là: {new_password}

    Hãy sử dụng mật khẩu này để đăng nhập vào tài khoản của bạn.

    Trân trọng,
    Đội ngũ của chúng tôi
    """

    # Tạo đối tượng MIMEText
    msg = MIMEText(body, "plain")
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    # Kết nối đến máy chủ email và gửi email
    try:
        server = smtplib.SMTP(
            "smtp.gmail.com", 587
        )  # Thay bằng thông tin máy chủ email của bạn
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()

        return {"ketqua": "Đã gửi email chứa mật khẩu mới đến địa chỉ email của bạn."}
    except Exception as e:
        print("loi", e)
        return {"ketqua": "Lỗi khi gửi email. Vui lòng thử lại sau."}


@app.route("/search", methods=["GET"])
def searchManga():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="search-story-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find("a", class_="item-img").text
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["src"]
        item["authod"] = itemMangaLastUpdate.find(
            "span", class_="text-nowrap item-author"
        ).text
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all(
            "a", class_="item-chapter a-h text-nowrap"
        ):
            item2 = "https://ww5.manganelo.tv" + chap.get("href")
            link_full2.append(item2)
            item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


@app.route("/categorieslist", methods=["GET"])
def categorieslist():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="content-genres-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find("a", class_="genres-item-img").get(
            "title"
        )
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["src"]
        item["author_home"] = itemMangaLastUpdate.find(
            "span", class_="genres-item-author"
        ).text
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all("a"):
            itemChapter = {}
            itemChapter["link"] = "https://ww5.manganelo.tv" + chap.get("href")
            itemChapter["title"] = chap.get("title")
            link_full2.append(itemChapter)
            item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


# Lấy category ở home
# Lấy link chapter
@app.route("/homenelo", methods=["GET"])
def get_Home():
    listJsonManga = {}
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonManga["latest_uptate"] = "READ MANGA ONLINE - LATEST UPDATES"
    chapter = soupManga_base.find("div", class_="content-homepage-item-right")
    link_full = []

    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all(
        "div", class_="content-homepage-item"
    ):
        item = {}
        item2 = {}
        item["title"] = itemMangaLastUpdate.find(
            "a", class_="tooltip a-h text-nowrap"
        ).text
        item["link"] = "https://ww5.manganelo.tv" + itemMangaLastUpdate.a["href"]
        item["poster"] = (
            "https://ww5.manganelo.tv" + itemMangaLastUpdate.img["data-src"]
        )
        item["author_home"] = (
            itemMangaLastUpdate.find("span", class_="text-nowrap item-author")
            .text.replace("\r", "")
            .replace("\n", " ")
            .replace(" ", "")
        )
        index2 = 0
        link_full2 = []
        for chap in itemMangaLastUpdate.find_all("p", class_="a-h item-chapter"):
            itemChapter = {}
            item2 = chap.text.replace("\r", "-").replace("\n", " ")
            itemChapter["title"] = item2
            itemChapter["link"] = chap.a["href"]
            link_full2.append(itemChapter)
        item["chapter_home"] = link_full2
        indexRun = indexRun + 1
        link_full.append(item)
    listJsonManga["manga_link"] = link_full
    return listJsonManga


# Lấy category ở home
@app.route("/category_home", methods=["GET"])
def get_category():
    listJsonMang = {}
    item = []
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, "html.parser")
    listJsonMang["genres"] = "MANGA BY GENRES"
    soup = soupManga_base.find("div", class_="panel-category")
    category = soup.find_all("p", class_="pn-category-row")
    list_cate = []
    for item in category:
        text_cate = item.text.replace("\r", "").replace("\n", " ")
        list_cate.append(str(text_cate))
    listJsonMang["category_home"] = list_cate
    return listJsonMang


# lấy thông tin của manga
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, "html.parser")
    detail = {}
    data1 = soup.find("table", class_="variations-tableInfo")
    lis = []

    def ac():
        name_imgs = data1.find_all("tr")
        lis = []
        for i in name_imgs[3]:
            text_a = (
                i.text.replace("\r", "")
                .replace("\n", "")
                .replace(" - ", ",")
                .replace(" ", "")
            )
            lis.append(str(text_a))
        del lis[0:3]
        return lis[:-1]

    # LẤY POSTER
    detail["poster_manga"] = "https://ww5.manganelo.tv" + soup.find(
        "div", class_="story-info-left"
    ).find("img", class_="img-loading").get("src")
    df = soup.find_all("h1")
    # LẤY TIÊU ĐỀ
    for i in df:
        detail["title_manga"] = i.text
    # LẤY AUTHOR
    list_au = []
    for au in data1.find_all("td", class_="table-value"):
        text_au = au.text.replace("\r", "").replace("\n", " ")
        list_au.append(text_au)
    detail["author"] = list_au[1]
    # LẤY DESCRIPTIONS
    des = soup.find("div", class_="story-info-right").findAll("h2")
    for ii in des:
        detail["descriptions"] = (
            ii.text.replace("\r", "").replace("\n", "").replace(" ", "")
        )
    # Lấy status
    status = soup.find("div", class_="story-info-right").find_all("tr")
    for st in status[2].find("td", class_="table-value"):
        detail["status"] = st.text.strip()
    # Lấy thể loại
    for li in data1.find_all("tr"):
        detail["categories"] = ac()
    detail["last_update"] = "27/12/2014"
    # Lấy lượt xem
    view = soup.find("div", class_="story-info-right-extent").find_all("p")
    for st in view[1].find("span", class_="stre-value"):
        detail["View"] = st.text.strip()
    # lấy xếp hạng
    list_xh = []
    for xh in view:
        text = xh.text.replace("\r", "").replace("\n", "")
        list_xh.append(text)
    detail["Rating"] = list_xh[3]
    # LẤY IMG BOOKMARK
    view2 = soup.find("div", class_="story-info-right-extent").find(
        "p", class_="info-bookmark"
    )
    detail["infor_bookmark"] = "https://ww5.manganelo.tv/" + view2.find("img").get(
        "src"
    )
    # LẤY NỘI DUNG
    list_nd = []
    nd = soup.find("div", class_="panel-story-info-description")
    for text1 in nd:
        text_nd = text1.text.replace("\r", "").replace("\n", "")
        list_nd.append(text_nd)
    detail["Description"] = list_nd[2]
    return detail


# Lấy  link chapter
@app.route("/chapter", methods=["GET"])
def get_Chapter():
    link_full = request.headers.get("Link-Full")
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, "html.parser")
    item = {}
    data1 = soup.find("table", class_="variations-tableInfo")
    data_link = (
        soup.find("div", class_="panel-story-chapter-list")
        .find("ul", class_="row-content-chapter")
        .find_all("li", class_="a-h")
    )
    link_all = []
    for link in data_link:
        link_all.append(link.find("a").get("href"))
        reversed_link_all = list(reversed(link_all))

    def get_link_img(url_link):
        link_imgs = []
        request = requests.get("https://ww5.manganelo.tv/" + str(url_link))
        soup = BeautifulSoup(request.text, "html.parser")
        data_img = soup.find("div", class_="container-chapter-reader").find_all(
            "img", class_="img-loading"
        )
        for item in data_img:
            link_imgs.append(item.get("data-src"))
        return link_imgs

    def get_name_img(url_name):
        request = requests.get("https://ww5.manganelo.tv/" + str(url_name))
        soup = BeautifulSoup(request.text, "html.parser")
        name_imgs = soup.find("div", class_="panel-chapter-info-top").find("h1").text
        return name_imgs

    link_all_img = []
    for link_img in range(0, len(reversed_link_all)):
        item_img = {}
        a = "page_list" + str(link_img + 1)
        item_img["chapter_id"] = link_img + 1
        item_img["chapter_name"] = get_name_img(reversed_link_all[link_img])
        item_img[a] = get_link_img(reversed_link_all[link_img])
        link_all_img.append(item_img)
    item["chapters"] = link_all_img
    return item


# # API lưu thông tin bộ truyện yêu thích của người dùng
@app.route("/api/favorite/<string:iduser>", methods=["POST"])
def add_favorite(iduser):
    # id_like = request.form.get("like_id")
    link = request.form.get("link")
    dateTimeLike = request.form.get("dateTimeLike")
    ip_like = request.form.get("ip_like")
    name_device_like = request.form.get("name_device")

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO mangaFavorite (idUser, dateTimeLike, Link_Manga_like,  ip_like, name_device) VALUES (%s, %s, %s, %s, %s)",
                (iduser, dateTimeLike, link, ip_like, name_device_like),
            )
            connection.commit()
            curs.close()
            connection.close()
            return jsonify(
                {
                    "message": "Favorite added successfully!",
                }
            )

    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"error": "Unknown error occurred."})


# API get ⇒ list favirote của 1 user
@app.route("/api/favirote/<string:iduser>", methods=["GET"])
def get_id(iduser):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT * from mangaFavorite where idUser=%s", (iduser,))
        data = cursor.fetchall()
        # print(data)

        if not data:
            return {"message": "No favorite data found."}

        mangaFavorites = []
        for row in data:
            mangaFavorite = {
                "id_like": row[0],
                "id_user": row[1],
                "dateTimeLike": row[2],
                "Link_data_like": row[3],
                "ip_like": row[4],
                "name_device": row[5],
            }
            mangaFavorites.append(mangaFavorite)

        cursor.close()
        connection.close()
        return mangaFavorites
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# API get ⇒ lấy 200 favorite mới nhất của bảng mangaFavorite


@app.route("/api/last_200_mangaFavorite", methods=["GET"])
def get_200_recent():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM mangaFavorite ORDER BY idLike DESC LIMIT 200")
        data = cursor.fetchall()

        list_mangafavourite = []
        for manga in data:
            manga_list = {
                "id_like": manga[0],
                "id_user": manga[1],
                "dateTimeLike": manga[2],
                "Link_Manga_like": manga[3],
                "ip_like": manga[4],
                "name_device": manga[5],
            }
            list_mangafavourite.append(manga_list)

        cursor.close()
        connection.close()
        return {"list_mangafavourite": list_mangafavourite}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# API thêm recent của 1 user
@app.route("/api/recent/<string:iduser>", methods=["POST"])
def add_recent(iduser):
    link_chapter = request.form.get("link_chapter")
    link_manga = request.form.get("link_manga")
    datetime = request.form.get("datetime")
    ip_readed = request.form.get("ip_readed")
    name_device_readed = request.form.get("name_device")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO recent_chapter_readed (link_detail_chapter, id_user, link_detail_manga, datetime, ip_readed, name_device_readed) VALUES (%s,%s,%s, %s,%s,%s)",
                (
                    link_chapter,
                    iduser,
                    link_manga,
                    datetime,
                    ip_readed,
                    name_device_readed,
                ),
            )
            data = "Favorite added successfully!"
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


@app.route("/api/recent/<string:iduser>", methods=["GET"])
def get_recent(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM recent_chapter_readed WHERE id_user = %s", (iduser,)
            )
            data = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()

            # Chuyển kết quả thành danh sách các từ điển
            result = []
            for row in data:
                item = {
                    "link_detail_chapter": row[0],
                    "id_readed": row[1],
                    "id_user": row[2],
                    "link_detail_manga": row[3],
                    "ip_readed": row[4],
                    "datetime": row[5],
                    "name_device_readed": row[6],
                }
                result.append(item)

            # Trả về dữ liệu dưới dạng JSON
            return jsonify(result)

    except:
        data = "error"
    return jsonify(data)


# API update avatar của 1 user
@app.route("/api/avatar/<string:iduser>", methods=["POST"])
def add_avatar(iduser):
    link_avatar = request.form.get("link_avatar")
    try:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()

        # Update the link_avatar for the user with the given id_user
        sql = "UPDATE users SET link_avatar = %s WHERE id_user = %s"
        val = (link_avatar, iduser)
        mycursor.execute(sql, val)
        connection.commit()
        mycursor.close()
        connection.close()

        return {"ketqua": "Avatar updated successfully!"}
    except Exception as e:
        return {"ketqua": "Lỗi khi kết nối đến cơ sở dữ liệu."}


# API post thêm comment vào profile của 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["POST"])
def add_comment(iduser):
    Id_User_Comment = request.form.get("Id_User_Comment")
    NoiDungComment = request.form.get("NoiDungComment")
    link_image_attach = request.form.get("link_image_attach")
    dateTimeComment = request.form.get("dateTimeComment")
    nameDevice_Comment = request.form.get("name_device")
    IPComment = request.form.get("IPComment")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO comment_user (Id_User_Comment, Id_User_Bi_Comment, NoiDungComment, link_image_attach, dateTimeComment, nameDevice_Comment,IPComment) VALUES (%s,%s,%s, %s,%s,%s, %s)",
                (
                    Id_User_Comment,
                    iduser,
                    NoiDungComment,
                    link_image_attach,
                    dateTimeComment,
                    nameDevice_Comment,
                    IPComment,
                ),
            )
            connection.commit()
            curs.close()
            connection.close()
            print("123")
            data = "Favorite added successfully!"
    except:
        data = "error"
    return jsonify(data)


# API  lấy toàn bộ comment trên 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["GET"])
def get_comment(iduser):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * from comment_user where id_User_Bi_Comment=%s", (iduser,)
        )
        data = cursor.fetchall()

        list_comments = []
        for comment in data:
            comments = {
                "id_user_Bi_Comment": comment[0],
                "id_User_comment": comment[1],
                "id_Comment": comment[2],
                "NoiDungComment": comment[3],
                "link_image_attach": comment[4],
                "dateTimeComment": comment[5],
                "name_device_comment": comment[6],
                "ip_comment": comment[7],
            }
            list_comments.append(comments)

        cursor.close()
        connection.close()
        return list_comments
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# API get ⇒ lấy 200 comment mới nhất của cả hệ thống comment_user
@app.route("/api/200_comment", methods=["GET"])
def get_200_comment():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comment_user ORDER BY idComment DESC LIMIT 200")
        data = cursor.fetchall()

        list_comments = []
        for comment in data:
            comments = {
                "id_user_Bi_Comment": comment[0],
                "id_User_comment": comment[1],
                "id_Comment": comment[2],
                "NoiDungComment": comment[3],
                "link_image_attach": comment[4],
                "dateTimeComment": comment[5],
                "name_device_comment": comment[6],
                "ip_comment": comment[7],
            }
            list_comments.append(comments)

        cursor.close()
        connection.close()
        return list_comments
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        cursor.close()
        connection.close()


# API post thêm thời gian đang hoạt động lên 1 trường trên database, cứ 1 phút gọi 1 lần
@app.route("/api/online/<string:iduser>", methods=["POST"])
def add_timeonline(iduser):
    # link_avatar = request.form.get("link_avatar")
    # ip_register = request.form.get("ip_register")
    # device_name_register = request.form.get("device_name_register")
    # password = request.form.get("password")
    TimeOnline = request.form.get("TimeOnline")
    # id_user = request.form.get('id_user')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            creatcurs = connection.cursor()
            creatcurs.execute("SELECT id_user FROM users where id_user=%s", (iduser,))
            users = creatcurs.fetchone()
            if users is not None:
                curs = connection.cursor()
                curs.execute(
                    "UPDATE users SET TimeOnline = %s WHERE id_user = %s",
                    (
                        TimeOnline,
                        iduser,
                    ),
                )
                connection.commit()
                curs.close()
                connection.close()
            else:
                curs = connection.cursor()
                curs.execute(
                    "INSERT INTO users (TimeOnline,id_user ) VALUES (%s,%s)",
                    (
                        TimeOnline,
                        iduser,
                    ),
                )
                connection.commit()
                curs.close()
                connection.close()
        data = " successfully!"
    except:
        data = "error"
    return jsonify(data)


def goi_timeonline(iduser):
    # t = threading.Thread(target=update_timeonline, args=[iduser])
    # t.start()
    while True:
        add_timeonline(iduser)
        time.sleep(60)


# API kiểm tra user hiện tại có đang online không ?
@app.route("/api/check_online/<string:iduser>", methods=["GET"])
def get_TimeOnline(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT TimeOnline FROM users where id_user=%s", (iduser,))
            query = curs.fetchone()
            connection.commit()
            curs.close()
            connection.close()
            if int(query[0]) > 0:
                data = "online"
            else:
                data = "offline"

            print(123)
    except:
        data = "error"
    return jsonify(data)


# API ấy toàn bộ các user đang online trên hệ thống
@app.route("/get/api/list_online", methods=["GET"])
def get_Online():
    a = "0"
    try:
        connection = mysql.connector.connect(**config)
        curs = connection.cursor()
        curs.execute("SELECT * FROM users where TimeOnline>%s", (a,))
        data = curs.fetchall()

        list_users = []
        for user in data:
            users = {
                "id_user": user[0],
                "email": user[1],
                "user_name": user[2],
                "link_avatar": user[4],
                "ip_register": user[5],
                "device_register": user[6],
                "time_online": user[7],
            }
            list_users.append(users)

        curs.close()
        connection.close()
        return list_users
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        curs.close()
        connection.close()


# API post comment vào 1 chapter
@app.route("/api/comment/chapter", methods=["POST"])
def add_comment_chapter():
    idUser = request.form.get("idUser")
    link_chapter = request.form.get("link_chapter")
    link_manga = request.form.get("link_manga")
    ip_comment = request.form.get("ip_comment")
    device_comment = request.form.get("device_comment")
    noidungComment = request.form.get("noidungComment")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "INSERT INTO comment_chapter (idUser, noidungComment, link_chapter, link_manga, ip_comment, device_comment) VALUES (%s,%s,%s, %s,%s,%s)",
                (
                    idUser,
                    noidungComment,
                    link_chapter,
                    link_manga,
                    ip_comment,
                    device_comment,
                ),
            )
            connection.commit()
            curs.close()
            connection.close()
            data = " comment successfully!"
    except:
        data = "error"
    return jsonify(data)


# API lấy toàn bộ comment của 1 user vào các bộ truyện manga
@app.route("/api/comment/<string:iduser>", methods=["GET"])
def get_user_comment(iduser):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute(
                "SELECT noidungComment,idComment FROM comment_chapter where idUser=%s",
                (iduser,),
            )
            data = curs.fetchall()
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ lấy 200 comment mới nhất của cả hệ thống user
@app.route("/api/last_200_comment", methods=["GET"])
def get_last_200_comment():
    try:
        connection = mysql.connector.connect(**config)
        creatcur = connection.cursor()
        creatcur.execute(
            "SELECT * FROM comment_chapter ORDER BY idComment DESC LIMIT 200"
        )
        data = creatcur.fetchall()

        list_comments = []
        for comment in data:
            comments = {
                "id_user": comment[0],
                "id_comment": comment[1],
                "link_chapter": comment[2],
                "link_manga": comment[3],
                "ip_comment": comment[4],
                "device_comment": comment[5],
                "noidung": comment[6],
            }
            list_comments.append(comments)
        creatcur.close()
        connection.close()
        return list_comments
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return {"error": str(err)}, 500
    finally:
        creatcur.close()
        connection.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1983)
