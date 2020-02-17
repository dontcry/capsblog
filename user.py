import http.client
import json  
from flask import request

AUTH0_DOMAIN = 'lihr.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://lihr.auth0.com/api/v2/'
CLIENT_ID = '5o5z4UvshNOCacm3NZIbGikfRSvA13JH'
CLIENT_SECRET = '-Kv3ATmI3Oiyau2Y1WGo55X0g4hqsYmB9tIxRzccg3ltIGwK1bTxd5rPw0kIL78y'
     
conn = http.client.HTTPSConnection("lihr.auth0.com")


def get_access_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "audience": API_AUDIENCE,
    }
    payload = json.dumps(payload)
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    print(data)
    if 'access_token' in data:
        return data['access_token']
    else:
        return False

def get_user_info(): 
    authorization = request.headers.get("Authorization")  
    if not authorization:
        return False
    else: 
        try:
            headers = {'authorization': authorization}
            conn.request("GET", "/userinfo", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read()) 
            if 'error' in data:
                return False
            else:
                return data 
        except: 
            return False

def get_users(token):
    print(token)
    if not token:
        return False
    else:
        authorization = f"Bearer {token}"
        headers = {'authorization': authorization}
        conn.request("GET", "/api/v2/users", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        return data
