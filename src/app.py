from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']

    # simple login check for demo
    if username == "admin" and password == "1234":
        return render_template('dashboard.html')
    else:
        return "Invalid login"

if __name__ == "__main__":
    app.run(debug=True)