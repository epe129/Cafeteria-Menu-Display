# Cafeteria Menu Display

Pages where user can see the cafeteria menu in slide show.
Admin have a login and admin can add, delete and change the database values.


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
    id, paiva, ruoka, paivamaara

#### viikon Buffet Ruokajuomat
    Buffetid, juoma

####        ruoka menu
    id, ruokalaji, ruoka, hinta

####        lasten menu
    id, ruokalaji, ruoka, hinta

####        kylmätjuoma
    id, juoma, hinta

####       kuumatjuoma
    id, juoma, hinta

####        aukioloajat
    id, paiva, kellonaika, paivamaara

####        tarjoukset
    id, ruoka, juoma, hinta

--------------------------------------------------------------------------------

![alt text](/dbkuva.png)