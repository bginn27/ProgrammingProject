import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO inventory (itemName, description, location) VALUES ( ?, ?, ?)",
            ('TestProduct1', 'Testing product 1', "School")
            )

cur.execute("INSERT INTO inventory (itemName, description, location) VALUES (?, ?, ?)",
            ('TestProduct2', 'Testing product 2', "School")
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('Brooke', 'Test123')
            )

 
connection.commit()
connection.close()