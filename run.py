from flask import Flask, render_template, url_for, redirect, request

import mysql.connector
import yaml


db = yaml.load(open('db.yaml'))
app = Flask(__name__)


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


@app.route('/customers')
def customers():
    mycursor.execute("SELECT * FROM customer_details;")

    data = mycursor.fetchall()

    return render_template('customers.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
