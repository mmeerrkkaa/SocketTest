from random import randint
import socket
import ast


def db(name):
    soc.send(f"{[name]}\n".encode())
    data = soc.recv(1024)
    print(data)

    return ast.literal_eval(data.decode())

class Game:
    def __init__(self, name):
        self.name = name

        data = db(self.name)

        

        Game.menu(self)
    
    def menu(self):
        while 1:
            a = int(input("1) начать игру\n2)Посмотреть статистику: "))

            if a == 1:
                Game.play(self)
            elif a == 2:
                Game.CheckLog(self)


    def play(self):
        data = db(self.name)
        Num = randint(1, data[4])
        poptk = 0

        while 1:
        #    print(Num)
            a = int(input("Выберите число: "))
            poptk += 1
            if a == Num:
                print("Правильно!")
                data = db(self.name)
                games = data[1] + 1
                atmps = data[2] + poptk
                log = ast.literal_eval(data[3]).append([ast.literal_eval(data[3])[-1][0] + 1 if len(ast.literal_eval(data[3])) != 0 else 1, poptk, Num])

                soc.send(f"{[self.name, games, atmps, log, data[4]]}\n".encode())
                data = soc.recv(1024)
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
        
soc = socket.socket()
soc.connect(("127.0.0.1", 8989))

Game("merka")