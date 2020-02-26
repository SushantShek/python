import logging

import shelve
from aiohttp import web
from flask import Flask, g, jsonify
from flask_restful import Resource, Api, reqparse

LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

api = Api(app)

# if __name__ == '__main__':
#   app.run(debug=True)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("users.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def health(self):
    return jsonify({'name': 'user-service'})




class UserGetCreate(Resource):
    #   @app.route('/users', methods=['GET'])
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        users = []
        for key in keys:
            users.append(shelf[key], status=200)

        return jsonify({'users': users})

    # @app.route('/users', methods=['POST'])
    def create_user(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('email', required=True)

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['id']] = args

        return jsonify({'user': args}, status=201)


class UserUpdate(Resource):
    # @app.route('/users/<string:user_id>', method=['PUT'])
    def update(self, user_id):
        shelf = get_db()

        if not (user_id in shelf):
            return jsonify({'message': 'Device not found', 'data': {}}, 404)

        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('email', required=True)

        args = parser.parse_args()

        shelf[args[user_id]] = args
        # shelf.update(id,request)
        return jsonify({'message': 'Device registered', 'data': args}, 201)

    # @app.route('/users/<string:user_id>', method=['DELETE'])
    def delete(self, user_id):

        shelf = get_db()
        if not (user_id in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[user_id]

        return jsonify(None, status=204)


api.add_resource(UserGetCreate, '/users')
api.add_resource(UserUpdate, '/users/<string:user_id>')


def create_app():
    return app
