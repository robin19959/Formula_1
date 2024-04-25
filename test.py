import json
import sqlite3
import requests
from urllib.request import urlopen

from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import API_SPORTS_KEY

app = Flask(__name__)

api = Api(app, version='1.1', title='Robi F1 API',
          description='Turts are Back :)')

url = "https://v1.formula-1.api-sports.io"
headers = {
    'x-rapidapi-key': API_SPORTS_KEY,
    'x-rapidapi-host': 'v1.formula-1.api-sports.io'
}
ns = api.namespace('Robins API', description='ONLY for Arsenal FANS!')


@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    return f'<h1>Hello Mr. {name}, you have now arrived at Turts Paradize!</h1>'


def save_json_file(name, data):
    with open(f'{name}.json', 'w') as outfile:
        outfile.write(data)


con = sqlite3.connect('F1searchpresets.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cursor = con.cursor()


@app.route('/presets', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        # return list of items
        response = cursor.execute('SELECT * FROM F1searches')
        unpacked = [{k: item[k] for k in item.keys()} for item in response.fetchall()]
        return '{"presets":' + str(unpacked).replace("'", '"') + '}'
    elif request.method == 'POST':
        presets = request.form.get('preset')
        interest = request.form.get('interest')
        favo_driver = SpecificDriver.get(interest)
        print(favo_driver)
        cursor.execute(f'INSERT INTO F1searches (preset, interest) VALUES (?,?)', (presets, interest))
        con.commit()
        return 'preset added'


@app.route('/items/<item_id>', methods=['GET', 'DELETE'])
def profile(item_id):
    if request.method == 'GET':
        interest = cursor.execute('SELECT interest FROM F1searches WHERE preset=' + str(item_id)).fetchall()#[0][0]
        print(interest)
        print(type(interest))
        interest_details = requests.get(url + "/" + str(interest), headers)
        print(interest_details.text)
        return str(interest_details.text)
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM F1searches WHERE presets=' + str(item_id))
        con.commit()
        if response.rowcount > 0:
            return "deleted"
        else:
            return 'could not delete', 404


@api.route('/drivers/<string:name>')
class SpecificDriver(Resource):
    @classmethod
    def load_drivers_data(cls):
        with open('driver_2024.json', 'r') as j_file:
            data = json.load(j_file)
            return data

    def get(self, name):
        drivers_data = self.load_drivers_data()
        for driver_info in drivers_data['response']:
            driver_name = driver_info['driver']['name']
            if name.lower() == driver_name.lower():
                print(f'Now we found the name {name} in our list\n')
                print(f'API user request driver: {name}\nAPI provide info: {driver_info["driver"]}')
                return driver_info['driver'], 200

        return {'driver':
                    {'message': f'{name} is not found in Formula 1'}}, 404


# @api.route('/drivers')
# class Drivers(Resource):
#     def get(self):
#         drivers = "/rankings/drivers?season=2024"
#
#         response = requests.get(url + drivers, headers=headers)
#
#         response_data = response.json()
#
#         drivers_json = json.dumps(response_data, indent=4)
#         save_json_file('driver_2024', drivers_json)
#
#         print(response.status_code)
#         print(response.json())
#
#         return response.json(), 200


# @api.route('/drivers/NAME')     ### Ta redo på hur man gör sista 'NAME' dynamisk
# class SpecificDriver(Resource):
#     def get(self):


if __name__ == '__main__':
    app.run(debug=True)
