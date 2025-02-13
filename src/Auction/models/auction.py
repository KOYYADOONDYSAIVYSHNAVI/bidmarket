import datetime

from bson import ObjectId
from google.protobuf.json_format import MessageToDict

from Auction.consts.consts import AUCTIONS_COLLECTION
from Auction.dao.mongoDAO import MongoDao
from Auction.models.bid import Bid
from Auction.service_connectors.user_connector import UserConnector
from Auction.service_connectors.item_connector import ItemConnector


class Auction:
    def __init__(self, item_id, seller_id, starting_time: str, ending_time: str, starting_price: float,
                 current_price: float, buy_now_price: float = None, active: bool = False, bids: list[Bid] = None,
                 auction_id=None):
        self.id = auction_id
        self.item_id = item_id
        self.seller_id = seller_id
        self.active = active
        self.starting_time = datetime.datetime.fromisoformat(starting_time)
        self.ending_time = datetime.datetime.fromisoformat(ending_time)
        self.starting_price = starting_price
        self.current_price = current_price
        self.buy_now_price = buy_now_price
        self.bids = bids

    def to_dict(self):
        return {"_id": str(self.id), "item_id": self.item_id, "seller_id": self.seller_id, "active": self.active,
                "starting_time": datetime.datetime.isoformat(self.starting_time),
                "ending_time": datetime.datetime.isoformat(self.ending_time), "starting_price": self.starting_price,
                "current_price": self.current_price, "bids": self.bids,
                "buy_now_price": self.buy_now_price if self.buy_now_price else None}

    @staticmethod
    def from_dict(auction_dict: dict):
        auction = Auction(item_id=auction_dict["item_id"],
                          seller_id=auction_dict["seller_id"],
                          active=auction_dict["active"] if "active" in auction_dict else False,
                          starting_time=auction_dict["starting_time"],
                          ending_time=auction_dict["ending_time"],
                          starting_price=float(auction_dict["starting_price"]),
                          current_price=float(auction_dict["current_price"]) if "current_price" in auction_dict else
                          auction_dict["starting_price"],
                          bids=auction_dict["bids"] if "bids" in auction_dict else [],
                          buy_now_price=float(
                              auction_dict["buy_now_price"]) if "buy_now_price" in auction_dict and auction_dict["buy_now_price"] else None,
                          auction_id=auction_dict["_id"] if "_id" in auction_dict else None)

        return auction

    def create(self, dao: MongoDao) -> list[str]:
        create_dict = self.to_dict()
        del create_dict["_id"]
        response = dao.write_to_db(AUCTIONS_COLLECTION, create_dict)

        # update item with auction id
        item_connector = ItemConnector()
        item = item_connector.get_item_by_id(self.item_id)
        item["auction_id"] = response[0]
        item_connector.update_item(self.item_id, item)

        return response

    def update(self, dao: MongoDao) -> int:
        update_dict = self.to_dict()
        del update_dict["_id"]
        return dao.update_db(AUCTIONS_COLLECTION, {"_id": self.id}, {"$set": update_dict})

    @staticmethod
    def filter(query: dict, dao: MongoDao) -> list:
        if "_id" in query and not isinstance(query["_id"], ObjectId):
            query["_id"] = ObjectId(query["_id"])
        res = dao.read_from_db(AUCTIONS_COLLECTION, query)
        return [Auction.from_dict(auction) for auction in res]

    def delete(self, dao: MongoDao):
        return dao.delete_from_db(AUCTIONS_COLLECTION, {"_id": self.id})

    def start_auction(self, dao: MongoDao):
        # validate auction
        valid, msg = self._validate_auction()
        if not valid:
            raise Exception(msg)

        # update auction status
        query = {"_id": self.id}
        update = {"$set": {"active": True}}
        return dao.update_db(AUCTIONS_COLLECTION, query, update)

    def stop_auction(self, dao: MongoDao):
        query = {"_id": self.id}
        update = {"$set": {"active": False}}
        return dao.update_db(AUCTIONS_COLLECTION, query, update)

    def place_bid(self, user_id: str, bid_amount: float, dao: MongoDao):
        bid = Bid(user_id=user_id, bid_amount=bid_amount,
                  bid_time=datetime.datetime.isoformat(datetime.datetime.now(tz=datetime.timezone.utc)))
        if not self.active:
            raise Exception("Auction is not active")

        if bid.bid_amount > self.current_price:  # todo race condition
            self.current_price = bid.bid_amount
            self.bids.append(bid.to_dict())
            self.update(dao)
        else:
            raise Exception("Bid amount must be greater than current price")

    def buy_item_now(self, user_id: str, dao: MongoDao):
        user_connector = UserConnector()
        try:
            user_connector.add_item_to_shopping_cart(user_id, self.item_id)
        except Exception as e:
            raise Exception(f"Could not add item to shopping cart. Error: {str(e)}")

        self.stop_auction(dao)

    def _validate_auction(self) -> (bool, str):
        if self.starting_time > self.ending_time:
            return False, "Ending time must be after starting time"
        if self.starting_price < 0:
            return False, "Starting price must be positive"
        if self.current_price < 0:
            return False, "Current price must be positive"

        return True, ""
