from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Really Secret Key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REMEMBER_COOKIE_DOMAIN'] = '.localhost'

login_manager = LoginManager()
login_manager.init_app(app)

api_prefix = '/api'
rest_api = Api(app)
