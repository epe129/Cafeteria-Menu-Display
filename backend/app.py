"""the application"""
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
    """log in form"""
    Username = StringField('Username', validators=[DataRequired()])
    Pword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddDrinkForm(FlaskForm):
    """form to juoma add"""
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

class AddFoodForm(FlaskForm):
    """form to ruoka add"""
    ruokalaji = StringField('ruokalaji', validators=[DataRequired()])
    ruoka = StringField('ruoka', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    hinta = IntegerField('hinta', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddLounasForm(FlaskForm):
    """form to lounas add"""
    ruoka = StringField('ruoka', validators=[DataRequired()])
    paivamaara = DateField('paivamaara', validators=[DataRequired()])
    ainekset = StringField('ainekset', validators=[DataRequired()])               
    juomat = StringField('juomat', validators=[DataRequired()])               
    submit = SubmitField('Submit')

class AddAikatauluForm(FlaskForm):
    """form to aikataulu add"""
    paiva = StringField('paiva', validators=[DataRequired()])
    paivamaara = DateField('paivamaara', validators=[DataRequired()])
    kellonaika = StringField('kellonaika', validators=[DataRequired()])               
    submit = SubmitField('Submit')

class PoistaDrinkForm(FlaskForm):
    """form to juoma deletion"""
    juomat = SelectField('Poista juoma',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

class PoistaRuokaForm(FlaskForm):
    """form to ruoka deletion"""
    ruoka = SelectField('Poista ruoka',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

class PoistaLounasForm(FlaskForm):
    """form to lounas deletion"""
    lounas = SelectField('Poista lounas',  
        choices=[], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

# login page
@app.route('/', methods=['GET', 'POST'])
def login():
    """the log in page and handles the log in"""
    form = LoginForm()
    # handles the login
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.Username.data
            pword = form.Pword.data
            cursor.execute(f"SELECT username, pword FROM admin WHERE username='{username}'")
            getdata = cursor.fetchall()
            if pword is not None and getdata:
                if bcrypt.checkpw(pword.encode('utf8'), getdata[0][1].encode('utf8')):
                    session["Username"] = getdata[0][0]
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
    """the add page"""
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    adddrink = AddDrinkForm()
    addfood = AddFoodForm()
    addlounasfood = AddLounasForm()
    addaikataulu = AddAikatauluForm()
    msg_d = request.args.get("error_d", "")
    msg_f = request.args.get("error_f", "")
    msg_l = request.args.get("error_l", "")
    msg_a = request.args.get("error_a", "")
    return render_template("add.html", adddrink=adddrink, addfood=addfood, addlounasfood=addlounasfood, addaikataulu=addaikataulu, msg_d=msg_d, msg_f=msg_f, msg_l=msg_l, msg_a=msg_a)

@app.route('/add_hot_drink', methods=['GET', 'POST'])
def add_drink():
    """Handles juoma add"""
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
        error_d = "Lisätty onnistuneesti"
    except ImportError:
        error_d = "Jokin meni pieleen"
    return redirect(url_for("add", error_d=error_d))

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    """Handles ruoka add"""
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
        error_f = "Lisätty onnistuneesti"
    except ImportError:
        error_f = "Jokin meni pieleen"
    return redirect(url_for("add", error_f=error_f))

@app.route('/add_lounas_food', methods=['GET', 'POST'])
def add_lounas_food():
    """Handles lounas add"""
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
        error_l = "Lisätty onnistuneesti"
    except ImportError:
        error_l = "Jokin meni pieleen"
    return redirect(url_for("add", error_l=error_l))

@app.route('/add_aukioloaika', methods=['GET', 'POST'])
def add_aukioloaika():
    """Handles aukioloaika add"""
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            paiva = request.form.get("paiva")
            paivamaara = request.form.get("paivamaara")
            kellonaika = request.form.get("kellonaika")
        cursor.execute("INSERT INTO aukioloajat (paiva, paivamaara, kellonaika)  VALUES (%s, %s, %s)", (paiva, paivamaara, kellonaika))
        connection.commit()
        error_a = "Lisätty onnistuneesti"
    except ImportError:
        error_a = "Jokin meni pieleen"
    return redirect(url_for("add", error_a=error_a))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """the deletion page"""
    text = ""
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        cursor.execute("SELECT id, juoma, hinta FROM juomat")
        getdatajuoma = cursor.fetchall()
        poista_drink = PoistaDrinkForm()
        poista_drink.juomat.choices = [
            (str(id), f"{id}, {juoma}, {hinta}")
            for id, juoma, hinta in getdatajuoma
        ]
        cursor.execute("SELECT id, ruoka FROM ruokamenu")
        getdataruoka = cursor.fetchall()
        poista_ruoka = PoistaRuokaForm()
        poista_ruoka.ruoka.choices = [
            (str(id), f"{id}, {ruoka}")
            for id, ruoka in getdataruoka
        ]
        cursor.execute("SELECT id, ruoka, paivamaara FROM viikonlounasruokamenu")
        getdatalounas = cursor.fetchall()
        poista_lounas = PoistaLounasForm()
        poista_lounas.lounas.choices = [
            (str(id), f"{id}, {ruoka}, {paivamaara}")
            for id, ruoka, paivamaara in getdatalounas
        ]
    except ImportError:
        text = "Jokin meni vikaan"
    msg_d_d = request.args.get("msg_d_d", "")
    msg_r_d = request.args.get("msg_r_d", "")
    msg_l_d = request.args.get("msg_l_d", "")
    return render_template("delete.html",  poista_drink=poista_drink, poista_ruoka=poista_ruoka, poista_lounas=poista_lounas, msg_d_d=msg_d_d, msg_r_d=msg_r_d, msg_l_d=msg_l_d, text=text)

@app.route('/delete_drink', methods=['GET', 'POST'])
def delete_drink():
    """Handles juoma deletion"""
    # if logged in shows the pages
    msg_d_d = ""
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            juomat = request.form.get("juomat")
            cursor.execute(f"DELETE FROM juomat WHERE id='{juomat}';")
            connection.commit()
            msg_d_d = "Poistettu onnistuneesti"
    except ImportError:
        msg_d_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_d_d=msg_d_d))

@app.route('/delete_ruoka', methods=['GET', 'POST'])
def delete_ruoka():
    """Handles ruoka deletion"""
    msg_r_d = ""
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            ruoka = request.form.get("ruoka")
            cursor.execute(f"DELETE FROM ruokamenu WHERE id='{ruoka}';")
            connection.commit()
            msg_r_d = "Poistettu onnistuneesti"
    except ImportError:
        msg_r_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_r_d=msg_r_d))

@app.route('/delete_lounas', methods=['GET', 'POST'])
def delete_lounas():
    """Handles lounas deletion"""
    msg_l_d = ""
    # if logged in shows the pages
    if not session.get("Username"):
        return redirect("/")
    try:
        if request.method == "POST":
            lounas = request.form.get("lounas")
            cursor.execute(f"DELETE FROM viikonlounasruokamenu WHERE id='{lounas}';")
            connection.commit()
            msg_l_d = "Poistettu onnistuneesti"
    except ImportError:
        msg_l_d = "Jokin meni pieleen"
    return redirect(url_for("delete", msg_l_d=msg_l_d))

@app.route("/logout")
def logout():
    """Handles user log out"""
    session["Username"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run()
