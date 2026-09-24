import os
from datetime import datetime, timezone

import jwt
import pytest
from dotenv import load_dotenv

from app import app

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_login_returns_jwt_with_identity_and_expiration(client):
    response = client.post(
        "/login",
        json={"username": "cphillips17", "password": "Hailmary400!"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data

    token = data["token"]

    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

    # Adjust thest to match your generated token structure
    assert decoded_token["username"] == "cphillips17"
    assert "sub" in decoded_token or "user_id" in decoded_token  # Depending on your implementation
    assert "exp" in decoded_token
    assert "iat" in decoded_token
    assert decoded_token["exp"] > decoded_token["iat"]  # Ensure expiration is after issued at