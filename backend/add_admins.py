"""
This script allows you to add new admin users to the blog platform database.
Make sure to run this script in a secure environment, 
as it will prompt you for the new admin's username and password."""
import pymysql
import bcrypt

connection = pymysql.connect(host="localhost", port=3306, user="root", password="", database="cafeteriaMenu")
cursor = connection.cursor()

def add_admin(username, password):
    """
    Add a new admin to the database.
    """
    cursor.execute("INSERT INTO admin (username, pword) VALUES (%s, %s)", (username, password))
    connection.commit()
    print(f"Admin '{username}' added successfully.")

if __name__ == "__main__":
    new_admin_username = input("Enter the new admin's username: ")
    new_admin_password = input("Enter the new admin's password: ")
    hashed_password = bcrypt.hashpw(new_admin_password.encode('utf-8'), bcrypt.gensalt())
    add_admin(new_admin_username, hashed_password)