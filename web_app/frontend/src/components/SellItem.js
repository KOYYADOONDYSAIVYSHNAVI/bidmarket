import React, { useState } from 'react';
import axios from 'axios'; // Import axios for making HTTP requests
import { v4 as uuidv4 } from 'uuid'; // Import uuid for generating unique IDs

const SellItem = () => {
  const [description, setDescription] = useState('');
  const [startingPrice, setStartingPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [shippingCost, setShippingCost] = useState('');
  const [category, setCategory] = useState('');
  const [keywords, setKeywords] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userID = localStorage.getItem('userId');
    if (!userID) {
      setMessage('You must be logged in to create an item.');
      return;
    }

    const itemData = {
      _id: uuidv4(), // Generate a unique ID
      user_id: userID,
      starting_price: parseFloat(startingPrice),
      quantity: parseInt(quantity, 10),
      shipping_cost: parseFloat(shippingCost),
      description,
      flagged: false,
      category,
      keywords: keywords.split(',').map(keyword => keyword.trim()), // Convert comma-separated string to array
    };

    try {
      const response = await axios.post('http://localhost:8081/items', itemData);
      console.log('Response:', response);
      setMessage(`Item created successfully! Item ID: ${response.data[0]}`);
      setDescription('');
      setStartingPrice('');
      setQuantity('');
      setShippingCost('');
      setCategory('');
      setKeywords('');
    } catch (error) {
      console.error('Error creating item:', error);
      setMessage('An error occurred while creating the item.');
    }
  };

  return (
    <div>
      <h2>Create Item</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Description:</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Starting Price:</label>
          <input
            type="number"
            value={startingPrice}
            onChange={(e) => setStartingPrice(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Quantity:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Shipping Cost:</label>
          <input
            type="number"
            value={shippingCost}
            onChange={(e) => setShippingCost(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Category:</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Keywords (comma-separated):</label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create Item</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SellItem;