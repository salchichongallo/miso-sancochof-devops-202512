import os
from flask_sqlalchemy import SQLAlchemy
from model.model import Base


db = SQLAlchemy(model_class=Base)

def init_db(app):
    already_initialize = hasattr(app, 'extensions') and 'sqlalchemy' in app.extensions
    if already_initialize:
        return
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("RDS_USERNAME")}:{os.getenv("RDS_PASSWORD")}@{os.getenv("RDS_HOSTNAME")}:{os.getenv("RDS_PORT")}/{os.getenv("RDS_DB_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    setup_database(app)

def setup_database(app):
    from .blacklist import Blacklist
    with app.app_context():
        db.create_all()
