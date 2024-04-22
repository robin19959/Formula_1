import json

#import flask_restful
from flask import Flask
from urllib.request import urlopen


app = Flask(__name__)


#@app.route('/api/driverStandings')
def get_driver_standings():
    response = urlopen('https://ergast.com/api/f1/current/driverStandings.json')
    lista = []
    standing = json.loads(response.read().decode('utf-8'))
    for i in standing['MRData']['StandingsTable']['StandingsLists']:  # ['DriverStandings']:
        lista.append(i)
        #print(i)
    for i in lista:
        for key, value in list(i.items()):
            if "url" in key:
                del i["url"]

    print(lista)
    #standing = make_readable(response)

    #readable = make_readable(response)

    #print(readable)
    #print(standing)


#@app.route('/api/constructorStandings')
def get_constructor_standings():
    response = urlopen('https://ergast.com/api/f1/current/constructorStandings.json')
    data = make_readable(response)

    print(data)


#@app.route('/api/raceSchedule')
def get_schedule():
    response = urlopen('https://ergast.com/api/f1/current.json')
    data = make_readable(response)

    print(data)


def make_readable(data):
    readable = json.dumps(json.loads(data.read().decode('utf-8')), indent=2)

    return readable


if __name__ == '__main__':
    get_driver_standings()
