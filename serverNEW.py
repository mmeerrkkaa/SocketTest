import asyncio
import socket
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


client = {}  # тут я буду хранить подключившивхся игроков (класс хранить)


# тут мы выполняем все действия связанные с аккаунтами (в будущем по крайне мере)
class User:
	def __init__(self, name):
		self.name = name

	def Connection(self):
		print(f"[{self.name}] Подключился")
		return User.CheckReg(self)  # проверка на существование пользователя

	def CheckReg(self):
		# Если аккаунт не создан, то создаём
		if cursor.execute(f'SELECT * FROM users where name="{self.name}"').fetchone() == None:
			sqliteAdd = json.dumps("[]")
			# вводит все данные об участнике в БД
			cursor.execute(f"INSERT INTO users VALUES ('{self.name}', '0', '0', {sqliteAdd}, '100')")
			conn.commit()
			print(f"{self.name} - регистрирует аккаунт")
			return "Вы зарегистрировали аккаунт"

		else:  # Если создан, то загружаем данные из базы данных
			self.games = cursor.execute(f'SELECT games FROM users where name="{self.name}"').fetchone()[0]
			self.atmps = cursor.execute(f'SELECT atmps FROM users where name="{self.name}"').fetchone()[0]
			self.log = ast.literal_eval(cursor.execute(f'SELECT log FROM users where name="{self.name}"').fetchone()[0])
			self.RandomNumber = cursor.execute(f'SELECT RandomNumber FROM users where name="{self.name}"').fetchone()[0]
			print(f"[{self.name}] Аккаунт загружен")
			return "Ваш акаунт загружен"

	def GetInfo(self): # собираем данные о пользователе
		data = cursor.execute(f'SELECT * FROM users where name="{self.name}"').fetchone()
		print(f"[{self.name}] - Запрашивает свои данные")
		return str(data)

	def update(self, games, atmps, log, randNum):
		sqliteAdd = json.dumps(log)
		cursor.execute(f'UPDATE users SET games="{games}", atmps="{atmps}", log="{sqliteAdd}", RandomNumber="{randNum}" where name="{self.name}"')
		conn.commit()
		print(f"[{self.name} Сыграл игру №{games}]")




async def handle_client(reader, writer):
	user = (await reader.read(1024)).decode('utf8')[:-1]
	while 1:

		try:  # Если можем преобразовать текст, значит всё ок
			data = (await reader.read(1024)).decode('utf8')
			data = ast.literal_eval(data)
		except Exception as ex:  # Тут мы можем получить только пустую строку, если была получена пустая строка, значит пользователь вышел
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)

			print("exc", user)
			if user in client:
				print(f"[{user}] Отключился")
				print(client)
				client.pop(user)
				print(client)
				writer.close()
				break
			else:
				writer.close()
				break

		# тут я буду принимать команды и обрабатывать. Шифрования нет, т.к тренировочный проект
		if data[0] == "Connection":
			#print(client, user)
			if user in client:
				response = "Аккаунт уже в сети"
				writer.write(response.encode('utf8'))
				await writer.drain()
				writer.close()
				break
			else:
				Users = User(user)
				client[user] = Users
				response = client[user].Connection()

		elif data[0] == "Запрос данных": # Пользователю отправляется строка(массив) со всеми своими данными
			response = client[user].GetInfo()

		elif data[0] == "Обновление данных":
			response = client[user].update(data[1], data[2], data[3], data[4])
			await writer.drain()
			continue

		elif data[0] == "Online":
			response = str(len(client))

		elif data[0] == "Top":
			response = str(cursor.execute(f"SELECT name, games, atmps, log FROM users ORDER BY games DESC;").fetchall())
			print(f"[{user}] Запрос данных топа")


	# elif data[0] in dir(User):  # тут не работает.
	#	response = f'{client[user].{data[0]}()}\n' # Я хотел проверять, существует ли функция в классе и если существует, то вызвать её

		writer.write(response.encode('utf8'))
		await writer.drain()
	writer.close()


async def run_server():
	server = await asyncio.start_server(handle_client, 'localhost', 15557)
	async with server:
		await server.serve_forever()

asyncio.run(run_server())
