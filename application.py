from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# from model.db import init_db
from errors.errors import ApiError
from blueprints.ping import ping_bp
from blueprints.reset import reset_bp
from blueprints.blacklists import blacklist_bp


load_dotenv('.env.development')

application = Flask(__name__)
# init_db(application)
cors = CORS(application)

application.register_blueprint(ping_bp)
application.register_blueprint(blacklist_bp)
application.register_blueprint(reset_bp)


@application.errorhandler(ApiError)
def handle_exception(error):
    response = { 'message': error.description }
    return jsonify(response), error.code
