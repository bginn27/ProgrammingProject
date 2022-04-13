# from crypt import methods
from fileinput import close
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import false
from werkzeug.exceptions import abort

app = Flask(__name__)

from flask import Flask, render_template

# connection to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print('running post')
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            print('checking pass')
            error = 'Invalid Credentials. Please try again.'
        else:
            print('pass accepted')
            loggedIn = True
            return redirect("/")

# home page
@app.route('/')
def home():
    return render_template('home.html')

# # modify products in the table
# @app.route('/inventorymodify')
# def inventorymodify():
#     conn = get_db_connection()
#     posts = conn.execute('SELECT * FROM inventory').fetchall()
#     conn.close()
#     return render_template('inventorymodify.html')
    
# @app.route('/create', methods=('GET', 'POST'))
# def create():
#     return render_template('create.html')


# main inventory page
@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    inventory = conn.execute("SELECT * FROM inventory").fetchall()
    for item in inventory[0]:
        print(item)
    conn.close()
    return render_template('inventory.html', inventory=inventory)
      


# @app.route('/inventory/<id>')
# def inventoryID(id):
#     if request.method == "GET":
#         conn = get_db_connection()
#         inventory = conn.execute("SELECT * FROM inventory WHERE id={}".format(id)).fetchall()
#         for item in inventory[0]:
#             print(item)
#         conn.close()
#         return render_template('inventory.html', inventory=inventory)


# # remove row from table and return to main inventory page
# @app.route('/inventoryremove', methods=["GET","POST"] )
# def inventoryremove():
#     if request.method == "GET":
#         return render_template("inventoryremove.html")

#     if request.method == "POST":
#         itemNum = request.form.get("itemNum")
#         conn = get_db_connection()
#         conn.execute('DELETE FROM inventory WHERE id = ?', (itemNum,))
#         conn.commit()
#         conn.close()
#         return redirect("/inventory")



# add info to table and return to main inventory page
@app.route('/inventoryadd', methods=["GET", "POST"] )
def inventoryadd():
    if request.method == "GET":
        return render_template('inventoryadd.html')
   
    if request.method == "POST":
        itemNum = request.form.get("itemNum")
        itemName = request.form.get("itemName")
        description = request.form.get("description")
        location = request.form.get("location")

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        add_inventory = cur.execute("""
        INSERT INTO inventory (id, itemName, description, location) 
        VALUES (?, ?, ?, ?)""",(itemNum, itemName, description, location))
        conn.commit()
        conn.close()
        return redirect("/inventory")

@app.route('/orders/update/<int:id>', methods=["GET","POST"] )
def orderUpdate(id):
    if request.method == "GET":
        conn = get_db_connection()
        orders = conn.execute("SELECT * FROM orders WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('orderupdate.html', orders=orders)
    if request.method == "POST":
        orderIP = id
        customer = request.form.get("customer")
        item = request.form.get("item")
        total = request.form.get("total")
        status = request.form.get("status")
        #DB Connection
        conn = get_db_connection()
        dbexe = """UPDATE orders SET customer='{}', item='{}', total='{}', status='{}' WHERE id={}""".format(customer, item, total, status, id)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/orders')

@app.route('/orders/remove/<int:id>', methods=["GET","POST"] )
def orderRemove(id):
    if request.method == "GET":
        conn = get_db_connection()
        orders = conn.execute("SELECT * FROM orders WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('orderremove.html', orders=orders)
    #DB Connection
    if request.method == "POST":
        userID = id
        conn = get_db_connection()
        dbexe = """DELETE FROM orders WHERE id = {}""".format(userID)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/orders')

if __name__ == '__main__':
    app.run(debug=True)