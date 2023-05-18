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
    session.pop("unique_code", None)
    return redirect(url_for("astudent"))

# Faculty Login
@app.route("/faculty_login", methods = ['POST', 'GET'])
def faculty_login():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gmail = request.form['gmail']
        unique_code = request.form['unique_code']
        pwd = request.form['pwd']
    
        con = mysql.connection.cursor()
        sql = "SELECT * FROM faculty WHERE full_name = %s and gmail = %s and unique_code = %s and pwd = %s"
        result = con.execute(sql, (full_name, gmail, unique_code, pwd))

        if result:
            session["unique_code"] = request.form.get("unique_code")
            return redirect(url_for('home'))
        else:
            return render_template("faculty_login.html")
    
    return render_template("faculty_login.html")

@app.route("/astudent")
def astudent():
    con = mysql.connection.cursor()
    sql = "select * from student"
    con.execute(sql)
    result= con.fetchall()
    con.connection.commit()  
    con.close()
    return render_template('astudent.html', data = result)
    
# Student profile page edit form
@app.route("/edit_profile", methods = ['POST',  'GET'])
def edit_profile():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gmail = request.form['gmail']
        roll_no = request.form['roll_no']
        reg_no = request.form['reg_no']
        skill = request.form['skill']
        dob = request.form['dob']

        con = mysql.connection.cursor()
        sql = "INSERT INTO student (full_name, gmail, roll_no, reg_no, skill, dob) values (%s, %s, %s, %s, %s, %s)"

        result = con.execute(sql, (full_name, gmail, roll_no, reg_no, skill, dob))
        con.connection.commit()
        con.close()

        if result:
            session['skill'] = request.form.get("skill")
            return redirect(url_for('astudent'))
        else:
            return render_template('edit_profile.html')
    return render_template('edit_profile.html')

# Contact message
@app.route("/contact_message", methods = ['POST', 'GET'])
def contact_message():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gmail = request.form['gmail']
        msg = request.form['message']
        if (full_name.strip() != "" and gmail.strip() != "" and msg.strip() != ""):
            con = mysql.connection.cursor()
            sql = "INSERT INTO messages (full_name, gmail, msg) values (%s, %s, %s)"
            result = con.execute(sql, (full_name, gmail, msg))
            con.connection.commit()
            con.close()

        if result:
            flash("message submitted successfully")
            return redirect(url_for('home'))
        else:
            return render_template('contact.html')
    
    return render_template('contact.html')

# Admin Panel
@app.route("/admin4002")
def admin():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM messages")
    result = con.fetchall()
    con.connection.commit()
    con.close()
    if result:
        return render_template('admin.html', messages = result)
    else:
        return render_template('base.html')


if __name__ == "__main__":
    app.debug = True
    app.run()

