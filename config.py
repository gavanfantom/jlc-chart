"""Flask configuration."""

from os import environ, path
from dotenv import load_dotenv
import secrets

basedir = path.abspath(path.dirname(__file__))
dotfile = path.join(basedir, '.env')

# Let's make this as easy as possible to deploy, shall we?
if not os.path.exists(dotfile):
    with open(dotfile, 'w') as f:
        f.write("SECRET_KEY = '{}'".format(secrets.token_urlsafe(16)))

load_dotenv(dotfile)

# For development, you know what to do
#FLASK_ENV = 'development'
FLASK_ENV = 'production'
SECRET_KEY = environ.get('SECRET_KEY')
