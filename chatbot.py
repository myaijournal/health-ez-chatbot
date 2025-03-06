import sys
import requests
import streamlit as st
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import getpass
import os


from dotenv import load_dotenv

# Load .env file
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


messages = []

# Streamlit UI
st.title("HealthEZ Chatbot")
prompt = st.text_input("Ask me about your appointment or reschedule request")

# Tools
@tool(parse_docstring=True)
def get_next_appointment(patient_id: int) -> dict:
    """Fetches the next appointment date for a given patient. Call this whenever a patient wants to know their next scheduled appointment.

    Args:
        patient_id: The unique ID of the patient.

    Note: View JSON Schema: get_next_appointment.args_schema.schema()

    Returns:
        dict: A dictionary containing:
            - next_appointment_date (str): The scheduled next appointment date in YYYY-MM-DD format.
            - doctor (str): The name of the assigned doctor.
    """
    response = requests.get(f"http://127.0.0.1:5000/patients/id/{patient_id}")
    return response.json() if response.status_code == 200 else {"error": "Patient not found"}

@tool(parse_docstring=True)
def check_reschedule_status(patient_id: int) -> dict:
    """Checks the status of a patient's reschedule request. Call this whenever a patient wants to check if their reschedule request has been approved or pending.

    Args:
        patient_id: The unique patient ID.

    Note: View JSON Schema: check_reschedule_status.args_schema.schema()

    Returns:
        dict: A dictionary containing:
            - status (str): The current status of the reschedule request ("Pending", "Approved", or "Rejected").
            - requested_date (str): The newly requested appointment date in YYYY-MM-DD format.
    """
    response = requests.get(f"http://127.0.0.1:5000/reschedule_requests/{patient_id}")
    return response.json() if response.status_code == 200 else {"error": "No reschedule request found"}

@tool(parse_docstring=True)
def request_reschedule(patient_id: int, doctor_id: int, current_date: str, requested_date: str, note: str) -> dict:
    """Submits a reschedule request for an appointment. Call this whenever a patient wants to request a change to their scheduled appointment.

    Args:
        patient_id: The unique patient ID.
        doctor_id: The unique doctor ID.
        current_date: The current appointment date in YYYY-MM-DD format.
        requested_date: The newly requested appointment date in YYYY-MM-DD format.
        note: A brief reason for rescheduling.

    Note: View JSON Schema: request_reschedule.args_schema.schema()

    Returns:
        dict: A dictionary containing:
            - message (str): A confirmation message indicating successful submission.
    """
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "current_date": current_date,
        "requested_date": requested_date,
        "note": note
    }
    response = requests.post("http://127.0.0.1:5000/reschedule", json=payload)
    return response.json()

# Mapping tools
tools_list = {
    "get_next_appointment": get_next_appointment,
    "check_reschedule_status": check_reschedule_status,
    "request_reschedule": request_reschedule,
}

if prompt:
    llm = ChatOpenAI(model = "gpt-4o-mini")
    llm_with_tools = llm.bind_tools(list(tools_list.values()))

    messages.append(HumanMessage(prompt))
    ai_response = llm_with_tools.invoke(messages)
    messages.append(ai_response)

    if not ai_response.tool_calls:
        with st.container(height=500, border=True):
            st.write(ai_response.content)
            sys.exit()

    for tool_call in ai_response.tool_calls:
        selected_tool = tools_list.get(tool_call["name"].lower())
        tool_response = selected_tool.invoke(tool_call["args"])
        messages.append(ToolMessage(content= tool_response, tool_call_id=tool_call["id"]))

    final_response = llm_with_tools.stream(messages)
    with st.container(height=500, border=True):
        st.write_stream(final_response)
