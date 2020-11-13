from models.User import User
from schemas.UserSchema import user_schema
from main import db
from main import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask import Blueprint, request, jsonify, abort

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({ "token": access_token })