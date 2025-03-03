from flask import Blueprint, jsonify, request
from app.utils.db import get_db_connection

# Blueprint for patient routes
patient_bp = Blueprint("patients", __name__)

# Get all patients
@patient_bp.route("/patients", methods=["GET"])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in patients])

# Add a new patient
@patient_bp.route("/patients", methods=["POST"])
def add_patient():
    data = request.json  # Get JSON request data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, gender, diagnosis, current_medication, previous_medication, next_appointment_date, provider, doctor, admission_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data["name"], data["age"], data["gender"], data["diagnosis"], data["current_medication"],
         data["previous_medication"], data["next_appointment_date"], data["provider"], data["doctor"], data["admission_date"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Patient added successfully"}), 201

# Query patient by ID
@patient_bp.route("/patients/id/<int:patient_id>", methods=["GET"])
def get_patient_by_id(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    conn.close()

    if patient:
        return jsonify(dict(patient))
    return jsonify({"error": "Patient not found"}), 404

# Query patients by name
@patient_bp.route("/patients/name/<name>", methods=["GET"])
def get_patients_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + name + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found with this name"}), 404

# Query patients by age
@patient_bp.route("/patients/age/<int:age>", methods=["GET"])
def get_patients_by_age(age):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE age = ?", (age,))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found with this age"}), 404

# Query patients by gender
@patient_bp.route("/patients/gender/<gender>", methods=["GET"])
def get_patients_by_gender(gender):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE gender = ?", (gender,))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found with this gender"}), 404

# Query patients by diagnosis
@patient_bp.route("/patients/diagnosis/<diagnosis>", methods=["GET"])
def get_patients_by_diagnosis(diagnosis):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", ('%' + diagnosis + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found with this diagnosis"}), 404

# Query patients by current medication
@patient_bp.route("/patients/current_medication/<medication>", methods=["GET"])
def get_patients_by_current_medication(medication):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE current_medication LIKE ?", ('%' + medication + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found taking this medication"}), 404

# Query patients by previous medication
@patient_bp.route("/patients/previous_medication/<medication>", methods=["GET"])
def get_patients_by_previous_medication(medication):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE previous_medication LIKE ?", ('%' + medication + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found with this previous medication"}), 404

# Query patients by next appointment date
@patient_bp.route("/patients/appointment/<appointment_date>", methods=["GET"])
def get_patients_by_appointment_date(appointment_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE next_appointment_date = ?", (appointment_date,))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"message": "No patients found with this appointment date"}), 404

# Query patients by provider
@patient_bp.route("/patients/provider/<provider>", methods=["GET"])
def get_patients_by_provider(provider):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE provider LIKE ?", ('%' + provider + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found under this provider"}), 404

# Query patients by doctor
@patient_bp.route("/patients/doctor/<doctor>", methods=["GET"])
def get_patients_by_doctor(doctor):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE doctor LIKE ?", ('%' + doctor + '%',))
    patients = cursor.fetchall()
    conn.close()

    if patients:
        return jsonify([dict(row) for row in patients])
    return jsonify({"error": "No patients found for this doctor"}), 404