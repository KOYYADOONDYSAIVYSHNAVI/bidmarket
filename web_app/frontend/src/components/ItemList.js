import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ItemList = () => {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchAllItems(); // Fetch all items instead of just recent ones
  }, []);

  const fetchAllItems = async () => {
    try {
      // Fetch all items from the item microservice
      const response = await fetch('http://localhost:8081/items');
      const data = await response.json();
      
      // Set the state with the fetched items
      setItems(data);

      // Check the fetched items with the user's watchlist
      await checkWithWatchlist(data);
    } catch (error) {
      console.error('Error fetching items:', error);
      setMessage('Error fetching items.');
    }
  };

  const checkWithWatchlist = async (allItems) => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      setMessage('User not authenticated.');
      return;
    }

    try {
      // Send each item to the user microservice to check if it matches the watchlist criteria
      for (const item of allItems) {
        const response = await axios.post(
          `http://localhost:8082/api/users/item_watchlist_match/${userId}`, 
          {
            keyword: item.keywords,     // Use appropriate item attribute(s)
            category: item.category,
            starting_price: item.starting_price,
          }
        );

        // If a match is found, trigger appropriate actions (e.g., notifications)
        if (response.data.matchFound) {
          console.log(`Match found for item: ${item.description}`);
          // Trigger a notification or email here (could call another service)
        }
      }
    } catch (error) {
      console.error('Error checking with watchlist:', error);
      setMessage('Error checking with watchlist.');
    }
  };

  return (
    <div>
      <h2>Available Items</h2>
      {message && <p>{message}</p>}
      <ul>
        {items.map((item) => (
          <li key={item._id}>
            {item.description} - {item.category}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ItemList;
