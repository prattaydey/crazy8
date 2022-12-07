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
