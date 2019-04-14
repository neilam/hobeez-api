from flask import Flask, url_for
from flask import request, redirect
import json
import redis

app = Flask(__name__)


ttl = 31104000 #one year


try:
    r = redis.Redis(host='redis-18197.c13.us-east-1-3.ec2.cloud.redislabs.com',port=18197, password='RsAHnx8V0YTE7B62P2LtgXt2MGFEXYie')
except Exception as ex:
    print 'Error:', ex

@app.route('/register', methods=['POST'])
def reg():
    if not request.json:
        abort(400)
    print request.json
    if 'username' not in request.json.keys() or "pwdhash" not in request.json.keys():
        return "invalid parameters"
    if r.get(request.json["username"]):
        return "user already exists"
    r.set(request.json["username"], request.json["pwdhash"])
    return r.get(request.json["username"])


@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)
    if 'username' not in request.json.keys() or "pwdhash" not in request.json.keys():
        return "invalid parameters"
    if int(r.get(request.json["username"])) == int(request.json["pwdhash"]):
        return redirect(url_for('about'))
    print type(r.get(request.json["username"]))
    print type(request.json["pwdhash"])
    return "wrong credentials"



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'You are now logged in. The about page is here..'

if __name__ == '__main__':
    app.run()




