from flask import Flask
from os import getenv

app = Flask(__name__, static_folder='static')
app.secret_key=getenv("SECRET_KEY")

import routes