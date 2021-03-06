import logging
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))

####################
# CORE             #
####################

LOGGING_LEVEL = logging.getLevelName(logging.INFO)
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'deli_menu': {
            'level': LOGGING_LEVEL,
            'handlers': ['console']
        },
        'ingredients_http': {
            'level': LOGGING_LEVEL,
            'handlers': ['console']
        },
        'ingredients_db': {
            'level': LOGGING_LEVEL,
            'handlers': ['console']
        },
        'cherrypy.access': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'cherrypy.error': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'sqlalchemy': {
            'level': 'WARN',
            'handlers': ['console']
        },
    }
}

####################
# DATABASE         #
####################

DATABASE_DB = 'sandwich'
DATABASE_PORT = '5432'
DATABASE_POOL_SIZE = 20

if os.environ.get('CLI'):
    DATABASE_POOL_SIZE = -1

DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']

####################
# Auth             #
####################

AUTH_FERNET_KEYS = os.environ['AUTH_FERNET_KEYS'].split(",")

####################
# HTTP             #
####################

# Set to True so the metadata service knows that it is behind a load balancer
# This is used so clients can't spoof addresses
# We ignore X-Forwarded-For unless we are behind a LB
# Your LB should be set to override any X-Forwarded-For headers from clients
HTTP_LOADBALANCER = os.environ.get('HTTP_LOADBALANCER', False)
