from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
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
    return jsonify({ 'message': 'Cuenta creada exitosamente.' }), 200
