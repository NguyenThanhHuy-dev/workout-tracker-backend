from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import SessionLocal
from models import User, Workout
from sqlalchemy import func

workout = Blueprint('workout', __name__)

@workout.route('/workouts', methods=['POST'])
@jwt_required()
def add_workout():
    db = SessionLocal()
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'name' not in data or 'duration' not in data:
        return jsonify({"error": "Name and duration are required"}), 400
    
    new_workout = Workout(user_id=user_id, name=data['name'], note=data.get('note'), duration=data['duration'])
    db.add(new_workout)
    db.commit()
    
    return jsonify({"message": "Workout added successfully"}), 201

@workout.route('/workouts/me', methods=['GET'])
@jwt_required()
def get_my_workouts():
    db = SessionLocal()
    user_id = get_jwt_identity()
    workouts = db.query(Workout).filter(Workout.user_id == user_id).all()
    return jsonify([{"id": w.id, "name": w.name, "note": w.note, "duration": w.duration} for w in workouts]), 200

@workout.route('/ranking', methods=['GET'])
def get_ranking():
    db = SessionLocal()
    ranking = (
        db.query(User.username, func.sum(Workout.duration).label("total_duration"))
        .join(Workout, User.id == Workout.user_id)
        .group_by(User.id)
        .order_by(func.sum(Workout.duration).desc())
        .all()
    )
    return jsonify([{"username": r[0], "total_duration": r[1]} for r in ranking]), 200