from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

# Flask Instance
app = Flask(__name__)


# Database Connectivity
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "sms"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "#GDKrs.4002*"
app.config['MYSQL_CURSORCLASS']="DictCursor"
app.secret_key="sms"
mysql = MySQL(app)


# Routing
@app.route("/")
def main():
    return render_template("base.html")

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
            return render_template('main.html')
        else:
            return render_template("login.html")

    return render_template("login.html")

@app.route("/logout")
def logout():
    return render_template('logout.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
