from flask import Flask, render_template, url_for, redirect, request

import mysql.connector
import yaml


db = yaml.load(open('db.yaml'))
app = Flask(__name__)


global accbalance, accname, identity1
accbalance = ""
accname = ""
identity1 = 0


mydb = mysql.connector.connect(
    host=db["mysql_host"],
    user=db["mysql_user"],
    passwd=db["mysql_password"],
    database=db["mysql_database"],
)

mycursor = mydb.cursor()


@app.route('/')
def home():
    return render_template('Homepage.html')


@app.route('/customers', methods=['GET', 'POST'])
def customers():

    global accname
    global accbalance
    global identity1
    mycursor.execute("SELECT * FROM customer_details;")

    data = mycursor.fetchall()

    if request.method == 'POST':
        customer_name = request.form.get("fname")

        mycursor.execute(
            "SELECT * FROM customer_details WHERE name='" + customer_name + "';")

        customer = mycursor.fetchall()
        identity1 = customer[0][0]
        accbalance = customer[0][4]
        accname = customer[0][1]

        return render_template('viewcustomer.html', customer=customer)

    return render_template('customers.html', data=data)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():

    global accname
    global accbalance
    global identity1

    mycursor.execute("SELECT * FROM customer_details;")

    data = mycursor.fetchall()

    if request.method == "POST":
        n = request.form.get("rname")
        amount = int(request.form.get("tnum"))

        if amount > accbalance:
            error = 1
            return render_template('transfer.html', data=data, accname=accname, error=error)

        else:

            mycursor.execute(
                "SELECT * FROM customer_details WHERE name='" + n + "';")

            c = mycursor.fetchall()
            existing_amount = c[0][4]
            identity2 = c[0][0]

            new_bal_sender = accbalance - amount
            new_bal_reciever = amount + existing_amount

            error = 0

            mycursor.execute(
                "UPDATE `bank_database`.`customer_details` SET `current balance` = "+f'{new_bal_sender}'+" WHERE (`customer id` =" + f'{identity1}' + ");")

            mycursor.execute(
                "UPDATE `bank_database`.`customer_details` SET `current balance` = "+f'{new_bal_reciever}'+" WHERE (`customer id` =" + f'{identity2}' + ");")

            mycursor.execute("SELECT * FROM customer_details;")

            data = mycursor.fetchall()

            return render_template('transfer.html', data=data, accname=accname, error=error)

    return render_template('transfer.html', data=data, accname=accname)


if __name__ == '__main__':
    app.run(debug=True)
