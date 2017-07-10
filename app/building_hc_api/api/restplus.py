import traceback
import logging

from flask_restplus import Api
from building_hc_api import settings
from sqlalchemy.orm.exc import NoResultFound


log = logging.getLogger(__name__)

api = Api(version='1.0', title='HotMaps building hc API',
          description='HotMaps building HC API that computes XXX.')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A models result was required but none was found.'}, 404