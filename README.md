# Cafeteria Menu Display

Pages where user can see the cafeteria menu in slide show.
Admin have a login and admin can add and delete the database values.


## Teknologias: 

### DATABASE:
- SQL
- XAMPP
- phpMyadmin
### BACKEND:
- Flask
- python
- python libraries
### FRONDEND:
- php

## Install requirements
    pip install -r requirements.txt

--------------------------------------------------------------------------------

###    BACKEND:
- app.py the backend application
- create_db.py can create the db using this includes all basic information about the cafeteria
- db_info.py information that needed to connect the db        
###    FRONDEND:
- index.php the menu display
- connect_dp.php create the connection to db
- pages includes all the menu pages

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
