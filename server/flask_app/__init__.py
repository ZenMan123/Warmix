from flask import Flask

app = Flask(__name__)

from server.flask_app import views