import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from app.models.user import User
from db import db
from werkzeug.security import generate_password_hash
import jwt
import datetime
import uuid

@pytest.fixture(scope="module")
def test_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test_userdb'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()  
    with app.app_context():
        yield app.test_client()
    with app.app_context():
        db.session.remove()
        db.drop_all()  

def test_signup(test_client):
    email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    
    response = test_client.post("/api/users/signup", json={
        "username": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "address": "Test Address",
        "password": "password123",
        "user_type": "buyer"
    })
    assert response.status_code == 201  

def test_login(test_client):
    email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"  
    test_client.post("/api/users/signup", json={
        "username": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "address": "Test Address",
        "password": "password123",
        "user_type": "buyer"
    })
    
    response = test_client.post("/api/users/", json={
        "email": email,
        "password": "password123"
    })
    assert response.status_code == 200  

def test_login_invalid_credentials(test_client):
    response = test_client.post("/api/users/", json={
        "email": "nonexistentuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401  


def test_get_profile(test_client):
    email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    response = test_client.post("/api/users/signup", json={
        "username": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "address": "Test Address",
        "password": "password123",
        "user_type": "buyer"
    })
    assert response.status_code == 201  
    
    login_response = test_client.post("/api/users/", json={
        "email": email,
        "password": "password123"
    })
    assert login_response.status_code == 200  
    token = login_response.json['token']  
    
    
    response = test_client.get(f"/api/users/profile/{uuid.uuid4()}", headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200  
    assert 'name' in response.json
    assert 'email' in response.json
    assert 'phoneNumber' in response.json
    assert 'address' in response.json
    assert 'userType' in response.json

def test_get_profile_invalid_token(test_client):
    response = test_client.get("/api/users/profile/invalid_user_id", headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == 401  
    assert response.json["message"] == "Invalid token"

def test_update_profile(test_client):
    email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    response = test_client.post("/api/users/signup", json={
        "username": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "address": "Test Address",
        "password": "password123",
        "user_type": "buyer"
    })
    assert response.status_code == 201  
    
    login_response = test_client.post("/api/users/", json={
        "email": email,
        "password": "password123"
    })
    assert login_response.status_code == 200  
    token = login_response.json['token']  
    
    updated_data = {
        "name": "Updated User",
        "phone_number": "9876543210",
        "address": "Updated Address",
        "user_type": "seller",
        "password": "newpassword123"
    }
    response = test_client.put(f"/api/users/profile/{uuid.uuid4()}", json=updated_data, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200  
    assert response.json["message"] == "Profile updated successfully"

def test_update_profile_invalid_token(test_client):
    updated_data = {
        "name": "Updated User",
        "phone_number": "9876543210",
        "address": "Updated Address",
        "user_type": "seller",
        "password": "newpassword123"
    }
    response = test_client.put("/api/users/profile/invalid_user_id", json=updated_data, headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == 401  
    assert response.json["message"] == "Invalid token"

def test_update_profile_missing_field(test_client):
    email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    response = test_client.post("/api/users/signup", json={
        "username": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "address": "Test Address",
        "password": "password123",
        "user_type": "buyer"
    })
    assert response.status_code == 201  
    
    
    login_response = test_client.post("/api/users/", json={
        "email": email,
        "password": "password123"
    })
    assert login_response.status_code == 200  
    token = login_response.json['token']  
    
    updated_data = {
        "name": "Updated User",
        "phone_number": "9876543210",
        "user_type": "seller"
    }
    response = test_client.put(f"/api/users/profile/{uuid.uuid4()}", json=updated_data, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200  
    assert response.json["message"] == "Profile updated successfully"

