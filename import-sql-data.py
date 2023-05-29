import json
import mysql.connector

_LINK_JSON_FILE = "/home/dev/Desktop/ListChapterTruyenTranh.json"
HOST = 'localhost'
USER = 'root'
PASSWD = '@Huytre123qwe'
DB = 'manga'


def getDataJson():
    with open(_LINK_JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def insertChapterIntoDB(id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release, id_server):
    try:
        dbcon = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD, db = DB)
        cursor = dbcon.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ListChapterTruyenTranh
                          (id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release, id_server) 
                          VALUES (%s, %s, %s, %s, %s, %s);"""
        
        data_tuple = (id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release, id_server)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        dbcon.commit()
        print("Chapter inserted successfully into SqliteDb_developers table: " + id_chapter)
        cursor.close()

    except mysql.connector.Error as error:
        dbcon.rollback()
        print("Failed to insert Chapter variable into sqlite table:", error)
    finally:
        if dbcon:
            dbcon.close()
            print("The SQLite connection is closed")

def insertDataIntoDB(data):
    for chapter in data:
        index1 = chapter['id_manga'].index('.')
        index2 = chapter['id_manga'].index('/', index1)
        id_server = chapter['id_manga'][:index2]
        id_manga = chapter['id_manga']
        id_chapter = chapter['id_chapter']
        list_image_chapter_da_upload = chapter['list_image_chapter_da_upload']
        list_image_chapter_server_goc = chapter['list_image_chapter_server_goc']
        thoi_gian_release = chapter['thoi_gian_release']
        insertChapterIntoDB(id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release, id_server)

if __name__ == '__main__':
    # Lay data
    data = getDataJson()
    # Dua data vao Database
    insertDataIntoDB(data)