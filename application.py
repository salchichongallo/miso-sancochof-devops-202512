from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from commands.check_token import CheckTokenCommand
from commands.block_email import BlockEmailCommand
from commands.reset_data import ResetData
from commands.verify_email import CheckEmailCommand
from errors.errors import ApiError
from model.blacklist import NewBlacklistJsonSchema, ValidateEmailJsonSchema
loaded = load_dotenv('.env.development')
from model.db import init_db

application = Flask(__name__)

init_db(application)
cors = CORS(application)

@application.route("/ping")
def ping():
    return "pong"

@application.post("/blacklists")
def add_email():
    CheckTokenCommand.execute()
    json = request.get_json()
    NewBlacklistJsonSchema.check(json)
    block_email = BlockEmailCommand(
        email=json['email'],
        app_uuid=json['app_uuid'],
        ip=request.remote_addr,
        blocked_reason=json.get('blocked_reason') or None,
    )
    data = block_email.execute()
    return jsonify({ 'message': 'Cuenta creada exitosamente.', 'data': data }), 200

@application.route("/blacklists/<string:email>", methods=["GET"])
def check_blacklist(email):
    CheckTokenCommand.execute()
    ValidateEmailJsonSchema.check({'email': email})
    response = CheckEmailCommand(email).execute()
    return jsonify(response), 200


@application.route("/reset", methods=["DELETE"])
def reset():
    ResetData().execute()
    return jsonify({ 'message': 'Todos los datos han sido borrados' }), 200

@application.errorhandler(ApiError)
def handle_exception(err):
    response = { 'message': err.description }
    return jsonify(response), err.code
