import requests
import urllib3
import json


# routes packages
from flask import Flask
from flask_cors import CORS


# removes error
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# instantiate the app
app = Flask(__name__)
# CORS
CORS(app)


#
#
# STRAVA API
#
#
# creates the link to access my Strava data
auth_url = "https://www.strava.com/oauth/token"

payload = {
    'client_id': 'XXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'refresh_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'grant_type': "refresh_token",
    'f': 'json'
}


# concatenates the url and the access token
print("requesting token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access token = {}\n".format(access_token))


# uses access token and retreives Strava data as json
activity_url = "https://www.strava.com/api/v3/athlete/activities"

header = {'Authorization': 'Bearer ' +
          access_token}
param = {'per_page': 200, 'page': 1}
activitiesFetched = requests.get(
    activity_url, headers=header, params=param).json()


#
# END STRAVA API
#


@app.route('/')
def index():
    return 'hello world'

# initialize endpoint (GET request)
@app.route('/activities', methods=['GET'])
def get_activities():
    return json.dumps(activitiesFetched)


# start the app
if __name__ == '__main__':
    app.run()
