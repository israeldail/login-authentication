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
    data = request.get_json()

    if "email" not in data:
        raise APIException('Email Not Found in request', status_code=400)
    if "password" not in data:
        raise APIException('Password Not Found in request', status_code=400)

    user = User.query.filter_by(email=data["email"]).first()

    if user is None:
        raise APIException(
            'Profile does not exist, please check credentials', status_code=404)
    if data["password"] != user.password:
        raise APIException('Password is incorrect', status_code=401)

    access_token = create_access_token(identity=data["email"])
    print("just say something")
    print(access_token)
    # response = make_response(
    #     jsonify({'message': 'login successfully', 'access_token': access_token}), 200,)
    # response.headers["Content-Type"] = "application/json"

    return jsonify(access_token=access_token), 200

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





