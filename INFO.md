# Cafeteria Menu Display

- admin can add new thing to the menus.
- user display is just basic cafeteria menu displays gets the data from db.

--------------------------------------------------------------------------------

- page 1: buffet
- page 2: food menu and kids menu
- page 3: drinks menus
- page 4: open hours

## teknologias:
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

## Project structure:
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

####        tarjoukset
    id, ruoka, juoma, hinta

####    BACKEND(admin):
- app.py the backend application
- create_db.py can create the db using this includes all basic information about the cafeteria
- db_info.py information that needed to connect the db        
####    FRONDEND(user site):
- index.php the menu display
- connect_dp.php create the connection to db
- pages includes all the menu pages