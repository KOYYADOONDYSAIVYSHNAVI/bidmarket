from app.consumers import callback
import pytest
import time
import json

@pytest.fixture
def mock_send_email(mocker):
    return mocker.patch('app.consumers.send_email')

def test_item_watchlist_match(mock_send_email):
    message = json.dumps({
        "event_type": "item_watchlist_match",
        "user_email": "user@example.com",
        "item_description": "Vintage Watch"
    })
    
    callback(None, None, None, message)
    time.sleep(1)  

    mock_send_email.assert_any_call(
        'user@example.com', 
        'Item Matched Watchlist', 
        "The item 'Vintage Watch' matches your criteria."
    )

def test_new_bid_on_item(mock_send_email):
    message = json.dumps({
        "event_type": "new_bid_on_item",
        "seller_email": "seller@example.com",
        "item_description": "Vintage Watch"
    })
    callback(None, None, None, message)

    mock_send_email.assert_any_call(
        'seller@example.com', 
        'New Bid Placed', 
        "A bid has been placed on your item 'Vintage Watch'."
    )

def test_higher_bid(mock_send_email):
    message = json.dumps({
        "event_type": "higher_bid",
        "user_email": "buyer@example.com",
        "item_description": "Vintage Watch"
    })

    callback(None, None, None, message)

    mock_send_email.assert_any_call(
        'buyer@example.com', 
        'Higher Bid Alert', 
        "A higher bid has been placed on your item 'Vintage Watch'."
    )

def test_auction_time_alert(mock_send_email):
    message = json.dumps({
        "event_type": "auction_time_alert",
        "seller_email": "seller@example.com",
        "bidders_emails": ["bidder1@example.com", "bidder2@example.com"],
        "item_description": "Vintage Watch",
        "time_left": "1 day"
    })

    callback(None, None, None, message)

    mock_send_email.assert_any_call(
        'seller@example.com', 
        "Time Alert for Vintage Watch", 
        "Your auction for 'Vintage Watch' ends in 1 day."
    )
    parsed_message = json.loads(message)

    for bidder_email in parsed_message["bidders_emails"]:
        mock_send_email.assert_any_call(
            bidder_email, 
            "Time Alert for Vintage Watch", 
            "The auction for 'Vintage Watch' ends in 1 day."
        )
