from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('Homepage.html')


@app.route('/customers')
def customers():
    return render_template('customers.html')


if __name__ == '__main__':
    app.run(debug=True)
