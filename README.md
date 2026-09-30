# Cafeteria Menu Display

Page where user can see the cafeteria menu in slide show.
Admin have a login and admin can add and delete values from database.

## Teknologias: 

### DATABASE:
- SQL
### BACKEND:
- Flask
- python
- python libraries
### FRONDEND:
- php

## Install requirements to python
    pip install -r requirements.txt

--------------------------------------------------------------------------------

###    BACKEND:
- app.py the backend application
- create_db.py can create the db using this includes all basic information about the cafeteria
- db_info.py information that needed to connect the db        

### Connect python app to database 
file name: db_info.py

    data = {
        "USER":'esimnerkki',
        "PASSWORD":'esimnerkki',
        "DBNIMI": 'esimnerkki',
        "PORT": 1234,
        "HOST": '123.1.2.3',
    } 

### Flask ohjelma:
    flask run --debug

###    FRONDEND:
- index.php the menu display
- connect_dp.php create the connection to db

--------------------------------------------------------------------------------

###    SQL DATABSE

#### admin
    id, username, pword

#### viikon Buffet Ruokamenu
    id, ruoka, paivamaara, ainekset, juomat

####        ruoka menu
    id, ruokalaji, ruoka, ainekset, hinta

####        juomat
    id, juoma, hinta, tyyppi

####        aukioloajat
    id, paiva, kellonaika, paivamaara


## Sivu

### page url when you host it localy: 
    http://localhost/CafeteriaMenuDisplay/frondend/index.php
