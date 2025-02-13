from flask import Flask, request, jsonify
from flask import current_app as app
from Item.models.item import Item
from werkzeug.exceptions import NotFound, BadRequest
from flask import Blueprint
from connectors.auction.auction_rpc_client import filter_auctions, create_auction
import bson
auction_api = Blueprint("auction", __name__)

@auction_api.route("/auctions", methods=["POST"])
def get_auctions_by_ids():
    data = request.json
    if "auction_ids" not in data:
        raise BadRequest("ids field is required")
    data = [bson.ObjectId(auction_id) for auction_id in data["auction_ids"]]
    query = {"_id": {"$in": data}}
    response = filter_auctions(query)

    return jsonify(response)

@auction_api.route("/auctions/create", methods=["POST"])
def create_auction_api():
    data = request.json
    response = create_auction(
        float(data["starting_price"]),
        data["starting_time"],
        data["ending_time"],
        data["seller_id"],
        data["item_id"],
        float(data["buy_now_price"])
    )

    return jsonify(response)
