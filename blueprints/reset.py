from flask import Blueprint, jsonify
from commands.reset_data import ResetData


reset_bp = Blueprint('reset', __name__)


@reset_bp.route("/reset", methods=["DELETE"])
def reset():
    ResetData().execute()
    return jsonify({ 'message': 'Todos los datos han sido borrados' }), 200
