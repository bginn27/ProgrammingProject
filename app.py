from fileinput import close
import re
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
        dbexe = """UPDATE inventory SET itemName='{}', description='{}', location='{}' WHERE id={}""".format(itemName, description, location,itemNum)
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




# invoices page
@app.route('/invoices', methods=["GET", "POST"])
def invoices():
    if request.method == "GET":
        return render_template('invoices.html')




if __name__ == '__main__':
    app.run(debug=True)