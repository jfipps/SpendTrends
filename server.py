from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import spending_dao
from sql_connection import get_sql_connection

app = Flask(__name__)
app.secret_key = 'thisisakey'
connection = get_sql_connection()

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    # if request.method == "GET" and session['greeting']:
    #     spending = spending_dao.get_all_charges(connection, session['id'])
    #     greeting = ""
    #     return render_template("home.html", spending=spending, greeting=greeting)
    # if request.method == "GET" and session['loggedin']:
    #     session['greeting'] = True
    #     greeting = ("Welcome, " + session['username'])
    #     spending = spending_dao.get_all_charges(connection, session['id'])
    #     return render_template("home.html", spending=spending, greeting=greeting)
    # if request.method == "GET" and not session['loggedin']:
    #     return redirect(url_for("login"))
    if request.method == "GET":
        session['id'] = 2
        spending = spending_dao.get_all_charges(connection, 2)
        sortedSpend = sorted(spending, key=lambda k: k['Date'], reverse=True)
        return render_template("home.html", spending=sortedSpend, greeting="")
    if request.method == "POST":
        filter_data = {
            'category': request.form['category'],
            'vendor': request.form['vendor'],
            'card': request.form['card'],
            'date': request.form['dateSelect']
        }
        filtered_spending = spending_dao.get_filtered_charges(connection, filter_data, 2)
        for item in filtered_spending:
            print(item)
        return render_template("home.html", spending=filtered_spending, greeting="")


@app.route("/delete_charges", methods=["POST"])
def delete_charges():
    charges = request.form.getlist("row_check")
    spending_dao.delete_charges(connection, charges)
    return redirect(url_for('home'))

@app.route("/add_charge", methods=["GET", "POST"])
def add_charge():
    if request.method == "GET":
        return render_template("add_charge.html")
    if request.method == "POST" and 'id' in session:
        input_data = {
            'category': request.form['category'],
            'vendor': request.form['vendor'],
            'charge': request.form['charge'],
            'card': request.form['card'],
            'date': request.form['date'],
            'userID': session['id']
        }
        for item in input_data:
            print(item)
        spending_dao.insert_new_charge(connection, input_data)
        return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = spending_dao.check_login(connection, username, password)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]['ID']
            session['username'] = account[0]['username']
            session['greeting'] = False
            return redirect(url_for("home"))
        else:
            msg = "Incorrect username/password"

    return render_template("login.html", msg=msg)

@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        spending_dao.create_user(connection, username, password, email)
        return redirect(url_for("login"))
    if request.method == "POST":
        msg = "Please complete the registration fields"
        return render_template("register.html", msg=msg)

    return render_template("register.html", msg=msg)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('greeting', None)
    return redirect(url_for("login"))

@app.route("/test", methods=["POST"])
def test():
    print(request.form.getlist("row_check"))
    return "Done"

if __name__ == "__main__":
    print("Startng Flask server on port 5001")
    app.run(port=5002)