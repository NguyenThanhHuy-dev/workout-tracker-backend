from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import Base, engine, SessionLocal
from auth import auth
from workout import workout

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)
CORS(app)

Base.metadata.create_all(bind=engine)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(workout, url_prefix='/workout')

@app.route('/')
def home():
    return {"status": "API is running"}

if __name__ == '__main__':
    app.run(debug=True)