import asyncio, json
import mysql.connector

_LINK_DATA_CHAPTER = r"D:/Code Python/ThinkDiff/mysql_anime_manga/data/sssss.json"

async def insertChapterIntoTable(id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc,
								 thoi_gian_release):
	connect_mysql = mysql.connector.connect(host="localhost", user="root", password="", database="manga_teach")
	cursor = connect_mysql.cursor()

	try:
		sqlite_insert_with_param = """
		INSERT INTO LISTCHAPTER
		(id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release) 
		VALUES (%s, %s, %s, %s, %s);
		"""
		data_tuple = (
		id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release)
		cursor.execute(sqlite_insert_with_param, data_tuple)
		connect_mysql.commit()
		print(f"Inserted chapter successfully data into table")
		cursor.close()
	except mysql.connector.Error as error:
		print("Failed to insert Python variable into sqlite table", error)
	finally:
		if connect_mysql:
			connect_mysql.close()
			print("The SQLite connection is closed")


async def start_insert_list_chapter():
	with open(_LINK_DATA_CHAPTER, 'r', encoding='utf-8') as f:
		data = json.load(f)
	i = 0
	for chapter in data:
		id_chapter = chapter["id_chapter"]
		id_manga = chapter["id_manga"]
		list_image_chapter_da_upload = chapter["list_image_chapter_da_upload"]
		list_image_chapter_server_goc = chapter["list_image_chapter_server_goc"]
		thoi_gian_release = chapter["thoi_gian_release"]
		await insertChapterIntoTable(id_chapter, id_manga, list_image_chapter_da_upload, list_image_chapter_server_goc, thoi_gian_release)
		i += 1
		if i == 5:
			break

async def start():
	await start_insert_list_chapter()
asyncio.run(start())