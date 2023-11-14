from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p["id"] == id), None)
    return jsonify(picture)



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<id>", methods=["POST"])
def create_picture(id):
    picture = request.get_json(data)
    if picture["id"] == id:
        for p in data:
            if p["id"] == id:
                return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json(data)
    if picture["id"] == id:
        for i, p in enumerate(data):
            if p["id"] == id:
                data[i] = picture
                return jsonify({"Message": f"picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
     id = int(id)
    for i, p in enumerate(data):
        if p["id"] == id:
           data.pop(i)
            return "", 204
    return jsonify({"Message": f"picture not found"}), 404
