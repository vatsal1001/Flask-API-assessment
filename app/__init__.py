from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/myapplication.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"autoflush": False})

from .routes.user_routes import UserRoutes
from .routes.team_routes import TeamRoutes
from .routes.board_routes import BoardRoutes

UserRoutes.register(app, route_base="/user")
TeamRoutes.register(app, route_base="/team")
BoardRoutes.register(app, route_base="/board")
