from flask import Blueprint, jsonify, request
from app.utils.db import get_db_connection

reschedule_bp = Blueprint("reschedule", __name__)

@reschedule_bp.route("/reschedule", methods=["POST"])
def request_reschedule():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reschedule_requests (patient_id, doctor_id, current_date, requested_date, note) VALUES (?, ?, ?, ?, ?)",
        (data["patient_id"], data["doctor_id"], data["current_date"], data["requested_date"], data.get("note", ""))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Reschedule request submitted successfully"}), 201

@reschedule_bp.route("/reschedule_requests/<int:patient_id>", methods=["GET"])
def get_reschedule_status(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT request_id, current_date, requested_date, status, note FROM reschedule_requests WHERE patient_id = ?", (patient_id,))
    requests = cursor.fetchall()
    conn.close()
    
    if requests:
        return jsonify([dict(row) for row in requests])
    return jsonify({"message": "No reschedule requests found for this patient."}), 404
