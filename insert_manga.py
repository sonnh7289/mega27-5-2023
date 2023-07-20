import asyncio, json
import mysql.connector

_LINK_DATA_MANGA = r"D:/Code Python/ThinkDiff/mysql_anime_manga/data/ListManga.json"

async def insertMangaIntoTable(id_manga, title_manga, descript_manga, link_image_poster_link_upload,link_image_poster_link_goc,
							   link_detail_manga, list_categories, list_chapter, rate, so_luong_view, status, tac_gia, id_server):
	connect_mysql = mysql.connector.connect(host="localhost", user="root", passwd="", db="manga_teach")
	cursor = connect_mysql.cursor()
	
	try:
		sqlite_insert_with_param = """
		INSERT INTO LISTMANGA
		(id_manga, title_manga, descript_manga, link_image_poster_link_upload, link_image_poster_link_goc, 
		link_detail_manga, list_categories, list_chapter, rate, so_luong_view, status, tac_gia, id_server) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
		"""
		data_tuple = (id_manga, title_manga, descript_manga, link_image_poster_link_upload, link_image_poster_link_goc,
					  link_detail_manga, list_categories, list_chapter, rate, so_luong_view, status, tac_gia, id_server)
		cursor.execute(sqlite_insert_with_param, data_tuple)
		connect_mysql.commit()
		print(f"Inserted manga successfully data into table")
		cursor.close()
	except mysql.connector.Error as error:
		print("Failed to insert Python variable into sqlite table", error)
	finally:
		if connect_mysql:
			connect_mysql.close()
			print("The SQLite connection is closed")
			
async def start_insert_list_manga():
	with open(_LINK_DATA_MANGA, 'r', encoding='utf-8') as f:
		data = json.load(f)
	i = 0
	for manga in data:
		id_manga = manga['ID_Manga']
		title_manga = manga['Title_Manga']
		descript_manga = manga['DescriptManga']
		link_image_poster_link_upload = manga['LinkImagePoster_link_Upload']
		link_image_poster_link_goc = manga['LinkImagePoster_linkgoc']
		link_detail_manga = manga['Link_Detail_Manga']
		list_categories = manga['ListCategories']
		list_chapter = manga['ListChapter']
		rate = manga['Rate']
		so_luong_view = manga['SoLuongView']
		status = manga['Status']
		tac_gia = manga['Tac_Gia']
		id_server = manga['id_Server']
		await insertMangaIntoTable(id_manga, title_manga, descript_manga, link_image_poster_link_upload, link_image_poster_link_goc,
								   link_detail_manga, list_categories, list_chapter, rate, so_luong_view, status, tac_gia, id_server)
		i += 1
		if i == 5:
			break

async def start():
	await start_insert_list_manga()

asyncio.run(start())