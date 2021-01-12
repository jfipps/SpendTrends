from sql_connection import get_sql_connection

def get_all_charges(connection, user):
    cursor = connection.cursor()
    query = "SELECT * FROM spendingtrends.spending WHERE userID = " + str(user)
    cursor.execute(query)
    response = []
    for (ChargeID, Category, Vendor, Charge, Card, Date, UserID) in cursor:
        response.append(
            {
                'Charge ID': ChargeID,
                'Category': Category,
                'Vendor': Vendor,
                'Charge': Charge,
                'Card': Card,
                'Date': Date,
                'UserID': UserID
            }
        )
    return response

def get_filtered_charges(connection, filterOptions, user):
    for item in filterOptions:
        print(item)

def insert_new_charge(connection, charge):
    cursor = connection.cursor()
    query = ("insert into spendingtrends.spending (category, vendor, charge, card, date, userID) values (%s, %s, %s, %s, %s, %s);")
    data = (charge['category'], charge['vendor'], charge['charge'], charge['card'], charge['date'], charge['userID'])
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_charge(connection, chargeID):
    cursor = connection.cursor()
    query = ("DELETE FROM spendingtrends.spending where chargeID=" + str(chargeID))
    cursor.execute(query)
    connection.commit()

def check_login(connection, username, password):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM spendingtrends.logins WHERE username = %s AND password = %s', (username, password))
    response = []
    for (ID, username, password, email) in cursor:
        response.append({
            'ID': ID,
            'username': username,
            'password': password,
            'email': email
        })
    return response

def create_user(connection, username, password, email):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO spendingtrends.logins (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    connection.commit()
    return cursor.lastrowid

if __name__ == "__main__":
    connection = get_sql_connection()
    delete_charge(connection, 3)

