from flask import Flask, request, jsonify
from flask import current_app as app
from flask_cors import CORS
from Item.models.item import Item
from werkzeug.exceptions import NotFound, BadRequest
from flask import Blueprint



item_api = Blueprint("item", __name__)
CORS(item_api)

@item_api.route("/items", methods=["GET"])
def get_all_items():
    try:
        items = Item.get_all(app.dao)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@item_api.route("/items/filter", methods=["POST"])
def filter_items():
    try:
        items = Item.filter(app.dao, request.json)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/<item_id>", methods=["GET"])
def get_item_by_id(item_id):
    try:
        item = Item.get_by_id(app.dao, item_id)
        if not item:
            raise NotFound(f"Item with ID {item_id} not found.")
        return jsonify(item.to_dict()), 200
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/user/<user_id>", methods=["GET"])
def get_items_by_user_id(user_id):
    try:
        items = Item.get_by_user_id(app.dao, user_id)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/category/<category>", methods=["GET"])
def get_items_by_category(category):
    try:
        items = Item.get_by_category(app.dao, category)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/keyword/<keyword>", methods=["GET"])
def get_items_by_keyword(keyword):
    try:
        items = Item.get_by_keyword(app.dao, keyword)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items", methods=["POST"])
def create_item():
    try:
        if not request.json:
            raise BadRequest("Request body must be JSON.")
        item = Item.from_dict(request.json)
        created_item_id = item.create(app.dao)
        return jsonify(created_item_id), 201
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    try:
        if not request.json:
            raise BadRequest("Request body must be JSON.")
        item = Item.from_dict(request.json)
        item.id = item_id
        updated_item_count = item.update(app.dao)
        if not updated_item_count:
            raise NotFound(f"Item with ID {item_id} not found for update.")
        return jsonify(updated_item_count), 200
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        item = Item.get_by_id(app.dao, item_id)
        if not item:
            raise NotFound(f"Item with ID {item_id} not found.")
        item.delete(app.dao)
        return jsonify({"message": f"Item with ID {item_id} deleted."}), 200
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@item_api.route("/items/flag/<item_id>", methods=["PUT"])
def flag_item(item_id):
    try:
        item = Item.get_by_id(app.dao, item_id)
        if not item:
            raise NotFound(f"Item with ID {item_id} not found.")
        item.flagged = True
        updated_item = item.update(app.dao)
        return jsonify(updated_item), 200
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500