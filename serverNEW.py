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


	def Connection(self):
		print(f"[{self.name}] Подключился")
		print(client[self.name])
		return User.CheckReg(self) # проверка на существование

	def CheckReg(self):
		if cursor.execute(f'SELECT * FROM users where name="{self.name}"').fetchone() == None: # Если аккаунт не создан, то создаём
			sqliteAdd = json.dumps("[]")
			cursor.execute(f"INSERT INTO users VALUES ('{self.name}', '0', '0', {sqliteAdd}, '100')")#вводит все данные об участнике в БД
			conn.commit()
			print(f"{self.name} - регистрирует аккаунт")
			return "Вы зарегистрировали аккаунт"

		else: # Если создан, то загружаем данные из базы данных
			self.games = cursor.execute(f'SELECT games FROM users where name="{self.name}"').fetchone()[0]
			self.atmps = cursor.execute(f'SELECT atmps FROM users where name="{self.name}"').fetchone()[0]
			self.log = ast.literal_eval(cursor.execute(f'SELECT log FROM users where name="{self.name}"').fetchone()[0])
			self.RandomNumber = cursor.execute(f'SELECT RandomNumber FROM users where name="{self.name}"').fetchone()[0]
			print(f"[{self.name}] Аккаунт загружен")
			return "Аккаунт загружен"

	def GetInfo(self):
		print(1)
		return self.name


async def handle_client(reader, writer):


    while 1:
        data = (await reader.read(1024)).decode('utf8')

        data = ast.literal_eval(data)
        print(data)


        if data[0] == "Connection": # тут я буду принимать команды и обрабатывать. Шифрования нет, т.к тренировочный проект
        	Users = User(data[1])
        	client[data[1]] = Users
        	response = client[data[1]].Connection()

        elif data[0] in dir(User):  # тут не работает.
        	response = f'{client[data[1]].{data[0]}()}\n' # Я хотел проверять, существует ли функция в классе и если существует, то вызвать её


        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15557)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
