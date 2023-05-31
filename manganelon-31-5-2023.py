from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json
import mysql.connector
import time
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

config = {
                'user': 'root',
                'password': 'mcso@123#@! ',
                'host': 'localhost',
                'port': 3306,
                'database': 'manganelon'
                }
# def mangaFavorite():
#     try:
#         connection= mysql.connector.connect(**config)
#         if connection.is_connected():
#             creatcur = connection.cursor()
#             creatcur.execute("create table mangaFavorite(id	INTEGER PRIMARY KEY," +
#                                 "idUser	INTEGER," +
#                                 "dateTimeLike	TEXT," +
#                                 "Link_Manga_like	TEXT," +
#                                 "ip_like	TEXT," +
#                                 "name_device_like TEXT)")
            
#             connection.commit()  
#             creatcur.close()  
#             connection.close()  
#     except:
#         print("not connected database")
# mangaFavorite()    
 


app = Flask(__name__)

@app.route("/search", methods=["GET"])
def searchManga():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='search-story-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='item-img').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['src']
        item['authod']=itemMangaLastUpdate.find('span',class_='text-nowrap item-author').text
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('a',class_='item-chapter a-h text-nowrap'):
            item2 = 'https://ww5.manganelo.tv' +  chap.get('href')
            link_full2.append(item2)
            item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga


@app.route("/categorieslist", methods=["GET"])
def categorieslist():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='content-genres-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='genres-item-img').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['src']
        item['author_home']=itemMangaLastUpdate.find('span',class_='genres-item-author').text
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('a'):
            itemChapter={}
            itemChapter['link'] = 'https://ww5.manganelo.tv' +  chap.get('href')
            itemChapter['title'] = chap.get('title')
            link_full2.append(itemChapter)
            item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga

#Lấy category ở home
#Lấy link chapter
@app.route("/homenelo", methods=["GET"])
def get_Home():
    listJsonManga = {}
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonManga['latest_uptate'] = 'READ MANGA ONLINE - LATEST UPDATES'
    chapter=soupManga_base.find('div',class_='content-homepage-item-right') 
    link_full= []
    
    indexRun = 0
    for itemMangaLastUpdate in soupManga_base.find_all('div', class_='content-homepage-item'):    
        item={}
        item2={}
        item['title'] =itemMangaLastUpdate.find('a', class_='tooltip a-h text-nowrap').text
        item['link']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.a['href']
        item['poster']= 'https://ww5.manganelo.tv' + itemMangaLastUpdate.img['data-src']
        item['author_home']=itemMangaLastUpdate.find('span',class_='text-nowrap item-author').text.replace("\r","").replace("\n"," ").replace(" ","")
        index2 = 0
        link_full2= [] 
        for chap in  itemMangaLastUpdate.find_all('p',class_='a-h item-chapter'):
            itemChapter={}
            item2 = chap.text.replace("\r","-").replace("\n"," ") 
            itemChapter["title"] = item2
            itemChapter["link"] = chap.a['href']
            link_full2.append(itemChapter)
        item['chapter_home']=link_full2
        indexRun = indexRun + 1    
        link_full.append(item)            
    listJsonManga['manga_link'] = link_full
    return listJsonManga
#Lấy category ở home
@app.route("/category_home", methods=["GET"])
def get_category():
    listJsonMang = {}
    item=[]
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    rManga_base = session.get(link_full)
    soupManga_base = BeautifulSoup(rManga_base.content, 'html.parser')
    listJsonMang['genres']='MANGA BY GENRES'
    soup=soupManga_base.find('div', class_='panel-category')
    category=soup.find_all('p', class_='pn-category-row')
    list_cate=[]
    for item in category:
        text_cate=item.text.replace("\r","").replace("\n"," ")
        list_cate.append(str(text_cate))
    listJsonMang['category_home'] = list_cate
    return listJsonMang
#lấy thông tin của manga
@app.route("/detailmanga", methods=["GET"])
def get_DetailManga():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    detail = {}
    data1 = soup.find('table',class_='variations-tableInfo')
    lis = []
    def ac ():
        name_imgs = data1.find_all('tr')
        lis = []
        for i in name_imgs[3]:
            text_a = i.text.replace("\r","").replace("\n","").replace(" - ",",").replace(" ","")
            lis.append(str(text_a)) 
        del lis[0:3]
        return lis[:-1]
    #LẤY POSTER
    detail['poster_manga'] = 'https://ww5.manganelo.tv' + soup.find('div', class_='story-info-left').find('img', class_="img-loading").get('src')
    df = soup.find_all('h1')
    #LẤY TIÊU ĐỀ
    for i in df:
        detail['title_manga'] = i.text
    #LẤY AUTHOR
    list_au=[]
    for au in data1.find_all('td', class_='table-value'):
        text_au=au.text.replace("\r","").replace("\n"," ")
        list_au.append(text_au)
    detail['author']=list_au[1]
    #LẤY DESCRIPTIONS
    des = soup.find('div' , class_='story-info-right').findAll('h2')
    for ii in des:
        detail['descriptions'] = ii.text.replace("\r","").replace("\n","").replace(" ","")
    #Lấy status
    status=soup.find('div', class_='story-info-right').find_all('tr')
    for st in status[2].find('td', class_='table-value'):
        detail['status']=st.text.strip()
    #Lấy thể loại
    for li in data1.find_all("tr"):
        detail['categories'] = ac()
    detail['last_update'] = "27/12/2014"
    #Lấy lượt xem
    view=soup.find('div', class_='story-info-right-extent').find_all('p')
    for st in view[1].find('span', class_='stre-value'):
        detail['View']=st.text.strip()  
    #lấy xếp hạng
    list_xh=[]
    for xh in view:
        text=xh.text.replace("\r","").replace("\n","")
        list_xh.append(text)
    detail['Rating']=list_xh[3]
    #LẤY IMG BOOKMARK
    view2=soup.find('div', class_='story-info-right-extent').find('p', class_='info-bookmark')
    detail['infor_bookmark']='https://ww5.manganelo.tv/' + view2.find('img').get('src')
    #LẤY NỘI DUNG
    list_nd=[]
    nd=soup.find('div', class_='panel-story-info-description')
    for text1 in nd:
        text_nd=text1.text.replace("\r","").replace("\n","")
        list_nd.append(text_nd)
    detail['Description']= list_nd[2]
    return detail
#Lấy  link chapter
@app.route("/chapter", methods=["GET"])
def get_Chapter():
    link_full = request.headers.get('Link-Full')
    session = requests.Session()
    request_ses = session.get(link_full)
    soup = BeautifulSoup(request_ses.content, 'html.parser')
    item = {}
    data1 = soup.find('table',class_='variations-tableInfo')
    data_link = soup.find('div', class_='panel-story-chapter-list').find('ul', class_='row-content-chapter').find_all('li', class_='a-h')
    link_all = []
    for link in data_link:
        link_all.append(link.find('a').get('href'))
        reversed_link_all = list(reversed(link_all))
    def get_link_img(url_link):
        link_imgs=[] 
        request = requests.get('https://ww5.manganelo.tv/'+str(url_link))
        soup = BeautifulSoup(request.text, 'html.parser')
        data_img=soup.find('div',class_="container-chapter-reader").find_all('img' ,class_='img-loading')
        for item in data_img:
            link_imgs.append(item.get('data-src')) 
        return link_imgs
    def get_name_img(url_name):
            request = requests.get('https://ww5.manganelo.tv/'+str(url_name))
            soup = BeautifulSoup(request.text, 'html.parser')
            name_imgs = soup.find('div',class_="panel-chapter-info-top").find('h1').text
            return name_imgs
    link_all_img = []
    for link_img in range(0,len(reversed_link_all)):
        item_img={}
        a = 'page_list' + str(link_img+1)
        item_img['chapter_id']=link_img+1
        item_img['chapter_name']=get_name_img(reversed_link_all[link_img])
        item_img[a]=get_link_img(reversed_link_all[link_img])
        link_all_img.append(item_img)
    item['chapters']=link_all_img
    return item
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1983)


# # API lưu thông tin bộ truyện yêu thích của người dùng
@app.route('/api/favorite/<string:iduser>', methods=['POST'])
def add_favorite(iduser):
    id_like = request.form.get('like_id')
    #id_user =request.form.get('user_id')
    link = request.form.get('link')
    saved_at = request.form.get('saved_at')
    like_ip = request.form.get('like_ip')
    name_device_like = request.form.get('name_device')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            # curs.execute("INSERT INTO mangaFavorite (idLike,idUser, Link_Manga_like, dateTimeLike,ip_like,name_device) VALUES (%s, %s,%s, %s,%s,%s)", (id_like,id_user, link, saved_at, like_ip, name_device_like))
            curs.execute("INSERT INTO mangaFavorite (idUser, Link_Manga_like, dateTimeLike,ip_like,name_device) VALUES (%s,%s, %s,%s,%s)", (iduser, link, saved_at, like_ip, name_device_like))
            data = 'Favorite added successfully!'
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)

# API get ⇒ list favirote của 1 user

@app.route("/api/favirote/<string:iduser>", methods=["GET"])
def get_id(iduser):
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * from mangaFavorite where idUser=%s",(iduser,) )
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
    except:
        data = "error"
    return jsonify(data)


# API get ⇒ lấy 200 recent mới nhất của cả hệ thống user

@app.route("/api/last_200_recent", methods=["GET"])
def get_200_recent():
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * FROM mangaFavorite ORDER BY idLike DESC LIMIT 200")
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
    except:
        data = "error"
    return jsonify(data)


# API thêm recent của 1 user
@app.route("/api/recent/<string:iduser>", methods=["POST"])
def add_recent(iduser):
    link_chapter = request.form.get('link_chapter')
    link_manga= request.form.get('link_manga')
    datetime = request.form.get('datetime')
    ip_readed = request.form.get('ip_readed')
    name_device_readed = request.form.get('name_device')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("INSERT INTO recent_chapter_readed (link_detail_chapter, id_user, link_detail_manga, datetime, ip_readed, name_device_readed) VALUES (%s,%s,%s, %s,%s,%s)", (link_chapter, iduser, link_manga, datetime,ip_readed, name_device_readed))
            data = 'Favorite added successfully!'
            connection.commit()
            curs.close()
            connection.close()
    except:
        data = "error"
    return jsonify(data)

# API lấy toàn bộ recent của 1 user

@app.route("/api/recent/<string:iduser>", methods=["GET"])
def get_recent(iduser):
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * from recent_chapter_readed where id_user=%s",(iduser,))
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
            data = 'Favorite added successfully!'
    except:
        data = "error"
    return jsonify(data)

# API thêm avatar của 1 user
@app.route("/api/avatar/<string:iduser>", methods=["POST"])
def add_avatar(iduser):
    link_avatar = request.form.get('link_avatar')
    password= request.form.get('password')
    TimeOnline = request.form.get('TimeOnline')
    ip_register = request.form.get('ip_register')
    device_name_register = request.form.get('name_device')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("INSERT INTO users (link_avatar, id_user, password, TimeOnline, ip_register, device_name_register) VALUES (%s,%s,%s, %s,%s,%s)", (link_avatar, iduser, password, TimeOnline,ip_register, device_name_register))
            connection.commit()
            curs.close()
            connection.close()
            data = 'Favorite added successfully!'
    except:
        data = "error"
    return jsonify(data)
 

# API post thêm comment vào profile của 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["POST"])
def add_comment(iduser):
    Id_User_Comment = request.form.get('Id_User_Comment')
    NoiDungComment= request.form.get('NoiDungComment')
    link_image_attach = request.form.get('link_image_attach')
    dateTimeComment = request.form.get('dateTimeComment')
    nameDevice_Comment = request.form.get('name_device')
    IPComment = request.form.get('IPComment')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("INSERT INTO comment_user (Id_User_Comment, Id_User_Bi_Comment, NoiDungComment, link_image_attach, dateTimeComment, nameDevice_Comment,IPComment) VALUES (%s,%s,%s, %s,%s,%s, %s)", (Id_User_Comment, iduser, NoiDungComment, link_image_attach,dateTimeComment, nameDevice_Comment, IPComment))
            connection.commit()
            curs.close()
            connection.close()
            data = 'Favorite added successfully!'
    except:
        data = "error"
    return jsonify(data)

# API post lấy toàn bộ comment trên 1 user
@app.route("/api/profile/comment/<string:iduser>", methods=["GET"])
def get_comment(iduser):
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * from comment_user where id_User_Bi_Comment=%s",(iduser,))
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
    except:
        data = "error"
    return jsonify(data)
# API get ⇒ lấy 200 recent mới nhất của cả hệ thống user
@app.route("/api/200_comment", methods=["GET"])
def get_200_comment():
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * FROM comment_user ORDER BY idComment DESC LIMIT 200")
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
    except:
        data = "error"
    return jsonify(data)


# API post thêm thời gian đang hoạt động lên 1 trường trên database, cứ 1 phút gọi 1 lần
@app.route("/api/online/<string:iduser>", methods=["POST"])
def add_timeonline(iduser):
    link_avatar = request.form.get('link_avatar')
    ip_register= request.form.get('ip_register')
    device_name_register = request.form.get('device_name_register')
    password = request.form.get('password')
    TimeOnline = request.form.get('TimeOnline')
    # id_user = request.form.get('id_user')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcurs = connection.cursor()
            creatcurs.execute("SELECT id_user FROM users where id_user=%s",(iduser,))
            users = creatcurs.fetchone()
            if users is not None:
                curs = connection.cursor()
                curs.execute("UPDATE users SET link_avatar = %s, password = %s, TimeOnline = %s, ip_register = %s, device_name_register = %s WHERE id_user = %s", (link_avatar, password, TimeOnline,ip_register, device_name_register,iduser))
                connection.commit()
                curs.close()
                connection.close()
            else:
                curs = connection.cursor()
                curs.execute("INSERT INTO users (link_avatar, id_user, password, TimeOnline, ip_register, device_name_register) VALUES (%s,%s,%s, %s,%s,%s)", (link_avatar, iduser, password, TimeOnline,ip_register, device_name_register))
                connection.commit()
                curs.close()
                connection.close()
        data = 'Favorite added successfully!'
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
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT TimeOnline FROM users where id_user=%s",(iduser,))
            query = curs.fetchone()
            connection.commit()  
            curs.close() 
            connection.close() 
            if int(query[0])>0:
                 data = "online"
            else:
                data = "offline"
    except:
        data = "error"
    return jsonify(data)


# API ấy toàn bộ các user đang online trên hệ thống 
@app.route("/get/api/list_online", methods=["GET"])
def get_Online():
    a = "0"
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT * FROM users where TimeOnline>%s",(a,))
            data = curs.fetchall()
            connection.commit()  
            curs.close() 
            connection.close() 
    except:
        data = "error"
    return jsonify(data)

# API post comment vào 1 chapter
@app.route("/api/comment/chapter", methods=["POST"])
def add_comment_chapter():
    idUser = request.form.get('idUser')
    link_chapter= request.form.get('link_chapter')
    link_manga = request.form.get('link_manga')
    ip_comment = request.form.get('ip_comment')
    device_comment = request.form.get('device_comment')
    noidungComment = request.form.get('noidungComment')
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("INSERT INTO comment_chapter (idUser, noidungComment, link_chapter, link_manga, ip_comment, device_comment) VALUES (%s,%s,%s, %s,%s,%s)", (idUser, noidungComment, link_chapter, link_manga,ip_comment, device_comment))
            connection.commit()
            curs.close()
            connection.close()
            data = 'Favorite added successfully!'
    except:
        data = "error"
    return jsonify(data)

# API lấy toàn bộ comment của 1 user vào các bộ truyện manga
@app.route("/api/comment/<string:iduser>", methods=["GET"])
def get_user_comment(iduser):
    
    try:
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            curs = connection.cursor()
            curs.execute("SELECT noidungComment,idComment FROM comment_chapter where idUser=%s",(iduser,))
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
        connection= mysql.connector.connect(**config)
        if connection.is_connected():
            creatcur = connection.cursor()
            creatcur.execute("SELECT * FROM comment_chapter ORDER BY idComment DESC LIMIT 200")
            data = creatcur.fetchall()
            connection.commit()  
            creatcur.close() 
            connection.close()  
    except:
        data = "error"
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    
