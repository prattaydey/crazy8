# Adorable Macho Elephants: Prattay, Joseph, Kevin, Anjini
# SoftDev
# Period 07
# Dec 2022

import sqlite3                      #for database building
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate user sessions
from flask import redirect, url_for #to redirect to a different URL
import os

app = Flask(__name__)               #create Flask object
app.secret_key = os.urandom(32)     #randomized string for SECRET KEY (for interacting with operating system)

DB_FILE="tables.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("create table if not exists accounts(username text, password text);")
db.commit()


# checks to see if the user already has a session
@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect("/main")
    return redirect("/login")

# REGISTER
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Already logged in
    if 'username' in session:
        return redirect("/main")
    
    # GET
    if request.method == 'GET':
        return render_template('register.html')

    # POST
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        input_confirm_password = request.form['confirm password']

    # if no registration info is inputted into the fields
    if input_username.strip() == '' or input_password.strip() == '' or input_confirm_password.strip() == '':
        error_msg = ""
        if input_username == '':
            error_msg += "Please enter a username. \n"

        if input_password == '':
            error_msg += "Please enter a password. \n"

        if input_confirm_password == '':
            error_msg += "Please confirm your password. \n"

        return render_template('register.html', message = error_msg)
        
    # if info is entered into fields
    else:
        # Checks for password/confirm password match
        if input_password != input_confirm_password:
            return render_template('register.html', message = "Passwords do not match. Please try again.")

        # Checks for existing username in accounts table
        var = (input_username,)
        c.execute("select username from accounts where username=?", var)

        # if there isn't an account associated with said username then create one
        if not c.fetchone():
            c.execute("insert into accounts values(?, ?)", (input_username, input_password))
            return render_template('login.html')
        # if username is already taken
        else:
            return render_template('register.html', message = "Username is already taken. Please select another username.")

# login process
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Already logged in
    if 'username' in session:
        app.redirect("/main")

    # GET
    if request.method == "GET":
        return render_template("login.html")

    # POST
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

    # Searches accounts table for user-password combination
    c.execute("select username from accounts where username=? and password=?;", (input_username, input_password))

    # login_check
    if c.fetchone():
        print("Login success!")
        if request.method == 'GET': #For 'get'
            session['username'] = request.args['username'] # stores username in session

        if request.method == 'POST': #For 'post'
            session['username'] = request.form['username'] # stores username in session

        return redirect("/main")

    else:
        print("Login failed")
        error_msg = ''
        username_check = "select username from accounts where username=?;"
        password_check = "select username from accounts where password=?;"

        # Username check
        c.execute(username_check, (input_username,))
        if not c.fetchone():
            error_msg += "Username is incorrect or not found. \n"

        #Password check
        c.execute(password_check, (input_password,))
        if not c.fetchone():
            error_msg += "Password is incorrect or not found. \n"

        error_msg += "Please try again."
        return render_template('login.html', message = error_msg)


# logout and redirect to login page
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect("/login")


@app.route("/loadings", methods=['GET', 'POST'])
def loadings():
    return render_template('loading.html')


@app.route("/main", methods=['GET', 'POST'])
def main():
    if 'username' in session:
        return render_template('main.html')
    else:
        return redirect("/login")
# <------------------------------------- END OF LOGIN / REGISTER ------------------------------------->

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

db.commit() #save changes
db.close()  #close database

