from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def configure_connections(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)
    migrate.init_app(app, db)





