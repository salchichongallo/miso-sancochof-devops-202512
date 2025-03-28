from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from .commands.block_email import BlockEmailCommand
from .errors.errors import ApiError
from .model.blacklist import NewBlacklistJsonSchema
loaded = load_dotenv('.env.development')
from .model.db import init_db

app = Flask(__name__)

init_db(app)
cors = CORS(app)

@app.route("/ping")
def ping():
    return "pong"

@app.post("/blacklists")
def add_email():
    json = request.get_json()
    NewBlacklistJsonSchema.check(json)
    block_email = BlockEmailCommand(
        email=json['email'],
        app_uuid=json['app_uuid'],
        blocked_reason=json.get('blocked_reason') or None,
    )
    data = block_email.execute()
    return jsonify({ 'message': 'Cuenta creada exitosamente.', 'data': data }), 200

@app.errorhandler(ApiError)
def handle_exception(err):
    response = { 'message': err.description }
    return jsonify(response), err.code
