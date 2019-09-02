from flask import Flask, render_template, request, redirect, make_response  , Response
from settings import *
import auth
from models import *


app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', products=Product.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if auth.is_authenticated(request):
        return redirect('/')
    if request.method == 'GET':
        return render_template('register.html')
    email = request.form['email']
    password = request.form['password']
    password = auth.encode_password(password)
    try:
        db.execute(
            'insert into users (email, password) values (?, ?)',
            [email, password]
        )
        db.commit()
    except:
        return render_template('register.html')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth.is_authenticated(request):
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    user = auth.authenticate(email, password)
    if user is None:
        return render_template('login.html')
    response = redirect('/')
    auth.login(response, user)
    return response


@app.route('/logout')
def logout():
    response = redirect('/')
    auth.logout(request, response)
    return response


@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.get(product_id)
    if product is None:
        return make_response('', 404)
    return render_template('product.html', product=product)


app.run()
