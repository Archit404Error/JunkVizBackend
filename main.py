import requests
from bson import json_util
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient(
    "mongodb+srv://admin:admin@trash.lxiq1x5.mongodb.net/?retryWrites=true&w=majority"
)


@app.route("/all-points", methods=["GET"])
def get_all_points():
    litter_posts = db.Trash.posts.find()
    return json_util.dumps(list(litter_posts))


@app.route("/classify", methods=["POST"])
def classify_image():
    data = request.files["image"]

    ## some logic here

    return jsonify({"success": True})


@app.route("/notify", methods=["POST"])
def send_notifs():
    requests.post(
        "https://exp.host/--/api/v2/push/send",
        json={
            "to": request.body["token"],
            "title": "Trash Detected",
            "body": "New trash detected in your area",
        },
    )

    return jsonify({})


app.run(debug=True)
