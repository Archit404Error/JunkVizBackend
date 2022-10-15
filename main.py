import json
import os

import boto3
import botocore
import requests
from bson import json_util
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from werkzeug.utils import secure_filename

app = Flask(__name__)
load_dotenv()
db = MongoClient(os.environ.get("CONNECTION_STR")).get_database("Trash")
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def upload(file):
    s3.upload_fileobj(
        file,
        os.getenv("AWS_BUCKET_NAME"),
        file.filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type,
        },
    )

    return file.filename


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["litter_img"]
    return json.dumps({"url": os.getenv("AWS_DOMAIN") + upload(file)})


@app.route("/all-points", methods=["GET"])
def get_all_points():
    litter_posts = db.posts.find()
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


if __name__ == "__main__":
    app.run(debug=True)
