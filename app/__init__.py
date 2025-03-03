from flask import Flask
from app.routes.patient_routes import patient_bp
from app.routes.reschedule_routes import reschedule_bp 

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(patient_bp)
    app.register_blueprint(reschedule_bp)

    return app
