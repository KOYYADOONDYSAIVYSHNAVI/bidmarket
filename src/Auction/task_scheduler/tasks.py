from __future__ import absolute_import

from bson import ObjectId

from Auction.dao.mongoDAO import MongoDao
from Auction.models.auction import Auction
from Auction.task_scheduler.celery import app


@app.task
def start_auction_task(auction_id: str):
    try:
        dao = MongoDao()
        auction = Auction.filter({"_id": ObjectId(auction_id)}, dao)[0]
        auction.start_auction(dao)

        return True
    except Exception as e:
        print(e)
        return False


@app.task
def create_auction_task(auction_dict: dict):
    try:
        dao = MongoDao()
        auction = Auction.from_dict(auction_dict)
        auction.create(dao)

        return True
    except Exception as e:
        print(e)
        return False
