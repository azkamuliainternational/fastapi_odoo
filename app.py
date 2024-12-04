from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Odoo server details
ODOO_URL = "http://localhost:8015"
DB_NAME = "odoo15"
USERNAME = "test"
PASSWORD = "123"

@app.post("/get_session_id")
def get_session_id():
    """Log in to Odoo and retrieve the session ID."""
    # Login endpoint
    login_url = f"{ODOO_URL}/web/session/authenticate"

    # Request payload
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": DB_NAME,
            "login": USERNAME,
            "password": PASSWORD,
        },
        "id": None,
    }

    # Make the request
    response = requests.post(login_url, json=payload)

    # Check for errors
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to authenticate with Odoo: {response.text}"
        )

    # Parse the response
    result = response.json().get("result")
    if not result or "session_id" not in result:
        raise HTTPException(status_code=400, detail="Failed to retrieve session ID")

    # Extract the session ID
    session_id = result["session_id"]
    return {"session_id": session_id}
