import socket
import ast
import sqlite3
import json

conn = sqlite3.connect("games.db") # или :memory:
cursor = conn.cursor()
cursor.execute("DROP TABLE users")
cursor.execute(f"CREATE TABLE users(name STRING, games INTEGER, atmps INTEGER, log STRING, RandomNumber INTEGER);")
conn.commit()


soc = socket.create_server(("127.0.0.1", 8989))
soc.listen(10)

while True:
    try: con, addr = soc.accept()
        
    except socket.error:
        pass

    else:
        
        data = con.recv(1024).decode()
      #  print(data)
        try:
            data = ast.literal_eval(data)
        except: pass
        if len(data) == 1:
            cursor.execute(f'SELECT * FROM users where name="{data[0]}"')
            if cursor.fetchone()==None:
                print(f"{data[0]} - регистрирует аккаунт")
                sqliteAdd = json.dumps("[]")
                cursor.execute(f"INSERT INTO users VALUES ('{data[0]}', '0', '0', {sqliteAdd}, '100')")#вводит все данные об участнике в БД
                conn.commit()
            
            cursor.execute(f'SELECT * FROM users where name="{data[0]}"')
            print(f"{data[0]} - Запрашивает свои данные")
            con.send((f"{cursor.fetchone()}\n").encode())
            

        elif len(data) == 5:
            print(f"{data[0]} - Сыграл игру №{data[1]}. Обновление данных")
            sqliteAdd = json.dumps(data[3])
            cursor.execute(f'UPDATE users SET games="{data[1]}", atmps="{data[2]}", log="{sqliteAdd}", RandomNumber="{data[4]}" where name="{data[0]}"')
            conn.commit()
        

            con.send((f"{cursor.fetchone()}\n").encode())
        
        elif data == "топ":
            print(f"запрос данных топа")
            cursor.execute(f"SELECT name, games, atmps, log FROM users ORDER BY games DESC;")
            data = cursor.fetchall()
            
            
            con.send((f"{data}\n").encode())
                
                
   #     con.close()