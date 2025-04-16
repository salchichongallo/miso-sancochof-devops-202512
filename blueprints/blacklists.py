from flask import Blueprint, request, jsonify

from commands.check_token import CheckTokenCommand
from commands.block_email import BlockEmailCommand
from commands.verify_email import CheckEmailCommand
from model.blacklist import NewBlacklistJsonSchema, ValidateEmailJsonSchema


blacklist_bp = Blueprint('blacklist', __name__)


@blacklist_bp.post("/blacklists")
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


@blacklist_bp.route("/blacklists/<string:email>", methods=["GET"])
def check_blacklist(email):
    CheckTokenCommand.execute()
    ValidateEmailJsonSchema.check({'email': email})
    response = CheckEmailCommand(email).execute()
    return jsonify(response), 200
