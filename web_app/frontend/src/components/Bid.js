import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Bid = () => {
  const { auction_id } = useParams(); // Extract auction ID from URL
  const [auction, setAuction] = useState(null);
  const [bidAmount, setBidAmount] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch auction details
    const fetchAuction = async () => {
      try {
        const response = await axios.get(`http://localhost:8081/auctions/${auction_id}`);
        setAuction(response.data);
      } catch (error) {
        console.error('Error fetching auction:', error);
      }
    };

    fetchAuction();
  }, [auction_id]);

  const handleBid = async (e) => {
    e.preventDefault();

    const userID = localStorage.getItem('userId');
    if (!userID) {
      setMessage('You must be logged in to place a bid.');
      return;
    }

    const bidData = {
      auction_id,
      user_id: userID,
      bid_amount: parseFloat(bidAmount),
    };

    try {
      const response = await axios.post('http://localhost:8081/bids', bidData);
      setMessage(`Bid placed successfully! Bid ID: ${response.data._id}`);
      setBidAmount('');
    } catch (error) {
      console.error('Error placing bid:', error);
      setMessage('An error occurred while placing the bid.');
    }
  };

  return (
    <div>
      <h2>Place a Bid</h2>
      {auction ? (
        <div>
          <h3>{auction.description}</h3>
          <p>Starting Price: ${auction.starting_price}</p>
          <p>Current Highest Bid: ${auction.highest_bid}</p>
          <form onSubmit={handleBid}>
            <div>
              <label>Bid Amount:</label>
              <input
                type="number"
                value={bidAmount}
                onChange={(e) => setBidAmount(e.target.value)}
                required
              />
            </div>
            <button type="submit">Place Bid</button>
          </form>
        </div>
      ) : (
        <p>Loading auction details...</p>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default Bid;