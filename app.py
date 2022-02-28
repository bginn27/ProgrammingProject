from crypt import methods
from fileinput import close
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    inventory = conn.execute("SELECT * FROM inventory").fetchall()
    for item in inventory[0]:
        print(item)
    conn.close()
    return render_template('inventory.html', inventory=inventory)


@app.route('/inventoryform')
def inventoryform():
    return render_template('inventoryform.html')

@app.route('/inventoryadd', methods=["GET", "POST"] )
def inventoryadd():
    if request.method == "POST":
        itemNum = request.form.get("itemNum")
        itemName = request.form.get("itemName")
        description = request.form.get("description")
        location = request.form.get("location")

      
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        add_inventory = cur.execute("INSERT INTO inventory (id, itemName, description, location) VALUES (?, ?, ?, ?)", (itemNum, itemName, description, location))
        conn.commit()
        conn.close()
        return render_template("inventory.html")

@app.route('/invoices')
def invoices():
    return render_template('invoices.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

if __name__ == '__main__':
    app.run(debug=True)