import json
import requests
import re           # Ease the handling of regular expressions, such as looking for matching characters in strings
import sqlite3

from flask import Flask, request
from flask_restx import Api, Resource  # , fields reqparse                                                              # Clean up imports?
#from urllib.request import urlopen                                                                                     # Clean up imports, delete?

from config import API_SPORTS_KEY


app = Flask(__name__)
api = Api(app, version='1.1', title='Robi F1 API', description='Turts are Back :)')
url = "https://v1.formula-1.api-sports.io"
headers = {
    'x-rapidapi-key': API_SPORTS_KEY,
    'x-rapidapi-host': 'v1.formula-1.api-sports.io'
}
ns = api.namespace('Robins API', description='ONLY for Arsenal FANS!')

con = sqlite3.connect('F1searchpresets.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cursor = con.cursor()


def save_json_file(name, data):
    """Saves an offline version of response from API(for development purposes)"""
    with open(f'{name}.json', 'w') as outfile:
        outfile.write(data)


@app.route('/presets', methods=['GET', 'POST'])
def check_and_add_db():                        ### Kanske vi ska bytta namn på denna? user, profile eller annet
    """Endpoint used to add elements to and checking all elements in database"""
    if request.method == 'GET':     # return whole database
        response = cursor.execute('SELECT * FROM F1searches')
        unpacked = [{k: item[k] for k in item.keys()} for item in response.fetchall()]
        return '{"presets":' + str(unpacked).replace("'", '"') + '}'
    elif request.method == 'POST':      # add entries to database
        presets = request.form.get('preset')                                                                                 # is "preset" even needed?
        interest = request.form.get('interest')
        validate = SpecificDriver().get(interest, request.method)  # checks for drivers name in the external API
        if validate:
            cursor.execute(f'INSERT INTO F1searches (preset, interest) VALUES (?,?)', (presets, interest))
            con.commit()
            return {'message': 'preset added'}, 201
        else:
            return {'message': 'The driver does not exist, check your spelling.'}, 403                                      # unsure of error code


@app.route('/db/<item_id>', methods=['GET', 'DELETE'])
def delete_and_fetchone_db(item_id):
    """Route used for getting and deleting specific elements in database using id"""
    item = cursor.execute('SELECT * FROM F1searches WHERE id=?', (item_id,)).fetchone()
    if not item:
        return {'message': f'ID: {item_id} not found'}, 404
    if request.method == 'GET':
        interest = cursor.execute('SELECT interest FROM F1searches WHERE id=' + str(item_id)).fetchall()[0][0]
        return SpecificDriver().get(interest, request.method)
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM F1searches WHERE id=' + str(item_id))
        con.commit()
        if response.rowcount > 0:
            return {'message': f'ID: {item_id} was deleted.'}, 200
        else:
            return {'message': f'could not delete ID: {item_id}'}, 404


# @api.route('/drivers/<string:name>')                                                                              #   Pretty sure this route isn't needed!
class SpecificDriver(Resource):
    """This is used to check if drivers names are in the correct format."""
    @classmethod
    def load_drivers_data(cls):
        """Usage: load offline version of response (for development purposes)"""
        with open('driver_2024.json', 'r') as j_file:
            data = json.load(j_file)
            return data

    @classmethod
    def load_rankings(cls):
        """requests rankings of current F1 drivers from external API"""
        rankings = requests.get(url + "/rankings/drivers?season=2024", headers=headers)
        data = rankings.json()
        return data

    def get(self, name, method):
        """Checks if the drivers to and from database exists in external API"""
        if not re.match(r'^[\s\w]+$', name):   # ^ symbol for start of string and $ symbol for end of string ## https://support.kobotoolbox.org/restrict_responses.html
            return {'message': 'Driver name does not exists or is typed in wrong format'}, 404
        drivers_data = self.load_rankings()  # self.load_drivers_data()
        for driver_info in drivers_data['response']:        ### kanske.. KAN TAS BORT!!
            driver_name = driver_info['driver']['name']
            if name.lower() in driver_name.lower():         ### uppdaterat till in istället för ==, nu ska Fernando få fram 'Fernando Alonso'.
                if method == 'POST':
                    print(f'{name} is a valid input')
                    return True
                print(f'We found the name {name} in our list\n')
                print(f'API user requested driver: {name}\nAPI provided info: {driver_info["driver"]}')
                driver = [driver_info['driver'], driver_info['team'], {"points": driver_info['points']}]
                return driver, 200
        if method == 'POST':
            return False
        else:
            return {"Driver does not exist"}, 403


@api.route('/drivers')
class Drivers(Resource):                                                                                                     # Does this need its own class?
    def get(self):
        drivers_url = f"{url}/rankings/drivers?season=2024"

        response = requests.get(drivers_url, headers=headers)
        response_data = response.json()

        if response.ok:  # Checks if response status code is 200
            print(response.status_code)                                                                        # Bara for att kolla, ska tas bort innan inlämning
            print(response_data['response'])                                                                   # Bara for att kolla, ska tas bort innan inlämning
            return response_data['response'], 200
        else:
            return {'error': 'Failed to fetch data'}, response.status_code


if __name__ == '__main__':
    app.run(debug=True)
