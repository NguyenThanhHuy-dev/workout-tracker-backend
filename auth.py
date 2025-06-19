from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import User, Workout
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    db = SessionLocal()
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = User(username=data['username'], password=data['password'])
    db.add(user)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Username already exists"}), 400
    
    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    db = SessionLocal()
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = db.query(User).filter(User.username == data['username'], User.password == data['password']).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200