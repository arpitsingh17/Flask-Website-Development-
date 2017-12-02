from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from dbconnect import connection
from wtforms import Form, TextField, BooleanField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc


TOPIC_DICT = Content()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'

@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/dashboard/')
def dashboard():
    flash("Please login for better experience!!!!")
    return render_template('dashboard.html',TOPIC_DICT = TOPIC_DICT)

@app.route('/login/',methods =["GET","POST"])
def login_page():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            flash(attempted_username)
            flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials, Please try again"
        return render_template("login.html", error=error)

    except exception as e:
        return render_template("login.html",error=error)


class RegistrationForm(Form):
    username = TextField('Username',[validators.length(min=4,max=20)])
    email = TextField('Email Address',[validators.length(min=6,max=50)])
    password = PasswordField('Password',[validators.Required(),
                                            validators.EqualTo('confirm',message = "Passwords must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/tos/"> Terms of Service </a> and the <a href="/privacy/">privacy notice (Last updated Nov-28-2017)</a>',[validators.Required()])



@app.route('/register/',methods =["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          [(thwart(username))])

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html')

@app.errorhandler(405)
def methodnotfound(e):
    return render_template('405.html')

if __name__ == "__main__":
    app.run()
