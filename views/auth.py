from flask import Flask, request, redirect
import requests
from urllib.parse import urlencode, quote_plus

app = Flask(__name__)

client_id = '476d8143e749490d82b9e34cc8a3cc5a'
client_secret = ''
redirect_uri = 'http://localhost/5000'
auth_url = 'https://accounts.spotify.com/authorize'

payload = {'client_id': client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}
params = urlencode(payload, quote_via=quote_plus)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/auth')
def authorize():
    return redirect(auth_url + params)


