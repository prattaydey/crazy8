# p1_AdorableMachoElephants
## to-do:
- make a way to interact with cards
- make a way to create rooms
- display opponent's hand face down
- incorporate count api for stats
- establish a turn order
- make a way to ensure they dont try to put down the wrong card (ie 2D on 5H)
- a way to determine win/lose and update stats accordingly
    - if the pile rusns out of cards, you win 
- Extr stuff
    * Powerups
    * chat system
    * a timer to prevent users from stalling

## Roster and Roles:
Prattay Dey:  Project Manager  
Kevin Li:  Devo  
Joseph Wu:  Devo  
Anjini Katari:  Devo
## Summary:
A recreation of Crazy 8s / Uno with the ability to play with other users. You can create and join games on the main page, which displays the same list of rooms to all users on the site

## API Cards:
Deck of Cards: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_deck_of_cards.md  
Count: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_CountAPI.md  
jsonblob: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_jsonblob.md

## Launch Codes:
Clone the repo into your local machine
```
HTTPS: $ git clone https://github.com/prattaydey/p1_AdorableMachoElephants.git
SSH: $ git clone git@github.com:prattaydey/p1_AdorableMachoElephants.git
```
Create and activate a virtual environment
```
$ python3 -m venv <VENV_NAME>
```
Enter the repo
```
$ cd p1_AdorableMachoElephants
```
Install all required elements
```
$ pip install -r requirements.txt
```
Start the Flask server
```
$ python3 app/__init__.py
```
Navigate to the URL on your browser
```
http://127.0.0.1:5000
```
