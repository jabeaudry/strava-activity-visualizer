import requests
import urllib3
from flask import Flask
import os
# SQLite package import
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# routes packages
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


# removes error
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# initilalize and start Flask module

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)


# base directory
basedir = os.path.abspath(os.path.dirname(__file__))


# db application configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# CORS handling
# accepts all requests from hitting the /api endpoint
CORS(app, resources={r"/api": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# databse model (activity)
# sport type, activity duration and year that ist was completed
class Activity(db.Model):
    id = db.Column(db.Double, primary_key=True)
    sport = db.Column(db.String(100))
    duration = db.Column(db.Double)
    year = db.Column(db.Integer)

    def __init__(self, sport, duration, year):
        # Adds the data to the instance
        self.sport = sport
        self.duration = duration
        self.year = year


# db schema (singular activity)
class ActivitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'sport', 'duration', 'year')


# initialize schema (single and multiple activities)
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)


#
#
# ENDPOINT POST
# create an activity
#
#
@app.route('/api/activity', methods=['POST'])
@cross_origin(origin='*', headers=['content-type'])
def add_act():
    # get the data
    sport = request.json['sport']
    duration = request.json['duration']
    year = request.json['year']

    # Create an instance
    new_act = Activity(sport, duration, year)

    # Save the todo in the db
    db.session.add(new_act)
    db.session.commit()

# return the created todo
    return activity_schema.jsonify(new_act)


#
#
# ENDPOINT GET
# retrieve all activities
#
#

@app.route('/api/activity', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_acts():
    # get the activities from db
    all_acts = Activity.query.all()
    # get the activities as per the schema
    result = activities_schema.dump(all_acts)
    # return the activities
    return jsonify(result)

#
#
# ENDPOINT GET
# retrieve one activity
#
#


@app.route('/api/activity/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_todo(id):
    # get a single todo
    activity = Activity.query.get(id)
    # return the todo as per the schema
    return activity_schema.jsonify(activity)


#
#
# ENDPOINT DELETE
#
#
# will probably not need this
@app.route('/api/activity/<id>', methods=['DELETE'])
@cross_origin(origin='*', headers=['Content-Type'])
def delete_activity(id):
    # get the todo to be deleted
    activity = Activity.query.get(id)

    # delete from the database
    db.session.delete(activity)

    # commit on the database
    db.session.commit()

    # return thr deleted activity as per the schema
    return activity_schema.jsonify(activity)


#
#
# STRAVA API
#
#

# creates the link to access my Strava data
auth_url = "https://www.strava.com/oauth/token"

payload = {
    'client_id': '83740',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'refresh_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
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
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activity_url, headers=header, params=param).json()

print(my_dataset[0]["name"])  # individual access to name
