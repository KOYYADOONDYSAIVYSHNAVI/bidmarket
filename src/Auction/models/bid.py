import datetime


class Bid:
    def __init__(self, user_id: str, bid_time: str, bid_amount: float):
        self.user_id = user_id
        self.bid_time = datetime.datetime.fromisoformat(bid_time)
        self.bid_amount = bid_amount

    def to_dict(self):
        return {"user_id": self.user_id, "bid_time": datetime.datetime.isoformat(self.bid_time),
                "bid_amount": self.bid_amount}

    @staticmethod
    def from_dict(bid_dict):
        return Bid(user_id=bid_dict["user_id"], bid_time=bid_dict["bid_time"],
                   bid_amount=bid_dict["bid_amount"])
