import datetime
from concurrent import futures
import json
import grpc
from bson import ObjectId
from google.protobuf.json_format import (MessageToDict, )

from Auction.consts.consts import AUCTION_SERVICE_PORT
from Auction.dao.mongoDAO import MongoDao
from Auction.models.auction import Auction
from Auction.rpc import service_pb2, service_pb2_grpc
from Auction.task_scheduler.tasks import start_auction_task

class AuctionService(service_pb2_grpc.AuctionServiceServicer):
    def __init__(self, dao: MongoDao):
        self.dao = dao

    def CreateAuction(self, request, context):
        auction = Auction.from_dict(MessageToDict(request, preserving_proto_field_name=True))
        # create auction
        try:
            auction_id = auction.create(self.dao)[0]
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.CreateAuctionResponse(success=False, auction_id=auction.id, message=str(e))

        # schedule auction to start at starting_time
        try:
            start_auction_task.apply_async(args=[auction_id], countdown=(auction.starting_time - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds())

            return service_pb2.CreateAuctionResponse(success=True, auction_id=auction_id, message="")
        except Exception as e:
            # rollback
            auction.delete(self.dao)
            return service_pb2.CreateAuctionResponse(success=False, auction_id=auction.id, message=str(e))

    def UpdateAuction(self, request, context):
        try:
            auction = Auction.filter({"_id": request.auction_id}, self.dao)[0]
            # update auction
            auction_dict = auction.to_dict()
            msg_dict = MessageToDict(request, preserving_proto_field_name=True) # dict of updated fields
            del msg_dict["auction_id"]
            for key, value in msg_dict.items():
                if key in auction_dict:
                    auction_dict[key] = value
                else:
                    return service_pb2.UpdateAuctionResponse(success=False, modified_count=0,
                                                             message="Invalid field: " + key)
            auction = Auction.from_dict(auction_dict)
            modified_count = auction.update(self.dao)
        except Exception as e:
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0, message=str(e))

        # schedule auction to start at starting_time and revoke previous task
        try:
            auction_id = str(request.auction_id)
            start_auction_task.AsyncResult(auction_id).revoke()
            start_auction_task.apply_async(args=[auction_id], countdown=(auction.starting_time - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds())

            return service_pb2.UpdateAuctionResponse(success=True, modified_count=modified_count, message="")
        except Exception as e:
            return service_pb2.UpdateAuctionResponse(success=False, modified_count=0, message=str(e))

    def StartAuction(self, request, context):
        try:
            auction = Auction.filter({"_id": request.auction_id}, self.dao)[0]
            auction.start_auction(self.dao)
            return service_pb2.StartAuctionResponse(success=True, message="")
        except Exception as e:
            return service_pb2.StartAuctionResponse(success=False, message=str(e))

    def StopAuction(self, request, context):
        try:
            auction = Auction.filter({"_id": request.auction_id}, self.dao)[0]
            auction.stop_auction(self.dao)
            return service_pb2.StopAuctionResponse(success=True, message="")
        except Exception as e:
            return service_pb2.StopAuctionResponse(success=False, message=str(e))

    def PlaceBid(self, request, context):
        try:
            auction = Auction.filter({"_id": request.auction_id}, self.dao)[0]
            auction.place_bid(request.user_id, request.bid_amount, self.dao)
            return service_pb2.PlaceBidResponse(success=True, message="")
        except Exception as e:
            return service_pb2.PlaceBidResponse(success=False, message=str(e))

    def GetAuctions(self, request, context):
        try:
            query = json.loads(request.query)
            auctions = Auction.filter(query, self.dao)
            res = []
            for auction in auctions:
                auction = auction.to_dict()
                auction["_id"] = str(auction["_id"])
                res.append(auction)

            return service_pb2.GetAuctionResponse(success=True, auctions=res)
        except Exception as e:
            return service_pb2.GetAuctionResponse(success=False, auctions=[], message=str(e))

    def BuyItemNow(self, request, context):
        try:
            auction = Auction.filter({"_id": request.auction_id}, self.dao)[0]
            auction.buy_item_now(request.user_id, self.dao)
            return service_pb2.BuyItemNowResponse(success=True, message="")
        except Exception as e:
            return service_pb2.BuyItemNowResponse(success=False, message=str(e))


def start_server():
    dao = MongoDao()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f"[::]:{AUCTION_SERVICE_PORT}")
    service_pb2_grpc.add_AuctionServiceServicer_to_server(AuctionService(dao), server)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    start_server()
