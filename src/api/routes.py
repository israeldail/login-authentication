"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

#create flask app
api = Blueprint('api', __name__)



@api.route("/token", methods=["GET", "POST"])
def create_token():
    request_body_user = request.get_json()
    userLogin = User(email=request_body_user["email"], password=request_body_user["password"])
    if request_body_user["email"] != request_body_user["email"] or request_body_user["password"] != request_body_user["password"]:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=request_body_user["email"])
    return jsonify(access_token=access_token)


@api.route("/hello", methods=["GET"])
@jwt_required()
def get_hello():
    
    dictionary =  {
        "message": "hello world"
    }
    
    return jsonify(dictionary)


@api.route('/user', methods=['POST'])
def create_user():

    request_body_user = request.get_json()
    new_user = User(email=request_body_user["email"],
                    password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    payload = {
        'msg': 'Your account has been registered successfully.',
    }
    return jsonify(payload), 200





