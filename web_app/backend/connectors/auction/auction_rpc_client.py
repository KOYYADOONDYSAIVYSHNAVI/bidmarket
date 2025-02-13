import datetime
import json

import grpc
from google.protobuf.json_format import MessageToDict

import web_app.backend.connectors.auction.service_pb2 as service_pb2
import web_app.backend.connectors.auction.service_pb2_grpc as service_pb2_grpc

SERVER_ADDRESS = 'localhost:50010'


def filter_auctions(query):
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = service_pb2_grpc.AuctionServiceStub(channel)

        json_query = json.dumps(query)
        get_request = service_pb2.GetAuctionRequest(query=json_query)
        get_response = stub.GetAuctions(get_request)

        return get_response


def create_auction(starting_price, starting_time, ending_time, seller_id, item_id, buy_now_price=None):
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = service_pb2_grpc.AuctionServiceStub(channel)

        create_request = service_pb2.CreateAuctionRequest(
            starting_price=starting_price,
            starting_time=datetime.datetime.isoformat(starting_time) if isinstance(starting_time,
                                                                                   datetime.datetime) else starting_time,
            ending_time=datetime.datetime.isoformat(ending_time) if isinstance(ending_time,
                                                                               datetime.datetime) else ending_time,
            seller_id=seller_id,
            item_id=item_id,
            buy_now_price=buy_now_price
        )
        create_response = MessageToDict(stub.CreateAuction(create_request))

        return create_response

# def run():
#     # Connect to the server
#     with grpc.insecure_channel('localhost:50010') as channel:
#         # Create a stub (client)
#         stub = service_pb2_grpc.AuctionServiceStub(channel)
#
#         # Get auctions by seller_id
#         query = {"seller_id": "zxcv"}
#         json_query = json.dumps(query)
#         get_request = service_pb2.GetAuctionRequest(query=json_query)
#         get_response = stub.GetAuctions(get_request)
#         print(f"GetAuctions response: {get_response}")
#
#         # Create an auction, all fields listed here are required
#         create_request = service_pb2.CreateAuctionRequest(
#             starting_price=100.00,
#             starting_time=datetime.datetime.isoformat(
#                 datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=20)),
#             ending_time="2024-12-31T12:00:00Z",
#             seller_id='zxcv',
#             item_id='zxcva'
#         )
#         create_response = stub.CreateAuction(create_request)
#         print(f"CreateAuction response: {create_response}")
#
#         # Update an auction, add a buy now price to enable the buy now feature
#         update_request = service_pb2.UpdateAuctionRequest(auction_id=create_response.auction_id, buy_now_price=500.00)
#         update_response = stub.UpdateAuction(update_request)
#         print(f"UpdateAuction response: {update_response}")
#
#         # Start auction
#         start_request = service_pb2.StartAuctionRequest(auction_id=create_response.auction_id)
#         start_response = stub.StartAuction(start_request)
#         print(f"StartAuction response: {start_response}")
#
#         # Place bid
#         place_bid_request = service_pb2.PlaceBidRequest(auction_id=create_response.auction_id, user_id='aaaz1',
#                                                         bid_amount=200.00)
#         place_bid_response = stub.PlaceBid(place_bid_request)
#         print(f"PlaceBid response: {place_bid_response}")
#
#         # Buy now
#         buy_now_request = service_pb2.BuyItemNowRequest(auction_id=create_response.auction_id, user_id='aaaz1')
#         buy_now_response = stub.BuyItemNow(buy_now_request)
#         print(f"BuyItemNow response: {buy_now_response}")
#
#
#         # Stop auction
#         stop_request = service_pb2.StopAuctionRequest(auction_id=create_response.auction_id)
#         stop_response = stub.StopAuction(stop_request)
#         print(f"StopAuction response: {stop_response}")
#
#         # Get the created auction
#         query = {"_id": create_response.auction_id}
#         json_query = json.dumps(query)
#         get_request = service_pb2.GetAuctionRequest(query=json_query)
#         get_response = stub.GetAuctions(get_request)
#         print(f"GetAuction response: {get_response}")
