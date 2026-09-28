from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired
import pymysql
import bcrypt
import db_info

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False     
app.config["SESSION_TYPE"] = "filesystem"     
csrf = CSRFProtect(app)  
Session(app)

# create db connecion
connection = pymysql.connect(host=db_info.data["HOST"], port=db_info.data["PORT"], user=db_info.data["USER"], password=db_info.data["PASSWORD"], database=db_info.data["DBNIMI"])
cursor = connection.cursor()

# csrf protected form
class LoginForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired()])
    Pword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_drink(FlaskForm):
    juoma = StringField('juoma', validators=[DataRequired()])
    hinta = IntegerField('hinta', validators=[DataRequired()])
    tyyppi = StringField('tyyppi', validators=[DataRequired()])
    submit = SubmitField('Submit')

# login page
@app.route('/', methods=['GET', 'POST'])
def login():
    text = ""
    form = LoginForm()
    # handles the login
    if request.method == 'POST':
        if form.validate_on_submit():
            Username = form.Username.data
            Pword = form.Pword.data
            print(Username)
            cursor.execute(f"SELECT username, pword FROM admin WHERE username='{Username}'")
            getData = cursor.fetchall()
            if Pword is not None and getData:
                if bcrypt.checkpw(Pword.encode('utf8'), getData[0][1].encode('utf8')):
                    print("correct")
                    session["Username"] = getData[0][0]
                    return redirect("/add")
                else:
                    text="Username or password is wrong"
                    return render_template("login.html", form=form, text=text)
            else:
                text="Username or password is wrong"
                return render_template("login.html", form=form, text=text)
        else:
            text="bad request"
            return render_template("login.html", form=form, text=text)
    return render_template("login.html", form=form)

# admin page
@app.route('/add', methods=['GET', 'POST'])
def add():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    adddrink = add_drink()
    return render_template("add.html", adddrink=adddrink)

@app.route('/add_hot_drink', methods=['GET', 'POST'])
def add_hot_drink():
    if request.method == "POST":
        juoma = request.form.get("juoma")
        hinta = request.form.get("hinta")
        tyyppi = request.form.get("tyyppi")
    cursor.execute("INSERT INTO juomat (juoma, hinta, tyyppi)  VALUES (%s, %s, %s)", (juoma, hinta, tyyppi))
    connection.commit()
    return redirect("/add")

if __name__ == '__main__':
    app.run()
