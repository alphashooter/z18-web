from flask import Flask, Response, make_response, render_template, request

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=["GET", "POST"])
def index():
    params = {}
    if request.method == "POST":
        params["name"] = request.form["name"]
    return render_template('index.html', **params)



app.run()
