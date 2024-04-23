import json
from urllib.request import urlopen

import requests
from flask import Flask
from flask_restx import Api, Resource, fields
from config import API_SPORTS_KEY
import dataset
app = Flask(__name__)

api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)
url = "https://v1.formula-1.api-sports.io"
headers = {
    'x-rapidapi-key': API_SPORTS_KEY,
    'x-rapidapi-host': 'v1.formula-1.api-sports.io'
}

ns = api.namespace('Robins API', description='ONLY for Arsenal FANS!')

def save_json_file(name, data):
    with open(f'{name}.json', 'w') as outfile:
        outfile.write(data)


@api.route('/drivers')
class Drivers(Resource):
    def get(self):
        drivers = "/rankings/drivers?season=2024"

        response = requests.get(url + drivers, headers=headers)

        drivers_json = json.dumps(response, indent=4)
        save_json_file(drivers, drivers_json)

        print(response.status_code)
        print(response.json())

        return response.json(), 200


# @api.route('/drivers/NAME')     ### Ta redo på hur man gör sista 'NAME' dynamisk
# class SpecificDriver(Resource):
#     def get(self):



if __name__ == '__main__':
    app.run(debug=True)