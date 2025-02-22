#from aiohttp import web
#from flask import Flask
from app import create_app
#from userservice.app import app
import logging

#from userservice import app

LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')

    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=True)
   #
   # web.run_app(app)