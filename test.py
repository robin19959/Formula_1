import requests
import sqlite3

from flask import Flask, request

from config import API_SPORTS_KEY

app = Flask(__name__)
url = "https://v1.formula-1.api-sports.io"  # External API, retrieving Formula 1 data from
headers = {                                 # External API authentication
    'x-rapidapi-key': API_SPORTS_KEY,
    'x-rapidapi-host': 'v1.formula-1.api-sports.io'
}

"""Connection and command to SQLite database"""
con = sqlite3.connect('F1searchpresets.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cursor = con.cursor()


@app.route('/api/docs')
def get_documentation():
    """Open and return the documentation file"""
    return open('docs/docs.yaml')


@app.route('/drivers', methods=['GET'])
def drivers():
    """Fetches full standings information"""
    return load_rankings()['response']


@app.route('/presets', methods=['GET', 'POST'])
def check_and_add_db():
    """Endpoint used to add elements to and checking all elements in database"""
    if request.method == 'GET':     # return whole database
        response = cursor.execute('SELECT * FROM F1searches')
        whole_db = []  # makes a list with dictionary containing presets and interests from database.
        for value in response.fetchall():
            db_item = {}
            for key in value.keys():
                db_item[key] = value[key]
            whole_db.append(db_item)
        return '{"presets":' + str(whole_db).replace("'", '"') + '}'
    elif request.method == 'POST':      # add entries to database
        preset = request.form.get('preset')
        interest = request.form.get('interest')
        validate = specific_driver(interest, request.method)  # checks for drivers name in the external API
        if validate:
            cursor.execute(f'INSERT INTO F1searches (preset, interest) VALUES (?,?)', (preset, interest))
            con.commit()
            return {'message': f'preset: {preset} added with {interest} as interest'}, 201
        else:
            return {'message': f'The driver: {interest} does not exist, check your spelling.'}, 403


@app.route('/db/<item_id>', methods=['GET', 'DELETE'])
def delete_and_fetchone_db(item_id):
    """Route used for getting and deleting specific elements in database using id"""
    item = cursor.execute('SELECT * FROM F1searches WHERE id=?', (item_id,)).fetchone()
    if not item:
        return {'message': f'ID: {item_id} not found'}, 404
    preset = cursor.execute('SELECT preset FROM F1searches WHERE id=' + str(item_id)).fetchall()[0][0]
    if request.method == 'GET':
        interest = cursor.execute('SELECT interest FROM F1searches WHERE id=' + str(item_id)).fetchall()[0][0]
        return {preset: specific_driver(interest, request.method)}     # returns info about driver
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM F1searches WHERE id=' + str(item_id))
        con.commit()
        if response.rowcount > 0:
            return {'message': f'Preset: {preset} with ID: {item_id} was deleted.'}, 200
        else:
            return {'message': f'could not delete Preset: {preset} with ID: {item_id}'}, 404


def specific_driver(name, method):
    """Checks if the drivers to and from database exists in external API"""
    drivers_data = load_rankings()
    for driver_info in drivers_data['response']:
        driver_name = driver_info['driver']['name']
        if name.lower() in driver_name.lower():
            if method == 'POST':
                return True
            driver = [driver_info['driver'], driver_info['team'], {"position": driver_info['position'], "points": driver_info['points']}]
            return driver, 200
    if method == 'POST':
        return False
    else:
        return {'message': f'Driver: {name} does not exist'}, 403


def load_rankings():
    """Requests rankings of current F1 drivers from external API"""
    response = requests.get(url + "/rankings/drivers?season=2024", headers=headers)
    data = response.json()
    if response.ok:
        return data
    else:
        return {'message': 'error'}, 404


if __name__ == '__main__':
    app.run(debug=True)
