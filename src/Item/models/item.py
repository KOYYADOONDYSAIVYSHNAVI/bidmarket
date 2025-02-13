from Item.consts.consts import ITEM_COLLECTION
import bson

class Item:
    def __init__(self, user_id: str, starting_price: float, quantity: int, shipping_cost: float, description: str,
                 flagged: bool = False,
                 category: str = None, keywords: list[str] = None, item_id=None, auction_id=None):
        self.id = item_id
        self.user_id = user_id
        self.starting_price = starting_price
        self.quantity = quantity
        self.shipping_cost = shipping_cost
        self.description = description
        self.flagged = flagged
        self.category = category
        self.keywords = keywords
        self.auction_id = auction_id

    def to_dict(self):
        return {"user_id": self.user_id, "starting_price": self.starting_price, "quantity": self.quantity,
                "shipping_cost": self.shipping_cost, "description": self.description, "flagged": self.flagged,
                "category": self.category, "keywords": self.keywords, "auction_id": self.auction_id,
                "_id": str(self.id)}

    @staticmethod
    def from_dict(data):
        return Item(user_id=data["user_id"], starting_price=data["starting_price"], quantity=data["quantity"],
                    shipping_cost=data["shipping_cost"], description=data["description"],
                    flagged=data["flagged"] if "flagged" in data else False,
                    category=data["category"] if "category" in data else None,
                    keywords=data["keywords"] if "keywords" in data else None,
                    auction_id=data["auction_id"] if "auction_id" in data else None,
                    item_id=data["_id"] if "_id" in data else None)

    def create(self, dao):
        create_dict = self.to_dict()
        del create_dict["_id"]
        return dao.write_to_db(ITEM_COLLECTION, create_dict)

    def update(self, dao):
        update_dict = self.to_dict()
        if "_id" in update_dict:
            del update_dict["_id"]
        return dao.update_db(ITEM_COLLECTION, {"_id": self.id}, {"$set": update_dict})

    @staticmethod
    def filter(dao, query):
        res = dao.read_from_db(ITEM_COLLECTION, query)
        return [Item.from_dict(r) for r in res]

    def delete(self, dao):
        res = dao.delete_from_db(ITEM_COLLECTION, {"_id": self.id})
        return res

    @staticmethod
    def get_by_id(dao, item_id):
        r = dao.read_from_db(ITEM_COLLECTION, {"_id": item_id})
        if r:
            return Item.from_dict(r[0])
        else:
            return None

    @staticmethod
    def get_all(dao):
        res = dao.read_from_db(ITEM_COLLECTION, {})
        return [Item.from_dict(r) for r in res]

    @staticmethod
    def get_by_user_id(dao, user_id):
        res = dao.read_from_db(ITEM_COLLECTION, {"user_id": user_id})
        return [Item.from_dict(r) for r in res]

    @staticmethod
    def get_by_category(dao, category):
        res = dao.read_from_db(ITEM_COLLECTION, {"category": category})
        return [Item.from_dict(r) for r in res]

    @staticmethod
    def get_by_keyword(dao, keyword):
        res = dao.read_from_db(ITEM_COLLECTION, {"keywords": {"$in": [keyword]}})
        return [Item.from_dict(r) for r in res]
