import os
from flask import Flask, g, session, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from requests_oauthlib import OAuth2Session
from dynaconf import settings

# Setup
OAUTH2_CLIENT_ID = settings.get("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = settings.get("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI = settings.get("OAUTH2_REDIRECT_URL")

API_BASE_URL = settings.get("API_BASE_URL")
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
db = SQLAlchemy(app)

# default route
@app.route("/")
def index():
    return "200 OK - Please use a link generated in-game."

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@app.route('/getauth/<did>')
def auth(did):
    scope = request.args.get(
        'scope',
        'identify email connections guilds guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL+did)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback/<did>')
def callback(did):
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return "200 OK - Linking Complete"