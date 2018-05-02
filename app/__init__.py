from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from .generator  import GeoGen
from flask.ext.fixtures import FixturesMixin


app = Flask(__name__, static_url_path = "/assets" , static_folder='assets')
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
migrate = Migrate(app, db)
migrate.add_command('db', MigrateCommand)
FixturesMixin.init_app(app, db)