import grpc
from app.grpc import user_pb2
from app.grpc import user_pb2_grpc
import json

def get_user_bids_from_auction(user_id):
    """Fetch active auctions where the user has placed bids."""
    with grpc.insecure_channel('localhost:50010') as channel:  # Auction Microservice gRPC server
        stub = user_pb2_grpc.AuctionServiceStub(channel)

        # Prepare the query to search for auctions where this user has placed a bid
        query = {"bids.user_id": user_id, "active": True}
        query_json = json.dumps(query)
        get_request = user_pb2.GetAuctionRequest(query=query_json)

        try:
            response = stub.GetAuctions(get_request)
            if response.success:
                return response.auctions  # Return the list of auctions
            else:
                return None  # Return None if no auctions are found or there's an error
        except grpc.RpcError as e:
            print(f"Error calling GetAuctions: {e}")
            return None

def create_auction(item_id, seller_id, starting_time, ending_time, starting_price):
    # Establish connection to the auction microservice's gRPC server
    channel = grpc.insecure_channel('localhost:50010')  # Assuming the auction microservice runs on port 5001
    stub = user_pb2_grpc.AuctionServiceStub(channel)

    # Prepare the request
    request = user_pb2.CreateAuctionRequest(
        item_id=item_id,
        seller_id=seller_id,
        starting_time=starting_time,
        ending_time=ending_time,
        starting_price=starting_price
    )

    # Call the CreateAuction RPC
    response = stub.CreateAuction(request)

    return response