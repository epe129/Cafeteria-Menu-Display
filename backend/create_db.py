"""
Luodaan tietokanta ja taulut.
pymysql avulla yhdistää tietokantaan.
db_infosta saa databasen yhdistämiseen tarvittavat tiedot.
"""
from datetime import date, timedelta

import pymysql

def databasen_luonti():
    """
    Luodaan itse tietokanta jos ei ole olemassa.
    """
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="",
    )
    try:
        with connection.cursor() as cursor:
            database_name = "cafeteriamenudisplay"
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
    finally:
        connection.close()

def db():
    """
    luodaan tietokannan taulut sekä lisätään arvoja.
    """
    databasen_luonti()
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="cafeteriamenudisplay",
        charset="utf8mb4",
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS admin ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "username VARCHAR(45) NOT NULL, "
                "pword VARCHAR(255) NOT NULL, "
                "CONSTRAINT uq_admin_username UNIQUE (username)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS viikonlounasRuokamenu ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "ruoka VARCHAR(250) NOT NULL, "
                "paivamaara DATE NOT NULL, "
                "ainekset TEXT NOT NULL, "
                "juomat TEXT NOT NULL"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS ruokamenu ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "ruokalaji VARCHAR(250) NOT NULL, "
                "ruoka VARCHAR(250) NOT NULL, "
                "ainekset TEXT NOT NULL, "
                "hinta DECIMAL(6, 2) NOT NULL"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS juomat ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "juoma VARCHAR(250) NOT NULL, "
                "hinta DECIMAL(6, 2) NOT NULL, "
                "tyyppi VARCHAR(250) NOT NULL"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS aukioloajat ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "paiva VARCHAR(20) NOT NULL, "
                "kellonaika VARCHAR(50) NOT NULL, "
                "paivamaara DATE NOT NULL"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            )

            weekday_names = ("ma", "ti", "ke", "to", "pe", "la", "su")
            weekday_hours = ("9-21", "9-21", "9-21", "9-21", "10-21", "8-21", "suljettu")
            today = date.today()
            for day_offset in range(7):
                opening_date = today + timedelta(days=day_offset)
                weekday = opening_date.weekday()
                cursor.execute(
                    "SELECT 1 FROM aukioloajat WHERE paivamaara = %s LIMIT 1",
                    (opening_date,),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO aukioloajat (paiva, kellonaika, paivamaara) "
                        "VALUES (%s, %s, %s)",
                        (weekday_names[weekday], weekday_hours[weekday], opening_date),
                    )

        connection.commit()
    finally:
        connection.close()
        
db()
