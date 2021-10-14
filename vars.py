# (c) Code-x-Mania

from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    SESSION_NAME = str(getenv('SESSION_NAME', 'idzeroid'))    
    OWNER_ID = int(getenv('OWNER_ID', '1445283714'))
    DATABASE_URL = str(getenv('DATABASE_URL'))
    
