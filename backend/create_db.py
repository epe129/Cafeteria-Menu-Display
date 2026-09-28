"""
Luodaan tietokanta ja taulut.
pymysql avulla yhdistää tietokantaan.
db_infosta saa databasen yhdistämiseen tarvittavat tiedot.
"""
import pymysql
import db_info

def databasen_luonti():
    """
    Luodaan itse tietokanta jos ei ole olemassa.
    """
    connection_luonti = pymysql.connect(host=db_info.data["HOST"], port=db_info.data["PORT"],
    user=db_info.data["USER"], password=db_info.data["PASSWORD"])
    cursor_luonti = connection_luonti.cursor()
    cursor_luonti.execute("CREATE DATABASE IF NOT EXISTS cafeteriaMenu")

# luodaan yhteys
try:
    databasen_luonti()
    connection = pymysql.connect(host=db_info.data["HOST"], port=db_info.data["PORT"],
    user=db_info.data["USER"], password=db_info.data["PASSWORD"], database=db_info.data["DBNIMI"])
    cursor = connection.cursor()
except ImportError:
    print("Yhteyden luominen epäonnistui")

def db():
    """
    luodaan tietokannan taulut sekä lisätään arvoja.
    """
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS admin "
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, username VARCHAR(45) NOT NULL, pword VARCHAR(255) NOT NULL);")
 
        cursor.execute("CREATE TABLE IF NOT EXISTS viikonBuffetRuokamenu"
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, ruoka VARCHAR(250), paivamaara date, ainekset VARCHAR(250), juomat VARCHAR(250));")
 
        cursor.execute("CREATE TABLE IF NOT EXISTS ruokamenu"
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, ruokalaji VARCHAR(250), ruoka VARCHAR(250), ainekset VARCHAR(250), hinta int);")
 
        cursor.execute("CREATE TABLE IF NOT EXISTS juomat"
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, juoma VARCHAR(250), hinta int, tyyppi VARCHAR(250));")
 
        cursor.execute("CREATE TABLE IF NOT EXISTS aukioloajat"
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, paiva VARCHAR(250), kellonaika VARCHAR(250), paivamaara datetime);")
 
        cursor.execute("CREATE TABLE IF NOT EXISTS tarjoukset"
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, ruoka VARCHAR(250), juoma VARCHAR(250), hinta int);")                          
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("ma", "9-21", "2026-10-05")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("ti", "9-21", "2026-10-06")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("ke", "9-21", "2026-10-07")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("to", "9-21", "2026-10-08")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("pe", "10-21", "2026-10-09")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("la", "8-21", "2026-10-10")')
        cursor.execute(f'INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) VALUES ("su", "suljettu", "2026-10-11")')
        
        cursor.connection.commit()       
    except ImportError:
        print("Taulukon luominen epäonnistui")
db()