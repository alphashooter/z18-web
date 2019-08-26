from flask import Flask, render_template, request, redirect
from sqlite3 import connect


app = Flask(__name__, static_url_path='/static')


def get_db():
    return connect('db.sqlite3')


@app.route('/', methods=["GET", "POST"])
def index():
    params = {}
    if request.method == "POST":
        params["name"] = request.form["name"]
    return render_template('index.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    db.execute(
        'insert into users (email, password) values (?, ?)',
        [email, password]
    )
    db.commit()
    return redirect('/')


app.run()
