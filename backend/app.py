from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired
import pymysql
import bcrypt
import db_info

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False     
app.config["SESSION_TYPE"] = "filesystem"     
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
csrf = CSRFProtect(app)  
Session(app)    

# create db connecion
connection = pymysql.connect(host=db_info.data["HOST"], port=db_info.data["PORT"], 
user=db_info.data["USER"], password=db_info.data["PASSWORD"], database=db_info.data["DBNIMI"])
cursor = connection.cursor()

# csrf protected form
class LoginForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired()])
    Pword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_drink_form(FlaskForm):
    juoma = StringField('juoma', validators=[DataRequired()])
    hinta = IntegerField('hinta', validators=[DataRequired()])
    tyyppi = SelectField('tyyppi',  
        choices=[
            ('kylmajuoma', 'kylmajuoma'),
            ('kuumajuoma', 'kuumajuoma'),
        ], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

class add_food_form(FlaskForm):
    ruokalaji = StringField('ruokalaji', validators=[DataRequired()])
    ruoka = StringField('ruoka', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    hinta = IntegerField('hinta', validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_lounas_form(FlaskForm):
    ruoka = StringField('ruoka', validators=[DataRequired()])
    paivamaara = DateField('paivamaara', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    juomat = StringField('juomat', validators=[DataRequired()])               
    submit = SubmitField('Submit')

class poista_drink_form(FlaskForm):
    juomat = SelectField('Poista juoma',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

class poista_ruoka_form(FlaskForm):
    ruoka = SelectField('Poista ruoka',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

class poista_lounas_form(FlaskForm):
    lounas = SelectField('Poista lounas',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

# login page
@app.route('/', methods=['GET', 'POST'])
def login():
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
    addlounasfood = add_lounas_form()
    msg_d = request.args.get("errorD", "")
    msg_f = request.args.get("errorF", "")
    msg_l = request.args.get("errorL", "")
    return render_template("add.html", adddrink=adddrink, addfood=addfood, addlounasfood=addlounasfood, msg_d=msg_d, msg_f=msg_f, msg_l=msg_l)

@app.route('/add_hot_drink', methods=['GET', 'POST'])
def add_drink():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            juoma = request.form.get("juoma")
            hinta = request.form.get("hinta")
            tyyppi = request.form.get("tyyppi")
        cursor.execute("INSERT INTO juomat (juoma, hinta, tyyppi)  VALUES (%s, %s, %s)", (juoma, hinta, tyyppi))
        connection.commit()
        errorD = "Lisätty onnistuneesti"
    except Exception:
        errorD = "Jokin meni pieleen"
    return redirect(url_for("add", errorD=errorD))

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            ruokalaji = request.form.get("ruokalaji")
            ruoka = request.form.get("ruoka")
            ainekset = request.form.get("ainekset")
            hinta = request.form.get("hinta")
        cursor.execute("INSERT INTO ruokamenu (ruokalaji, ruoka, ainekset, hinta, tyyppi)  VALUES (%s, %s, %s, %s)", (ruokalaji, ruoka, ainekset, hinta))
        connection.commit()
        errorF = "Lisätty onnistuneesti"
    except Exception:
        errorF = "Jokin meni pieleen"
    return redirect(url_for("add", errorF=errorF))

@app.route('/add_lounas_food', methods=['GET', 'POST'])
def add_lounas_food():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            ruoka = request.form.get("ruoka")
            paivamaara = request.form.get("paivamaara")
            ainekset = request.form.get("ainekset")
            juomat = request.form.get("juomat")
        cursor.execute("INSERT INTO viikonlounasRuokamenu (ruoka, paivamaara, ainekset, juomat)  VALUES (%s, %s, %s, %s)", (ruoka, paivamaara, ainekset, juomat))
        connection.commit()
        errorL = "Lisätty onnistuneesti"
    except Exception:
        errorL = "Jokin meni pieleen"
    return redirect(url_for("add", errorL=errorL))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        cursor.execute("SELECT id, juoma, hinta FROM juomat")
        getDataJuoma = cursor.fetchall()
        poista_drink = poista_drink_form()
        poista_drink.juomat.choices = [
            (str(id), f"{id}, {juoma}, {hinta}")
            for id, juoma, hinta in getDataJuoma
        ]
        cursor.execute("SELECT id, ruoka FROM ruokamenu")
        getDataRuoka = cursor.fetchall()
        poista_Ruoka = poista_ruoka_form()
        poista_Ruoka.ruoka.choices = [
            (str(id), f"{id}, {ruoka}")
            for id, ruoka in getDataRuoka
        ]
        cursor.execute("SELECT id, ruoka, paivamaara FROM viikonlounasruokamenu")
        getDataLounas = cursor.fetchall()
        poista_Lounas = poista_lounas_form()
        poista_Lounas.lounas.choices = [
            (str(id), f"{id}, {ruoka}, {paivamaara}")
            for id, ruoka, paivamaara in getDataLounas
        ]
    except Exception:
        pass
    msg_d_d = request.args.get("msg_d_d", "")
    msg_r_d = request.args.get("msg_r_d", "")
    msg_l_d = request.args.get("msg_l_d", "")
    return render_template("delete.html",  poista_drink=poista_drink, poista_Ruoka=poista_Ruoka, poista_Lounas=poista_Lounas, msg_d_d=msg_d_d, msg_r_d=msg_r_d, msg_l_d=msg_l_d)

@app.route('/delete_drink', methods=['GET', 'POST'])
def delete_drink():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            juomat = request.form.get("juomat")
            print(juomat)
            cursor.execute(f"DELETE FROM juomat WHERE id='{juomat}';")
            connection.commit()
            msg_d_d = "Poistettu onnistuneesti"
    except Exception:
        msg_d_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_d_d=msg_d_d))

@app.route('/delete_ruoka', methods=['GET', 'POST'])
def delete_ruoka():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            ruoka = request.form.get("ruoka")
            print(ruoka)
            cursor.execute(f"DELETE FROM ruokamenu WHERE id='{ruoka}';")
            connection.commit()
            msg_r_d = "Poistettu onnistuneesti"
    except Exception:
        msg_r_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_r_d=msg_r_d))

@app.route('/delete_lounas', methods=['GET', 'POST'])
def delete_lounas():
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            lounas = request.form.get("lounas")
            print(lounas)
            cursor.execute(f"DELETE FROM viikonlounasruokamenu WHERE id='{lounas}';")
            connection.commit()
            msg_l_d = "Poistettu onnistuneesti"
    except Exception:
        msg_l_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_l_d=msg_l_d))

@app.route("/logout")
def logout():
    session["Username"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run()
