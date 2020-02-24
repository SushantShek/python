import logging
from aiohttp import web
import markdown
import os
import shelve
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

LOGGER = logging.getLogger(__name__)


routes = web.RouteTableDef()

appf = Flask(__name__)
api = Api(appf)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("users.db")
    return db

@appf.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@routes.get('/')
async def health(request):
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    shelf = get_db()
    keys=shelf.keys()

    users= []
    for key in keys:
        users.append(shelf[key],status=200)

    return web.json_response(users)


@routes.post('/users')
async def create_user(request):
    parser = reqparse.RequestParser()

    parser.add_argument('id', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('email', required=True)

    args = parser.parse_args()

    shelf = get_db()
    shelf[args['id']] = args

    return web.json_response({'user': args}, status=201)


@routes.put('/users/{user_id}')
async def update_user(request):
    user_id=request.match_info.get('user_id','0')
    shelf = get_db()

    if not (user_id in shelf):
        return {'message': 'Device not found', 'data': {}}, 404

    parser = reqparse.RequestParser()

    parser.add_argument('id', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('email', required=True)

    args = parser.parse_args()

    shelf[args['identifier']] = args
    #shelf.update(id,request)
    return web.json_response({'message': 'Device registered', 'data': args}, 201)



@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = request.match_info.get('user_id', '0')

    shelf = get_db()
    if not (user_id in shelf):
        return {'message': 'Device not found', 'data': {}}, 404

    del shelf[user_id]

    return web.json_response(None, status=204)


#def create_app():
 #   app = web.Application()
  #  app.add_routes(routes)
   # return app
api.add_resource()