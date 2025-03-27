import os
from flask_sqlalchemy import SQLAlchemy
from .model import Base


db = SQLAlchemy(model_class=Base)

def init_db(app):
    already_initialize = hasattr(app, 'extensions') and 'sqlalchemy' in app.extensions
    if already_initialize:
        return
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    setup_database(app)

def setup_database(app):
    from .blacklist import Blacklist
    with app.app_context():
        db.create_all()
