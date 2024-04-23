# Resource pypi.org:
### https://pypi.org/project/flask-restx/ ###

# Resource from Pypi.org
import json
from urllib.request import urlopen
from flask import Flask
from flask_restx import Api, Resource, fields
import dataset
app = Flask(__name__)
db = dataset.connect('sqlite:///api2.db')
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('Robins API', description='ONLY for Arsenal FANS!')








@api.route('/cardata')
class CarData(Resource):
    def get(self):
        response = urlopen('https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315')
        data = json.loads(response.read().decode('utf-8'))
        return data, 200


@api.route('/combine_data_test')
class CombineDataTest(Resource):
    def get(self):
        try:
            race_results = urlopen('https://ergast.com/api/f1/current/last/results.json')
            qualifying_results = urlopen('https://ergast.com/api/f1/current/last/qualifying.json')
            sprint_results = urlopen('https://ergast.com/api/f1/2024/last/sprint.json')

            race_data = json.loads(race_results.read().decode('utf-8'))
            qualifying_data = json.loads(qualifying_results.read().decode('utf-8'))
            sprint_data = json.loads(sprint_results.read().decode('utf-8'))

            print(race_data)
            print(qualifying_data)
            print(sprint_data)

            combi_f1_data = {
                'race': race_data['MRData']['RaceTable']['Races'][0]['raceName'],
                'quali': qualifying_data['MRData']['RaceTable']['Races'][0]['QualifyingResults'][0]['Driver'],
                # 'sprint': sprint_data['MRData']['RaceTable']['Races'][0]['Sprint']
            }

            json_formatted = json.dumps(combi_f1_data)

            print(json_formatted)

            return json_formatted, 200

        except Exception as e:
            return {'error': str(e)}, 500



if __name__ == '__main__':
    app.run(debug=True)


"""todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)"""