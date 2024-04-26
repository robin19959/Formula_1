import json
import sqlite3
import requests
from urllib.request import urlopen

from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
import re           # Ease the handling of regular expressions, such as looking for matching characters in strings
from config import API_SPORTS_KEY

app = Flask(__name__)

api = Api(app, version='1.1', title='Robi F1 API',description='Turts are Back :)')
url = "https://v1.formula-1.api-sports.io"
headers = {
    'x-rapidapi-key': API_SPORTS_KEY,
    'x-rapidapi-host': 'v1.formula-1.api-sports.io'
}
ns = api.namespace('Robins API', description='ONLY for Arsenal FANS!')




def save_json_file(name, data):
    with open(f'{name}.json', 'w') as outfile:
        outfile.write(data)


con = sqlite3.connect('F1searchpresets.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cursor = con.cursor()


@app.route('/presets', methods=['GET', 'POST'])
def items():                        ### Kanske vi ska bytta namn på denna? user, profile eller annet
    if request.method == 'GET':
        # return list of items
        response = cursor.execute('SELECT * FROM F1searches')
        unpacked = [{k: item[k] for k in item.keys()} for item in response.fetchall()]
        return '{"presets":' + str(unpacked).replace("'", '"') + '}'
    elif request.method == 'POST':
        presets = request.form.get('preset')
        interest = request.form.get('interest')
        cursor.execute(f'INSERT INTO F1searches (preset, interest) VALUES (?,?)', (presets, interest))
        con.commit()
        return 'preset added'


@app.route('/db/<item_id>', methods=['GET', 'DELETE'])
def profile(item_id):
    item = cursor.execute('SELECT * FROM F1searches WHERE id=?', (item_id)).fetchone()
    if not item:
        return {'message': 'ID not found'}, 404
    if request.method == 'GET':
        interest = cursor.execute('SELECT interest FROM F1searches WHERE id=' + str(item_id)).fetchall()[0][0]
        # to_api = url + "/drivers?name=" + str(interest)
        # interest_details = requests.get(to_api, headers=headers)
        # return str(interest_details.text)
        #interest = interest.replace(" ", "")
        return SpecificDriver(Resource).get(interest)
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM F1searches WHERE id=' + str(item_id))
        con.commit()
        if response.rowcount > 0:
            return "deleted"
        else:
            return 'could not delete', 404


class SpecificDriver(Resource):
    @classmethod
    def load_drivers_data(cls):
        with open('driver_2024.json', 'r') as j_file:
            data = json.load(j_file)
            return data

    def load_rankings(self):
        rankings = requests.get(url + "/rankings/drivers?season=2024", headers=headers)
        data = rankings.json()
        return data

    def get(self, name):
        if not re.match(r'^[\s\w]+$', name):   # ^ symbol for start of string and $ symbol for end of string ## https://support.kobotoolbox.org/restrict_responses.html
            return {'message': 'Driver name does not exists or is typed in wrong format'}, 404

        drivers_data = self.load_rankings()  # self.load_drivers_data()
        print(drivers_data)
        for driver_info in drivers_data['response']:        ### kanske.. KAN TAS BORT!!
            driver_name = driver_info['driver']['name']
            if name.lower() in driver_name.lower():         ### opdaterat til in istället för ==, nu ska Fernando få främ 'Fernando Alonso'.
                print(f'Now we found the name {name} in our list\n')
                print(f'API user request driver: {name}\nAPI provide info: {driver_info["driver"]}')
                driver = [driver_info['driver'], driver_info['team'], {"points": driver_info['points']}]
                return driver, 200

                # return driver_info['driver'], 200

        return {'driver':
                    {'message': f'{name} is not found in Formula 1'}}, 404


@api.route('/drivers')
class Drivers(Resource):
    def get(self):
        drivers_url = f"{url}/rankings/drivers?season=2024"

        response = requests.get(drivers_url, headers=headers)

        response_data = response.json()

        drivers_json = json.dumps(response_data, indent=4)
        save_json_file('driver_2024', drivers_json)

        print(response.status_code)
        print(response_data['response'])

        return response_data['response'], 200




if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/home/<string:name>', methods=['POST', 'GET'])
# def home(name):
#     return f'<h1>Hello Mr. {name}, you have now arrived at Turts Paradize!</h1>'

# @api.route('/api/docs')         ### Denna ska göras !!!
# class Documentation():
#     def get(self):
#         return with open('docs/docs.json')



# @api.route('/drivers/NAME')     ### Ta redo på hur man gör sista 'NAME' dynamisk
# class SpecificDriver(Resource):
#     def get(self):