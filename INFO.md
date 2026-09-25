# Cafeteria Menu Display

- admin can add new thing to the menus.
- user display is just basic cafeteria menu displays gets the data from db.

pade 1: buffet
page 2: food menu and kids menu
page 3: drinks menus


## Project structure:
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

####    BACKEND(admin):
- app.py the backend application
- create_db.py can create the db using this includes all basic information about the cafeteria
- db_info.py information that needed to connect the db        
####    FRONDEND(user site):
- index.php the menu display
- connect_dp.php create the connection to db
