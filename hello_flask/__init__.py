from flask import Flask, render_template, flash, request, url_for, redirect
from content_management import Content
from dbconnect import connection
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

@app.route('/register/',methods =["GET","POST"])
def register_page():
    try:
        c,conn = connection()
        return("okay")
    except Exception as e:
        return str(e)




@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html')

@app.errorhandler(405)
def methodnotfound(e):
    return render_template('405.html')

if __name__ == "__main__":
    app.run()
