import socket
import ast
import sqlite3

conn = sqlite3.connect("games.db") # или :memory:
cursor = conn.cursor()
cursor.execute("DROP TABLE users")
cursor.execute(f"CREATE TABLE users(name INTEGER, games INTEGER, atmps INTEGER, log STRING, RandomNumber INTEGER);")
conn.commit()


soc = socket.create_server(("127.0.0.1", 8989))
soc.listen(100)

while True:
    try: con, addr = soc.accept()
        
    except socket.error:
        pass

    else:
        data = con.recv(1024).decode()
            
        data = ast.literal_eval(data)

        if len(data) == 1:
            cursor.execute(f'SELECT * FROM users where name="{data[0]}"')
            if cursor.fetchone()==None:
                cursor.execute(f"INSERT INTO users VALUES ('{data[0]}', '0', '0', '[]', '100')")#вводит все данные об участнике в БД
                conn.commit()
            else:
                pass
            
            cursor.execute(f'SELECT * FROM users where name="{data[0]}"')

            con.send((f"{cursor.fetchone()}").encode())

        elif len(data) == 5:
            cursor.execute(f'UPDATE users SET games={data[1]}, atmps={data[2]}, log={data[3]}, RandomNumber={data[4]} where name={data[0]}')
            conn.commit()
            cursor.execute(f'SELECT * FROM users where name="{data[0]}"')
            con.send((f"{cursor.fetchone()}").encode())
        print(data)