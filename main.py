from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session

# Flask Instance
app = Flask(__name__)


# Database Connectivity
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "sms"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "#GDKrs.4002*"
app.config['MYSQL_CURSORCLASS']="DictCursor"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key="sms"
mysql = MySQL(app)


# Routing
@app.route("/")
def main():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Register / Signup
@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gmail = request.form['gmail']
        roll_no = request.form['roll_no']
        reg_no = request.form['reg_no']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']

        if (pwd == cpwd):
            con = mysql.connection.cursor()
            sql = "INSERT INTO register(full_name, gmail, roll_no, reg_no, pwd, cpwd) values (%s, %s, %s, %s, %s, %s)"
            con.execute(sql, (full_name, gmail, roll_no, reg_no, pwd, cpwd))
            con.connection.commit()
            con.close()
            flash("Register Successfully")
            return redirect(url_for('login'))
    return render_template("signup.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        gmail = request.form['gmail']
        reg_no = request.form['reg_no']
        pwd = request.form['pwd']
        con = mysql.connection.cursor()

        sql = "SELECT gmail, reg_no, pwd FROM register WHERE gmail = %s and reg_no = %s and pwd = %s"
        result = con.execute(sql, (gmail, reg_no, pwd))
        con.connection.commit()
        con.close()

        if result:
            session["reg_no"] = request.form.get("reg_no")
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/signout")
def signout():
    return render_template("logout.html")

@app.route("/logout")
def logout():
    session.pop("reg_no", None)
    return redirect(url_for("main"))


# Faculty Login
@app.route("/faculty_login")
def faculty_login():
    return render_template("faculty_login.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

