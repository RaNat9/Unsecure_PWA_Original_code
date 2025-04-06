from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
##
from flask import session 
from flask import url_for
from flask import make_response
import uuid
##

import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)

##
app.secret_key = uuid.uuid4()
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
##

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():

    ## validates session
    if 'uuid' not in session:
        return redirect("/")
    
    ## Checks number of times accessed
    session['success_access_count'] = session.get('success_access_count', 0) + 1
    if session['success_access_count'] == 1:
        render_value = session['username']
    else:
        render_value = "Back"        
    
    ## Handles http requests and generates a response
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url)
        #return render_template("/success.html", state=True, value=render_value)
    elif request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        #return render_template("/success.html", state=True, value=render_value)
    else:
        dbHandler.listFeedback()
        #return render_template("/success.html", state=True, value=render_value)

    response = make_response(render_template("/success.html", state=True, value=render_value))
    # response = make_response(render_template('sensitive.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        print(url)
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")

##
@app.route('/logout', methods = ["POST", "GET", "PUT", "PATCH", "DELETE"])
def logout():
    session.clear()
    return redirect("/")
##


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            session.clear()
            session['uuid']=uuid.uuid4()
            session['username'] = username
            session['success_access_count'] = 0
            dbHandler.listFeedback()
            return redirect("/success.html")
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
