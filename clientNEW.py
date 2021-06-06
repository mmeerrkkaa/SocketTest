from random import randint
import socket
import ast
import json
from time import sleep
import sys

def soc_open(addres, name):
	global soc

	soc = socket.socket()
	soc.connect((addres[0], addres[1]))

	soc.send(f"{name}\n".encode())
	sleep(0.2)
	soc.send(f"['Connection']\n".encode())

	data = soc.recv(1024).decode()
	if data == "Аккаунт уже в сети":
		print(data)
		sys.exit()




def db(name):
	print(1)
	sleep(0.2)
	soc.send(f"['Запрос данных']\n".encode())
	data = soc.recv(1024).decode()
	return ast.literal_eval(data)

class Game:
	def __init__(self, name):
		self.name = name
		soc_open(addres, self.name)
		sleep(0.2)
		Game.menu(self)

	def menu(self):
		while 1:
			sleep(0.2)
			soc.send(f"['Online']\n".encode())
			online = soc.recv(1024).decode()
			print(f"Ваш ник: {self.name}. Онлайн: {online} player")
			a = int(input("1) начать игру\n2) Посмотреть статистику\n3) Топ по кол-ву игр: "))

			if a == 1:
				Game.play(self)
			elif a == 2:
				Game.CheckLog(self)
			elif a == 3:
				Game.Tops(self)


	def play(self):
		data = db(self.name)
		Num = randint(1, data[4])
		poptk = 0

		while 1:
			print(Num)
			a = int(input("Выберите число: "))
			poptk += 1
			if a == Num:
				print("Правильно!")
				games = data[1] + 1
				atmps = data[2] + poptk

				log = json.loads(data[3])
				log.append([ast.literal_eval(data[3])[-1][0] + 1 if len(ast.literal_eval(data[3])) != 0 else 1, poptk, Num])
				sleep(0.2)
				soc.send(f"['Обновление данных', {games}, {atmps}, {str(log)}, {data[4]}]\n".encode())
				break

			elif a > Num:
				print("Меньше")
			elif a < Num:
				print("Больше")



	def CheckLog(self):
		data = db(self.name)
		print(f"Игр: {data[1]}")
		if len(ast.literal_eval(data[3])) == 0:
			return

		poptk = 0
		count = 0
		for i in ast.literal_eval(data[3]):
			poptk += i[1]
			count += 1
			print(f"Игра №{i[0]} | Попыток: {i[1]} | Загаданное число: {i[2]}")

		print(f"Ср.Кол-во попыток: {round(poptk/count, 1)}")

	def Tops(self):
		soc.send("['Top']".encode())
		top = soc.recv(1024).decode()
		top = ast.literal_eval(top)
		text = ""
		for i in range(len(top)):
			text += f"{i+1} место: {top[i][0]} = {top[i][1]} Игр\n"
		print(text)

		a = int(input("Получить полную статистику игрока. Введите место или 0 для отмены: "))
		if a == 0:
		  pass

		else:
			try:
				print(top[a-1])
				print(f"Игр: {top[a-1][1]}")
				if len(ast.literal_eval(top[a-1][3])) == 0:
					return
				poptk = 0
				count = 0
				for i in ast.literal_eval(top[a-1][3]):
					poptk += i[1]
					count += 1
					print(f"Игра №{i[0]} | Попыток: {i[1]} | Загаданное число: {i[2]}")
				print(f"Ср.Кол-во попыток: {round(poptk/count, 1)}")

			except: print("Err")

addres = input("Адрес: ").replace(":", " ").split()
#soc.connect(("127.0.0.1", 8989))

Game(input("Ник: "))
