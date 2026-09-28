from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
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

class add_drink_form(FlaskForm):
    juoma = StringField('juoma', validators=[DataRequired()])
    hinta = IntegerField('hinta', validators=[DataRequired()])
    tyyppi = StringField('tyyppi', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_food_form(FlaskForm):
    ruokalaji = StringField('ruokalaji', validators=[DataRequired()])
    ruoka = StringField('ruoka', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    hinta = IntegerField('hinta', validators=[DataRequired()])
    tyyppi = StringField('tyyppi', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_sale_form(FlaskForm):
    ruoka = StringField('ruoka', validators=[DataRequired()])
    juoma = StringField('juoma', validators=[DataRequired()])               
    hinta = IntegerField('hinta', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_buffetfood_form(FlaskForm):
    ruoka = StringField('ruoka', validators=[DataRequired()])
    paivamaara = DateField('paivamaara', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    submit = SubmitField('Submit')

class add_drinkbuffet_form(FlaskForm):
    juoma = StringField('juoma', validators=[DataRequired()])               
    paivamaara = DateField('paivamaara', validators=[DataRequired()])
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
    adddrink = add_drink_form()
    addfood = add_food_form()
    addsale = add_sale_form()
    addbuffetfood = add_buffetfood_form()
    addbuffetdrink = add_drinkbuffet_form()
    return render_template("add.html", adddrink=adddrink, addfood=addfood, addsale=addsale, addbuffetfood=addbuffetfood, addbuffetdrink=addbuffetdrink)

@app.route('/add_hot_drink', methods=['GET', 'POST'])
def add_drink():
    if request.method == "POST":
        juoma = request.form.get("juoma")
        hinta = request.form.get("hinta")
        tyyppi = request.form.get("tyyppi")
    cursor.execute("INSERT INTO juomat (juoma, hinta, tyyppi)  VALUES (%s, %s, %s)", (juoma, hinta, tyyppi))
    connection.commit()
    return redirect("/add")

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == "POST":
        ruokalaji = request.form.get("ruokalaji")
        ruoka = request.form.get("ruoka")
        ainekset = request.form.get("ainekset")
        hinta = request.form.get("hinta")
        tyyppi = request.form.get("tyyppi")
    cursor.execute("INSERT INTO ruokamenu (ruokalaji, ruoka, ainekset, hinta, tyyppi)  VALUES (%s, %s, %s, %s, %s)", (ruokalaji, ruoka, ainekset, hinta, tyyppi))
    connection.commit()
    return redirect("/add")

@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    if request.method == "POST":
        ruoka = request.form.get("ruoka")
        juoma = request.form.get("juoma")
        hinta = request.form.get("hinta")
    cursor.execute("INSERT INTO tarjoukset (ruoka, juoma, hinta)  VALUES (%s, %s, %s)", (ruoka, juoma, hinta))
    connection.commit()
    return redirect("/add")

@app.route('/add_buffet_food', methods=['GET', 'POST'])
def add_buffet_food():
    if request.method == "POST":
        ruoka = request.form.get("ruoka")
        paivamaara = request.form.get("paivamaara")
        ainekset = request.form.get("ainekset")

    cursor.execute("INSERT INTO viikonbuffetruokamenu (ruoka, paivamaara, ainekset)  VALUES (%s, %s, %s)", (ruoka, paivamaara, ainekset))
    connection.commit()
    return redirect("/add")

@app.route('/add_buffet_drink', methods=['GET', 'POST'])
def add_buffet_drink():
    if request.method == "POST":
        juoma = request.form.get("juoma")
        paivamaara = request.form.get("paivamaara")
    cursor.execute("INSERT INTO viikonbuffetruokajuomat (juoma, paivamaara)  VALUES (%s, %s)", (juoma, paivamaara))
    connection.commit()
    return redirect("/add")

if __name__ == '__main__':
    app.run()
