import json
import logging
from aiohttp import web
from random import seed, randint
from dao import Users, session


LOGGER = logging.getLogger(__name__)

routes = web.RouteTableDef()

repo = [
    {
        'id': '1',
        'name': u'User_1',
        'email': u'user.1@test.com'

    },
    {
        'id': '2',
        'name': u'User_2',
        'email': u'user.2@test.com'

    }
]


@routes.get('/')
async def health(request):
    LOGGER.info('HEALTH service called')
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    """GET Request for users return the JSON array for all Users"""

    LOGGER.info('GET service called User ')
    users = session.query(Users).all();
    data =[]
    for u in users:
        user={
            'id': u.id,
            'name': u.name,
            'email':u.email
        }
        data.append(user)

    return web.json_response({'Users': data})


@routes.post('/users')
async def create_user(request):
    """POST Request for users Create a New Entry in the Store for User"""

    LOGGER.info('POST service called')

    try:

        req = await request.json()
        LOGGER.info(req['name'])
        name_p = req['name']
        LOGGER.info('For Name : '+ name_p)
        email_p = req['email']
        LOGGER.info('for email : '+ email_p)
        index = randint(1, 9999)
        value = {'id': index, 'name': name_p, 'email': email_p}

        user=Users(name = name_p, email=email_p)
        session.add(user)
        session.commit()
        repo.append(value)
        response_obj = {'status': 'success'}

        return web.Response(text=json.dumps(response_obj), status=201)

    except Exception as e:

        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response({response_obj}, status=500)


@routes.put('/users/{user_id}')
async def update_user(request,user_id):
    """PUTRequest for user return User of a specific ID and Updated the Detail with ID JSON """

    LOGGER.info('PUT service called')

    req = await request.json()
    user = [user for user in repo if user['id'] == user_id]

    user_p = session.query(Users).filter(Users.id == user_id).first()

    if (len(user) == 0 or not user_p):
        return web.json_response({'User id ': user_id, "available": 0}, status=404)

    try:
        name = req['name']
        email = req['email']
        value = {'id': user_id, 'name': name, 'email': email}
        user_p.name = name
        user_p.email = email
        session.add(user_p)
        session.commit()
        repo.remove(user)
        repo.append(value)
        return web.json_response(value, status=200)
    except Exception as e:

        response_obj = {'status': 'failed', 'reason': str(e)}

        return web.json_response({response_obj}, status=500)


@routes.delete('/users/{user_id}')
async def delete_user(request,user_id):
    """DELETE Request for user remove  User of a specific ID """

    LOGGER.info('DELETE service called for ')

    user_p = session.query(Users).filter(Users.id == user_id).first()
    user = [user for user in repo if user['id'] == user_id]


    try:
        repo.remove(user)
        session.delete(user_p)
        session.commit()
        return web.json_response(None, status=204)

    except Exception as ex:
        response_obj = {'status': 'failed', 'reason': str(ex)}
        return web.json_response(response_obj, status=500)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
