import os
from datetime import datetime

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# 1. Pull authentication details injected by Kubernetes
DB_USER = os.environ.get("MONGO_USER", "")
DB_PASSWORD = os.environ.get("MONGO_PASSWORD", "")
# Default host points to the internal Kubernetes service name we will create
DB_HOST = os.environ.get("MONGO_HOST", "mongodb-service")

# 2. Build the URI conditionally based on whether auth is provided
if DB_USER and DB_PASSWORD:
    MONGODB_URI = (
        f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:27017/flask_db?authSource=admin"
    )
else:
    # Fallback to standard URI if no auth vars are present
    MONGODB_URI = os.environ.get("MONGODB_URI", f"mongodb://{DB_HOST}:27017/")

client = MongoClient(MONGODB_URI)
db = client.flask_db
collection = db.data


@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == "GET":
        data_list = list(collection.find({}, {"_id": 0}))
        return jsonify(data_list), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
