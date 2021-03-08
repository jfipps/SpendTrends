from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_jsglue import JSGlue
import json
import spending_dao
from sql_connection import get_sql_connection

app = Flask(__name__)
jsglue = JSGlue(app)
app.secret_key = 'thisisakey'
connection = get_sql_connection()

# Home page for logged in users. Will redirect to login page if hit without login session
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

    # Gets all charges for the logged in user. Sorts by date by default
    if request.method == "GET":
        session['id'] = 2
        spending = spending_dao.get_all_charges(connection, 2)
        sortedSpend = sorted(spending, key=lambda k: k['Date'], reverse=True)

        # Adds in dictionary entry for two decimal places for the charge float
        for item in sortedSpend:
            charge_string = "{:.2f}".format(item['Charge'])
            item['charge_string'] = charge_string

        return render_template("home.html", spending=sortedSpend, greeting="")

    # Gets filter data from home page for user. Filters by said data and reloads homepage.
    if request.method == "POST":
        filter_data = {
            'category': request.form['category_filter'],
            'vendor': request.form['vendor_filter'],
            'card': request.form['card_filter'],
            'date': request.form['date_select']
        }
        filtered_spending = spending_dao.get_filtered_charges(connection, filter_data, 2)

        # Adds in dictionary entry for two decimal places for the charge float
        for item in filtered_spending:
            charge_string = "{:.2f}".format(item['Charge'])
            item['charge_string'] = charge_string

        return render_template("home.html", spending=filtered_spending, greeting="")


# Gets checked boxes from user list and deletes said charges. Can be used for returns or paybacks.
@app.route("/delete_charges", methods=["POST"])
def delete_charges():
    if len(request.form.getlist("row_check")) > 0:
        charges = request.form.getlist("row_check")
        spending_dao.delete_charges(connection, charges)
    return redirect(url_for('home'))


# Function for adding a charge. Receives data from the add charge modal.
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
        spending_dao.insert_new_charge(connection, input_data)
        return redirect(url_for('home'))

# Login page for users. Landing page. Sets initial greeting if the first time session was created in browser cache.
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


# Registration page for accounts.
@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST" and 'username' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        spending_dao.create_user(connection, firstName, lastName, username, password, email)
        return redirect(url_for("login"))
    if request.method == "POST":
        msg = "Please complete the registration fields"
        return render_template("register.html", msg=msg)
    if request.method == "GET" and session.get('id') == True:
        return redirect(url_for("home"))

    return render_template("register.html", msg=msg)


# Logout function
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('greeting', None)
    return redirect(url_for("login"))


# Charting page. Used to visualize user data.
@app.route("/charts", methods=["GET"])
def charts():
    if session.get('id'):
        pie_category = spending_dao.get_pie_category(connection, session['id'])
        pie_vendor = spending_dao.get_pie_vendor(connection, session['id'])
        pie_card = spending_dao.get_pie_card(connection, session['id'])
        return render_template("charts.html", title="Charge Charts", max=17000, pie_category=pie_category, pie_vendor=pie_vendor, pie_card=pie_card)
    else:
        return redirect(url_for("login"))

# User profile page. User can edit profile info as needed.
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if session.get('id'):
        user_info = spending_dao.get_user_profile(connection, session['id'])
        print(user_info)
        return render_template("profile.html", user_info=user_info)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    print("Starting Flask server on port 5001")
    app.run(port=5003)