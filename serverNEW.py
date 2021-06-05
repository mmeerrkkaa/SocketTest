import asyncio, socket
import ast
import math
import sqlite3
import json

conn = sqlite3.connect("games.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE users")
cursor.execute(f"CREATE TABLE users(name STRING, games INTEGER, atmps INTEGER, log STRING, RandomNumber INTEGER);")
# name Имя, games Кол во игр, atmps попыток, log массив с играми, RandomNumber число от какого загадывать По идее вам от этой информации роли нету

conn.commit()


client = {} # тут я буду хранить подключившивхся игроков (класс хранить)

class User:  # тут мы выполняем все действия связанные с аккаунтами (в будущем по крайне мере)
	def __init__(self, name):
		self.name = name
		User.CheckReg(self) # проверка на существование

	def CheckReg(self):
		if cursor.execute(f'SELECT * FROM users where name="{self.name}"').fetchone() == None: # Если аккаунт не создан, то создаём
			print(f"{self.name} - регистрирует аккаунт")
			sqliteAdd = json.dumps("[]")
			cursor.execute(f"INSERT INTO users VALUES ('{self.name}', '0', '0', {sqliteAdd}, '100')")#вводит все данные об участнике в БД
			conn.commit()
		else: # Если создан, то загружаем данные из базы данных
			self.games = cursor.execute(f'SELECT games FROM users where name="{self.name}"').fetchone()[0]
			self.atmps = cursor.execute(f'SELECT atmps FROM users where name="{self.name}"').fetchone()[0]
			self.log = ast.literal_eval(cursor.execute(f'SELECT log FROM users where name="{self.name}"').fetchone()[0])
			self.RandomNumber = cursor.execute(f'SELECT RandomNumber FROM users where name="{self.name}"').fetchone()
			print(f"[{self.name}] Аккаунт загружен")


async def handle_client(reader, writer):


    while 1:
        data = (await reader.read(1024)).decode('utf8')

        data = ast.literal_eval(data)
        print(data)


        if data[0] == "Подключение": # тут я буду принимать команды и обрабатывать. Шифрования нет, т.к тренировочный проект
        	print(f"[{data[1]}] Подключился")
        	client[data[1]] = User(data[1])
        	print(client[data[1]])

        response = f'{client[data[1]]}\n'
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15557)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())