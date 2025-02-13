import React, {useEffect, useState} from 'react';
import {Button, Card, Col, Container, Form, ListGroup, Modal, Row} from 'react-bootstrap';
import {useNavigate, useParams} from 'react-router-dom';
import config from '../config';

const convertDateToLocalISOString = (date) => {
    const pad = num => num.toString().padStart(2, '0'); // Ensures two digits
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

const setAuctionDetails = async (auctionId, item) => {
    try {
        const response = await fetch(`${config.AUCTION_SERVICE_URL}/auctions/${auctionId}`);
        const data = await response.json();
        item.current_price = data.current_price;
        item.starting_time = data.starting_time;
        item.ending_time = data.ending_time;
        item.active = data.active;
        item.bids = data.bids;
        item.buy_now_price = data.buy_now_price;


        return item;
    } catch (error) {
        console.error('Failed to fetch auction details', error);
    }
}


const CreateAuctionForm = ({showModal, handleCloseModal, itemId, userId}) => {
    const [auctionDetails, setAuctionDetails] = useState({
        startingPrice: 100,
        startingTime: convertDateToLocalISOString(new Date()),
        endingTime: convertDateToLocalISOString(new Date(Date.now() + 1000 * 60 * 60 * 24)), // 24 hours from now
        buyNowPrice: 0,
    });

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${config.AUCTION_SERVICE_URL}/auctions/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    starting_price: auctionDetails.startingPrice,
                    starting_time: new Date(auctionDetails.startingTime).toISOString(),
                    ending_time: new Date(auctionDetails.endingTime).toISOString(),
                    seller_id: userId,
                    item_id: itemId,
                    buy_now_price: auctionDetails.buyNowPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to create auction');
            }

            const updatedItem = await response.json();
            handleCloseModal();
            window.location.reload();
        } catch (error) {
            console.error('Failed to create auction', error);
        }
    };

    return (
        <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header closeButton>
                <Modal.Title>Create Auction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleFormSubmit}>
                    <Form.Group controlId="startingPrice">
                        <Form.Label>Starting Price</Form.Label>
                        <Form.Control
                            type="number"
                            step="0.01"
                            min="0"
                            value={auctionDetails.startingPrice}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, startingPrice: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="startingTime">
                        <Form.Label>Starting Time</Form.Label>
                        <Form.Control
                            type="datetime-local"
                            value={auctionDetails.startingTime}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, startingTime: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="endingTime">
                        <Form.Label>Ending Time</Form.Label>
                        <Form.Control
                            type="datetime-local"
                            value={auctionDetails.endingTime}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, endingTime: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="buyNowPrice">
                        <Form.Label>Buy Now Price</Form.Label>
                        <Form.Control
                            type="number"
                            step="0.01"
                            min="0"
                            value={auctionDetails.buyNowPrice}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, buyNowPrice: e.target.value})
                            }
                        />
                    </Form.Group>


                    <Button variant="primary" type="submit" className="mt-3">
                        Create Auction
                    </Button>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseModal}>
                    Cancel
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

const PlaceBidForm = ({showModal, handleCloseModal, itemId, auctionId, userId}) => {
    const [bidAmount, setBidAmount] = useState(0);

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${config.AUCTION_SERVICE_URL}/auctions/place_bid`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    auction_id: auctionId,
                    user_id: userId,
                    item_id: itemId,
                    bid_amount: bidAmount,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to place bid');
            }

            handleCloseModal();
            window.location.reload();
        } catch (error) {
            console.error('Failed to place bid', error);
        }
    };

    return (
        <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header closeButton>
                <Modal.Title>Place Bid</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleFormSubmit}>
                    <Form.Group controlId="bidAmount">
                        <Form.Label>Bid Amount</Form.Label>
                        <Form.Control
                            type="number"
                            step="0.01"
                            min="0"
                            value={bidAmount}
                            onChange={(e) => setBidAmount(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Button variant="primary" type="submit" className="mt-3">
                        Place Bid
                    </Button>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseModal}>
                    Cancel
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

const Bidding = () => {
    const [items, setItems] = useState([]);
    const [showCreateAuctionModal, setShowCreateAuctionModal] = useState(false);
    const [showPlaceBidModal, setShowPlaceBidModal] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const navigate = useNavigate();
    const {user_id} = useParams();

    const handleCloseModal = () => {
        setShowCreateAuctionModal(false);
        setShowPlaceBidModal(false);
    }
    const handleShowCreateAuctionModal = (item) => {
        setSelectedItem(item);
        setShowCreateAuctionModal(true);
    };

    const handleShowPlaceBidModal = (item) => {
        setSelectedItem(item);
        setShowPlaceBidModal(true);
    }

    const handleBuyNow = async (item) => {
        if (!window.confirm('Are you sure you want to buy now?')) {
            return;
        }
        try {
            const response = await fetch(`${config.AUCTION_SERVICE_URL}/auctions/buy_now/${item.auction_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    user_id: user_id,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to buy now');
            }
            const cartResponse = await fetch(`${config.USER_SERVICE_URL}/users/cart/${user_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    item_id: item._id,
                    user_id: user_id,
                    quantity: 1,  // Default to 1, unless you want to support selecting a quantity
                }),
            });
    
            if (!cartResponse.ok) {
                throw new Error('Failed to add item to cart');
            }
    
            // Optionally, show a success message or update the UI without reloading
            alert('Item successfully purchased and added to your cart!');
            window.location.reload();

        } catch (error) {
            console.error('Failed to buy now', error);
        }
    }

    const handleDeleteItem = async (item) => {
        if (!window.confirm('Are you sure you want to delete this item?')) {
            return;
        }
        try {
            const response = await fetch(`${config.ITEM_SERVICE_URL}/items/${item._id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete item');
            }

            window.location.reload();
        } catch (error) {
            console.error('Failed to delete item', error);
        }
    }

    const handleFlagItem = async (item) => {
        if (!window.confirm('Are you sure you want to flag this item?')) {
            return;
        }
        try {
            const response = await fetch(`${config.ITEM_SERVICE_URL}/items/flag/${item._id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to flag item');
            }

            window.location.reload();
        } catch (error) {
            console.error('Failed to flag item', error);
        }
    }

    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await fetch(`${config.ITEM_SERVICE_URL}/items`);
                const data = await response.json();
                for (let item of data) {
                    if (item.auction_id) {
                        await setAuctionDetails(item.auction_id, item);
                    }
                }
                setItems(data);
            } catch (error) {
                console.error('Failed to fetch items', error);
            }
        };

        fetchItems();
    }, []);

    return (
        <Container className="mt-4">
            <h2 className="mb-4">Items</h2>
            <Row>
                {items.length === 0 ? (
                    <Col>
                        <p>No items available</p>
                    </Col>
                ) : (
                    items.map((item) => (
                        <Col key={item._id} md={4} className="mb-4">
                            <Card className={`h-100 ${item.flagged ? 'bg-info text-white' : ''}`}>
                                <Card.Body>
                                    <Card.Title>{item.description}</Card.Title>
                                    <Card.Text>
                                        <strong>Category:</strong> {item.category}
                                        <br/>
                                        <strong>Keywords:</strong> {item.keywords.join(', ')}
                                        <br/>
                                        <strong>Starting Price:</strong> ${item.starting_price}
                                        <br/>
                                        <strong>Flagged:</strong> {item.flagged ? 'Yes' : 'No'}
                                        <br/>
                                        <strong>Seller:</strong> {item.user_id}
                                        <br/>
                                        {item.auction_id ? (
                                            <>
                                                <br/>
                                                <strong>Current Price:</strong> ${item.current_price}
                                                <br/>
                                                <strong>Starting
                                                    Time:</strong> {new Date(item.starting_time).toLocaleString()}
                                                <br/>
                                                <strong>Ending
                                                    Time:</strong> {new Date(item.ending_time).toLocaleString()}
                                                <br/>
                                                <strong>Auction
                                                    Status:</strong> {item.active ? 'Active' : 'Inactive'}
                                                <br/>
                                                {item.buy_now_price && (
                                                    <>
                                                        <strong>Buy Now Price:</strong> ${item.buy_now_price}
                                                        <br/>
                                                    </>
                                                )
                                                }
                                            </>
                                        ) : null}
                                    </Card.Text>
                                    {item.auction_id && item.bids ? (
                                        <>
                                            <strong>Bids:</strong>
                                            <ListGroup>
                                                {item.bids.map((bid) => (
                                                    <ListGroup.Item key={bid.bid_time + bid.user_id}>
                                                        ${bid.bid_amount} by {bid.user_id} at {new Date(bid.bid_time).toLocaleString()}
                                                    </ListGroup.Item>
                                                ))}
                                            </ListGroup>
                                        </>
                                    ) : null}

                                    {item.auction_id ? (
                                        <>
                                            <Button
                                                variant="success"
                                                onClick={() => handleShowPlaceBidModal(item)}
                                                className="ms-2"
                                            >
                                                Place Bid
                                            </Button>
                                            {item.buy_now_price && (
                                                <Button
                                                    variant="warning"
                                                    onClick={() => handleBuyNow(item)}
                                                    className="ms-2"
                                                >
                                                    Buy Now
                                                </Button>
                                            )}
                                        </>
                                    ) : (
                                        <>
                                            <Button
                                                variant="primary"
                                                onClick={() => handleShowCreateAuctionModal(item)}
                                                className="ms-2"
                                            >
                                                Create Auction
                                            </Button>
                                            <Button
                                                variant="warning"
                                                onClick={() => handleFlagItem(item)}
                                                className="ms-2"
                                            >
                                                Flag Item
                                            </Button>
                                            {item.user_id === user_id && (
                                                <Button
                                                    variant="danger"
                                                    onClick={() => handleDeleteItem(item)}
                                                    className="ms-2"
                                                >
                                                    Delete Item
                                                </Button>
                                            )}
                                        </>
                                    )}

                                </Card.Body>
                            </Card>
                        </Col>
                    ))
                )}
            </Row>

            {/* Modal for creating auction */}
            {selectedItem && (
                <CreateAuctionForm
                    showModal={showCreateAuctionModal}
                    handleCloseModal={handleCloseModal}
                    itemId={selectedItem._id}
                    userId={user_id}
                />
            )}

            {/* Modal for placing bid */}
            {selectedItem && (
                <PlaceBidForm
                    showModal={showPlaceBidModal}
                    handleCloseModal={handleCloseModal}
                    itemId={selectedItem._id}
                    auctionId={selectedItem.auction_id}
                    userId={user_id}
                />
            )}
        </Container>
    );
};

export default Bidding;