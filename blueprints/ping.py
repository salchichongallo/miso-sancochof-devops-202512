from flask import Blueprint


ping_bp = Blueprint('health', __name__)


@ping_bp.route("/ping")
def ping():
    return "pong"
