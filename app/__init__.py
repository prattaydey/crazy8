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
import time
from deck import *

app = Flask(__name__)               #create Flask object
app.secret_key = os.urandom(32)     #randomized string for SECRET KEY (for interacting with operating system)

DB_FILE="tables.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("create table if not exists accounts(username text, password text);")
c.execute("create table if not exists stats(id int, won int, lost int);")
db.commit()


# checks to see if the user already has a session
@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        print("user is logged in as " + session['username'] + ". Redirecting to /main")
        return redirect("/main")

    print("user is not logged in. Redirecting to /login")
    return redirect("/login")

# REGISTER
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Already logged in
    if 'username' in session:
        print("user is logged in as " + session['username'] + " is already logged in. Redirecting to /main")
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
        print("user is logged in as " + session['username'] + " is already logged in. Redirecting to /main")
        return redirect("/main")

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
    print("user has logged out. Redirecting to /login")
    return redirect("/login")

# <------------------------------------- END OF LOGIN / REGISTER ------------------------------------->
# renders the cool loading page 
@app.route("/loadings", methods=['GET', 'POST'])
def loadings():
    return render_template('loading.html')

# the main page where we can make custom rooms and stuff!
@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == "POST" and 'room_name' in request.form:
        #create a room
        room_name = request.form['room_name']
        deck_id = create_deck()
        setup(deck_id)
        upload_deck_id(deck_id, room_name)
        print("created room " + room_name + " with id " + deck_id)

        #create a counter
        requests.get(f"https://api.countapi.xyz/{deck_id}").json()
        requests.get(f"https://api.countapi.xyz/hit/{deck_id}")
        print("created a counter at " + f"https://api.countapi.xyz/get/{deck_id}")

        # get a dictionary of all the rooms
        rooms = get_rooms()
        # tell the dictionary that it's a dictionary
        room_dict = dict(rooms[deck_id])
        # add the counter url
        room_dict.update( {"counter" : f"https://api.countapi.xyz/{deck_id}"})
        # replace the current definition for deck_id with the modified one
        rooms[deck_id] = room_dict

        # upload the data
        rooms = json.dumps(rooms)
        url = f"https://jsonblob.com/api/room/{blobId}"
        requests.put(url, data=rooms)

    if 'username' in session:
        # returns a dictionary
        rooms = get_rooms()
        # tell the variable that it is a dictionary
        rooms = dict(rooms)
        # returns a list of deck ids
        ids = rooms.keys()

        return render_template('main.html', room_names=rooms, ids=ids)
    else:
        print("user is not logged in. Redirecting to /login")
        return redirect("/login")
        
#how to remove a player from the room
@app.route("/leave", methods=["POST"])
def leave():
    if not 'username' in session:
        print("user is not logged in. Redirecting to /login")
        return redirect("/login")
    print("removing player from room")
    remove_player(request.form['deck_id'], session['username'])
    print("Redirecting to /main")
    return redirect("/main")
        
# starts up the room
@app.route("/connect-<deck_id>", methods=['GET', 'POST'])
def connect(deck_id):
    if not 'username' in session:
        print("user is not logged in. Redirecting to /login")
        return redirect('/login')

    room = get_rooms()[deck_id]

    # if the player trying to join the room has already entered the room previously, then let them in, but don't add their name again
    usernames = room.values()
    if session['username'] in usernames:
        if 'player1' in room and room['player1'] == session['username']:
            my_hand = get_pile(deck_id, "player1")
            opponents_hand = get_pile(deck_id, "player2")
        elif 'player2' in room and room['player2'] == session['username']:
            my_hand = get_pile(deck_id, "player2")
            opponents_hand = get_pile(deck_id, "player1")

    # for players entering the room for the first time
    else:
        add_player(deck_id, session['username'])
        if not 'player1' in room:
            my_hand = get_pile(deck_id, "player1")
            opponents_hand = get_pile(deck_id, "player2")
        elif not 'player2' in room:
            my_hand = get_pile(deck_id, "player2")
            opponents_hand = get_pile(deck_id, "player1")
        else:
            return "this room is full :(" 

    cards_in_play = get_pile(deck_id, "play")
    current_card = cards_in_play[len(cards_in_play) - 1]

    cards_remaining = remaining_in_deck(deck_id)

    if 'error' in session:
        error_message = session['error']
        session.pop('error')
    else:
        error_message = ""

    msg = ""

    # count api for win/lose
    #winning and losing
    if len(my_hand) == 0:
        #count api stuff
        c.execute("UPDATE stats SET won=? WHERE id=?", )
        msg = "Congrats, you win!"
    elif len(opponents_hand) == 0:
        #count api stuff
        c.execute("UPDATE stats SET won=? WHERE id=?", )
        msg = "Aw shucks, you loose"
    elif cards_remaining == 0:
        reshuffle_deck(deck_id)

    return render_template("crazy8.html", my_hand=my_hand, opponents_hand=opponents_hand, card_in_play=current_card, deck_id=deck_id, cards_remaining=cards_remaining, error_message=error_message, msg=msg)
    
@app.route("/draw-<deck_id>", methods=["GET"])
def draw(deck_id):
    if 'username' not in session:
        return redirect("/login")

    if which_player(deck_id, session) == "player1":
        # player 1 goes on odd values
        if get_counter_value(deck_id) % 2 == 0:
            session['error'] = "It is not your turn"
            return redirect(f"/connect-{deck_id}")
    elif which_player(deck_id, session) == "player2":
        # player 2 goes on even values
        if get_counter_value(deck_id) % 2 == 1:
            session['error'] = "It is not your turn"
            return redirect(f"/connect-{deck_id}")

    me = which_player(deck_id, session)
    card_drawn = draw_from_deck(deck_id)['code']
    add_to_pile(me, deck_id, card_drawn)
    increment_counter(deck_id)
    return redirect(f"/connect-{deck_id}")

#playing the game
#Potential use of this, we can get the list of rooms, run through them
#The first room with an empty spot, the player will join
#parameters = list of rooms
#goal: player will join random room with empty spot. If none available, go to waiting list
@app.route("/<deck_id>/play", methods=['POST'])
def play(deck_id):
    if request.method == "POST":
        if which_player(deck_id, session) == "player1":
            # player 1 goes on odd values
            if get_counter_value(deck_id) % 2 == 0:
                session['error'] = "It is not your turn"
                return redirect(f"/connect-{deck_id}")
        elif which_player(deck_id, session) == "player2":
            # player 2 goes on even values
            if get_counter_value(deck_id) % 2 == 1:
                session['error'] = "It is not your turn"
                return redirect(f"/connect-{deck_id}")

        # current card is a dictionary but its type is a string
        current_card = request.form["current_card"]
        print("current card: " + current_card)

        # json.loads() requires things to be enclosed in double quotes
        current_card = current_card.replace("'", '"')
        current_card = json.loads(current_card)

        if not card_check(deck_id, current_card):
            session['error'] = "You cannot play that card"
        else:
            increment_counter(deck_id)

    return redirect(f"/connect-{deck_id}")
    #return render_template("crazy8.html", my_hand=my_hand, opponents_hand=opponents_hand, card_in_play=card_in_play, deck_id=deck_id) #redirect('/connect-<deck_id>', code=307)

#To be used after Player presses play button and there are no avalible rooms
@app.route("/waiting", methods=['POST'])
def waiting():
    room_list = get_rooms()
    for id in room_list:
        deck_id = id #deck_id now equal to the deck id of one of the rooms
        room = room_list[deck_id] #room now equal to dictionary containing player one and player two
        
        # If there is an empty slot, redirect to connect to that room
        if (not 'player1' in room) or (not 'player2' in room):
            return redirect(f"/connect-{deck_id}")

    # get sent to the waiting room
    return render_template("loading.html")


# page with the game
# No idea what to do with this
@app.route("/crazy8", methods=['GET', 'POST'])
def crazy8():
    deckID = create_deck()
    # pileID = ret_pile_name()
    setup(deckID)
    hand1 = get_pile(deckID, "player1")
    hand2 = get_pile(deckID, "player2")
    card_in_play = get_pile(deckID, "play")[len(card_in_play)-1]
    # draw_from_pile(deckID, hand1)

    return render_template('crazy8.html', opponents_hand=hand1, my_hand=hand2, card_in_play=card_in_play)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

db.commit() #save changes
db.close()  #close database

