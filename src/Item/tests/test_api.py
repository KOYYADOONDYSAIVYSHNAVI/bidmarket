import bson
import pytest
from flask import Flask
import bson
from unittest.mock import MagicMock, patch

# Import the app object from your Flask application
from Item.app import app

@pytest.fixture
def client():
    # Set up the Flask test client
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_dao():
    mock_dao = MagicMock()
    app.dao = mock_dao
    return mock_dao

@pytest.fixture
def mock_item1():
    return {"user_id": 1, "starting_price": 1.0, "quantity": 1, "shipping_cost": 1.0, "description": "New item", "flagged": False, "category": "New", "keywords": ["New", "Item"], "_id": "123", "auction_id": 1}

@pytest.fixture
def mock_item2():
    return {"user_id": 2, "starting_price": 2.0, "quantity": 2, "shipping_cost": 2.0, "description": "New item2", "flagged": False, "category": "New", "keywords": ["New", "Item"], "_id": "asdasdsa", "auction_id": 2}

@pytest.fixture
def mock_flagged_item():
    return {"user_id": 1, "starting_price": 1.0, "quantity": 1, "shipping_cost": 1.0, "description": "New item", "flagged": True, "category": "New", "keywords": ["New", "Item"], "_id": "123", "auction_id": 1}


def test_get_all_items(client, mock_dao, mock_item1, mock_item2):
    mock_dao.read_from_db.return_value = [mock_item1, mock_item2]
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json == [mock_item1, mock_item2]

def test_get_item_by_id_success(client, mock_dao, mock_item1):
    mock_dao.read_from_db.return_value = [mock_item1]
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json == mock_item1

def test_get_item_by_id_not_found(client, mock_dao):
    mock_dao.read_from_db.return_value = None
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "Item with ID 999 not found." in response.json["error"]

def test_create_item_success(client, mock_dao, mock_item1):
    mock_dao.write_to_db.return_value = [1]

    response = client.post("/items", json=mock_item1)
    assert response.status_code == 201
    assert response.json == [1]


def test_update_item_success(client, mock_dao, mock_item1):
    updated_item = mock_item1
    updated_item["starting_price"] = 2.0
    mock_dao.update_db.return_value = 1

    response = client.put("/items/1", json=updated_item)
    assert response.status_code == 200
    assert response.json == 1

def test_update_item_not_found(client, mock_dao, mock_item1):
    mock_dao.update_db.return_value = None
    response = client.put("/items/999", json=mock_item1)
    assert response.status_code == 404

def test_delete_item_success(client, mock_dao, mock_item1):
    mock_dao.delete_from_db.return_value = 1
    response = client.delete(f"/items/1")
    assert response.status_code == 200

def test_delete_item_not_found(client, mock_dao):
    mock_dao.read_from_db.return_value = None
    response = client.delete("/items/999")
    assert response.status_code == 404

def test_flag_item_success(client, mock_dao, mock_item1):
    flagged_item = mock_item1
    flagged_item["flagged"] = True
    mock_dao.read_from_db.return_value = [mock_item1]
    mock_dao.update_db.return_value = flagged_item

    response = client.put("/items/flag/1")
    assert response.status_code == 200
    assert response.json == flagged_item

def test_flag_item_not_found(client, mock_dao):
    mock_dao.read_from_db.return_value = None
    response = client.put("/items/flag/999")
    assert response.status_code == 404

def test_filter_items(client, mock_dao, mock_item1):
    mock_dao.read_from_db.return_value = [mock_item1]
    response = client.post("/items/filter", json={"query": {"user_id": "123"}})
    assert response.status_code == 200
    assert response.json == [mock_item1]