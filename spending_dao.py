from sql_connection import get_sql_connection

#MYSQL call to get all charges with userID as key
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

#MYSQL call to get charges with filters in place
def get_filtered_charges(connection, filterOptions, user):
    query_where_string = []
    for item in filterOptions:
        if filterOptions[item] != "" and item != "date":
            query_where_string.append(" " + item + " = " + "'" + filterOptions[item] + "'")
        if filterOptions[item] != "" and item == "date":
            query_where_string.append(" " + item + " BETWEEN DATE(NOW()) - INTERVAL " + filterOptions[item] + " AND DATE(NOW())")
    cursor = connection.cursor()
    query = "SELECT * FROM spendingtrends.spending WHERE userID = " + str(user) + " AND"
    for string in query_where_string:
        query = query + string + " AND"
    query = query.rsplit(' AND', 1)[0]
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

#MYSQL call to insert a charge
def insert_new_charge(connection, charge):
    cursor = connection.cursor()
    query = ("insert into spendingtrends.spending (category, vendor, charge, card, date, userID) values (%s, %s, %s, %s, %s, %s);")
    data = (charge['category'], charge['vendor'], charge['charge'], charge['card'], charge['date'], charge['userID'])
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

#MYSQL call to delete selected charge(s)
def delete_charges(connection, charges):
    cursor = connection.cursor()
    for charge in charges:
        query = ("DELETE FROM spendingtrends.spending where chargeID=" + str(charge))
        cursor.execute(query)
    connection.commit()

#MYSQL call to check the logins table for the username and password
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

#MYSQL call to create new users
def create_user(connection, username, password, email):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO spendingtrends.logins (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    connection.commit()
    return cursor.lastrowid

def get_pie_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT category, COUNT(*) AS count FROM spendingtrends.spending GROUP BY category ORDER BY count DESC")
    response = []
    for (category, count) in cursor:
        response.append({
            'Category': category,
            'Count': count
        })
    return response


if __name__ == "__main__":
    connection = get_sql_connection()

