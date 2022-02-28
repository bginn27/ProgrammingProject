import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO inventory (id, itemName, description, location) VALUES (?, ?, ?, ?)",
            (1000, 'Darth Vader Lego', 'Big hat, small body', "Lego Store")
            )

cur.execute("INSERT INTO inventory (id, itemName, description, location) VALUES (?, ?, ?, ?)",
            (1001, 'Chocolate Chip Cookie', 'Delicious goodness from heaven', "Heaven")
            )
 
connection.commit()
connection.close()