from aiohttp import web
from app import create_app
import logging
from dao import Users
from sqlalchemy import engine_from_config


LOGGER = logging.getLogger(__name__)

users = {}
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')
    app = create_app()
    web.run_app(app)