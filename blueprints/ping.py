from flask import Blueprint


ping_bp = Blueprint('health', __name__)


@ping_bp.route("/ping")
def ping():
    return "pong"

@ping_bp.route("/pong")
def pong():
    return "ping"
