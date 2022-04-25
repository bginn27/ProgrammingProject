from ast import And
from fileinput import close
from operator import and_
import re
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash, session
from sqlalchemy import false
# from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = 'SecretKey'

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
        username = request.form.get("username")
        password = request.form.get("password")
        #Get record for user from DB
        conn = get_db_connection()
        dbexe = 'SELECT username, password FROM users WHERE username="{}"'.format(username)
        print(dbexe)
        login = conn.execute(dbexe).fetchall()
        conn.close()

        if username.lower() == login[0][0].lower() and password == login[0][1]:
            print('Success!')
            session['user'] = username
            return render_template('home.html') 
        else:
            print('Bad Username and/or Password!')
            flash('Bad Username and/or Password!')
            return redirect("/login")

# logout page
@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')



# home page
@app.route('/')
def home():
    if('user' in session):
        return render_template('home.html')
    else:
        return redirect('/login')




# main inventory page
@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    inventory = conn.execute("SELECT * FROM inventory").fetchall()
    conn.close()
    return render_template('inventory.html', inventory=inventory)
      

# add info to table and return to main inventory page
@app.route('/inventoryadd', methods=["GET", "POST"] )
def inventoryadd():
    if request.method == "GET":
        return render_template('inventoryadd.html')
   
    if request.method == "POST":
        itemID = request.form.get("itemID")
        itemName = request.form.get("itemName")
        description = request.form.get("description")
        quantity = request.form.get("quantity")
        location = request.form.get("location")
        print(itemID)
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        add_inventory = cur.execute("""
        INSERT INTO inventory (id, itemName, description, quantity, location) 
        VALUES (?, ?, ?, ?, ?)""",(itemID, itemName, description, quantity, location))
        conn.commit()
        conn.close()
        return redirect("/inventory")


@app.route('/inventory/update/<int:id>', methods=["GET","POST"] )
def inventoryUpdate(id):
    if request.method == "GET":
        conn = get_db_connection()
        inventory = conn.execute("SELECT * FROM inventory WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('inventoryupdate.html', inventory=inventory)
    if request.method == "POST":
        itemNum = id
        itemName = request.form.get("itemName")
        description = request.form.get("description")
        location = request.form.get("location")
        #DB Connection
        conn = get_db_connection()
        dbexe = """UPDATE inventory SET itemName='{}', description='{}', quantity='{}', location='{}', updated=CURRENT_TIMESTAMP WHERE id={}""".format(itemName, description, quantity, location, itemNum)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/inventory')



@app.route('/inventory/remove/<int:id>', methods=["GET","POST"] )
def inventoryRemove(id):
    if request.method == "GET":
        conn = get_db_connection()
        inventory = conn.execute("SELECT * FROM inventory WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('inventoryremove.html', inventory=inventory)
    #DB Connection
    if request.method == "POST":
        itemNum = id
        conn = get_db_connection()
        dbexe = """DELETE FROM inventory WHERE id = {}""".format(itemNum)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/inventory')



# main users page
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('users.html', users=users)

# add user to table and return to main inventory page
@app.route('/useradd', methods=["GET", "POST"] )
def useradd():
    if request.method == "GET":
        return render_template('useradd.html')
   
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        add_users = cur.execute("""
        INSERT INTO users (username,password) 
        VALUES (?, ?)""",(username, password))
        conn.commit()
        conn.close()
        return redirect("/users")

@app.route('/users/update/<int:id>', methods=["GET","POST"] )
def userUpdate(id):
    if request.method == "GET":
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM users WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('userupdate.html', users=users)
    if request.method == "POST":
        userID = id
        username = request.form.get("username")
        password = request.form.get("password")
        #DB Connection
        conn = get_db_connection()
        dbexe = """UPDATE users SET username='{}', password='{}' WHERE id={}""".format(username, password, id)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/users')

@app.route('/users/remove/<int:id>', methods=["GET","POST"] )
def userRemove(id):
    if request.method == "GET":
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM users WHERE id={}".format(id)).fetchall()
        conn.close()
        return render_template('userremove.html', users=users)
    #DB Connection
    if request.method == "POST":
        userID = id
        conn = get_db_connection()
        dbexe = """DELETE FROM users WHERE id = {}""".format(userID)
        print(dbexe)
        db_update = conn.execute(dbexe)
        conn.commit()
        conn.close()
        return redirect('/users')



# main orders page
@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

# add user to table and return to main inventory page
@app.route('/orderadd', methods=["GET", "POST"] )
def orderadd():
    if request.method == "GET":
        return render_template('orderadd.html')
   
    if request.method == "POST":
        customer = request.form.get("customer")
        item = request.form.get("item")
        total = request.form.get("total")
       
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        add_orders = cur.execute("""
        INSERT INTO orders (customer,item,total,status) 
        VALUES (?, ?, ?, ?)""",(customer, item, total, 'NEW'))
        conn.commit()
        conn.close()
        return redirect("/orders")

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