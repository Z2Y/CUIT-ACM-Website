# coding=utf-8
#The database URI that should be used for the connection.
#fomate: dialect+driver://username:password@host:port/database
#mysql format : mysql://scott:tiger@localhost/database_name
SQLALCHEMY_DATABASE_URI = 'mysql://root:63005610@localhost/cuit_acm'

#A dictionary that maps bind keys to SQLAlchemy connection URIs.
SQLALCHEMY_BINDS = {}

ADMIN = ['Rayn', 'dreameracm']

SCHOOL_MAP = {
    'cuit': u'成都信息工程大学',
    'scu': u'四川大学'
}

OJ_MAP = {
    'hdu': 'HDU',
    'cf': 'Codeforces',
    'bc': 'BestCoder',
    'poj': 'POJ',
    'uva': 'UVA',
    'zoj': 'ZOJ',
    'bnu': 'BNU',
    'vj': 'Virtual Judge',
}


CSRF_ENABLED = True
import os.path
UPLOADED_RESOURCE_DEST = os.path.split(os.path.realpath(__file__))[0] + '/static/resource/'
UPLOADED_RESOURCE_URL = '/upload/resource/'
IMAGE_FILE_PATH = 'static/image/bookimg/'
SECRET_KEY = 'a very hard string'
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days=1)

## some config for front end
NEWS_PER_PAGE = 5
USER_MANAGE_PER_PAGE = 10
RESOURCE_MANAGE_PER_PAGE = 10
NEWS_MANAGE_PER_PAGE = 10
