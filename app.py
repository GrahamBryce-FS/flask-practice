from flask import Flask, redirect, url_for, render_template, request, session,jsonify
from datetime import timedelta

import json
from os import environ as env
from urllib.parse import quote_plus,urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from functools import wraps

app= Flask(__name__)
oauth = OAuth(app)
app.secret_key = "apples"
app.debug=True
AUTH0_BASE_URL="https://dev-p7gfb1ppjic0nc3g.us.auth0.com"

auth0 = oauth.register(

        'auth0',
        client_id="4kCcQd4M5oepaEjmLSaGjzJzTooltn8Y",
        client_secret="xsXT7A54Fyy9sUa49Y2fvZnUDGNfAUsCQfGsMFbXtxnk4FuAbq-kWAAZ-4IWmA5b",
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL+"/oauth/token",
        authorize_url=AUTH0_BASE_URL+"/authorize",
        client_kwargs={'scope':'openid profile email',
        
        },
    server_meta_url="https://dev-p7gfb1ppjic0nc3g.us.auth0.com/.well-known/openid-configuration",
    jwks_uri= "https://dev-p7gfb1ppjic0nc3g.us.auth0.com/.well-known/jwks.json",
)


app.config["SESSION_TYPE"]="filesystem"

class AuthErro(Exception):
  def __init__(self, error,status_code):
    self.error=error
    self.status_code=status_code


@app.route("/home")
def home():
  print("hello")
  return render_template("home.html")


@app.route("/callback", methods=["GET", "POST"])
def callback():
  token = auth0.authorize_access_token()
  session["user"]=token
  resp= auth0.get('userinfo')
  print(resp)
  return redirect("/dashboard")

@app.route("/login")
def login():
  return oauth.auth0.authorize_redirect(
    redirect_uri=url_for("callback", _external=True,_scheme="http"))


def requires_auth(f):
  @wraps(f)
  def decorated(*arg, **kwargs):
    print(session)
    if 'profile' not in str(session):
      return redirect("/home")
    return f(*arg, **kwargs)
  return decorated

@app.route("/settings")
@requires_auth
def settings():
  return render_template("settings.html",
    session=session.get("user"), 
    pretty = json.dumps(session.get("user"),indent=4))

@app.route("/dashboard")
@requires_auth
def dashboard():
  return render_template("dashboard.html", 
    session=session.get("user"), 
    pretty = json.dumps(session.get("user"),indent=4))

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=8080)
