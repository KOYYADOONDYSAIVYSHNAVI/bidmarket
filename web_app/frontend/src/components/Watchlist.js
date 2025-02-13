import React, { useState, useEffect } from 'react';
import userService from '../services/userService'; // Assuming the file is in the services folder

const Watchlist = () => {
  const [watchlist, setWatchlist] = useState([]); // Ensure the initial state is an array
  const [newCriteria, setNewCriteria] = useState({ keyword: '', category: '', category_id: '', maxPrice: '' });
  const userId = localStorage.getItem('userId');

  // Fetch user's watchlist
  useEffect(() => {
    const fetchWatchlist = async () => {
      try {
        const data = await userService.getWatchlist(userId);
        console.log('Fetched data:', data); // Log the structure of the fetched data
        
        // Check if the data contains the watchlist array inside an object
        if (data && data.watchlist && Array.isArray(data.watchlist)) {
          setWatchlist(data.watchlist); // Only set state if 'watchlist' is an array
        } else {
          console.error('Watchlist data is not an array:', data);
          setWatchlist([]); // Fallback to empty array if not an array
        }
      } catch (error) {
        console.error('Error fetching watchlist:', error);
        setWatchlist([]); // Fallback to empty array on error
      }
    };

    fetchWatchlist();
  }, [userId]);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCriteria({ ...newCriteria, [name]: value });
  };

  // Add a new criterion to the watchlist
  const handleAddCriteria = async (e) => {
    e.preventDefault(); // Prevent form submission default behavior
    try {
        
      const { category_id, ...criteria } = newCriteria; // Extract categoryId, leave other criteria
      console.log('sending data', newCriteria);
      
      // Pass the categoryId as part of the URL and the remaining data in the request body
      const newItem = await userService.addToWatchlist(userId, category_id, criteria); // Passing categoryId separately
      
      // Ensure newItem is valid and append it to the current watchlist
      if (newItem && newItem.id) {
        setWatchlist((prevWatchlist) => [...prevWatchlist, newItem]); // Append the new item to the watchlist
      } else {
        console.error('Failed to add new item:', newItem);
      }
  
      // Clear the form fields
      setNewCriteria({ keyword: '', category: '', category_id: '', maxPrice: '' });
    } catch (error) {
      console.error('Error adding to watchlist:', error);
    }
  };

  // Delete a criterion from the watchlist
  const handleDeleteCriteria = async (category_id) => {
    try {
      await userService.deleteFromWatchlist(userId, category_id);
      setWatchlist((prev) => prev.filter((item) => item.category_id !== category_id)); // Update UI
    } catch (error) {
      console.error('Error deleting from watchlist:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Your Watchlist</h1>

      {/* Watchlist Display */}
      {Array.isArray(watchlist) && watchlist.length > 0 ? (
        <ul style={{ padding: 0, listStyle: 'none' }}>
          {watchlist.map((item) => (
            <li
              key={item.id}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '10px',
                border: '1px solid #ccc',
                marginBottom: '10px',
                borderRadius: '5px',
              }}
            >
              <div>
                <strong>Keyword:</strong> {item.keyword} | <strong>Category:</strong> {item.category} 
              </div>
              <button
                style={{
                  backgroundColor: 'red',
                  color: 'white',
                  border: 'none',
                  padding: '5px 10px',
                  cursor: 'pointer',
                  borderRadius: '5px',
                }}
                onClick={() => handleDeleteCriteria(item.category_id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No items in your watchlist.</p>
      )}

      {/* Add New Criteria Form */}
      <div style={{ marginTop: '20px' }}>
        <h2>Add New Criteria</h2>
        <form onSubmit={handleAddCriteria}>
          <div style={{ marginBottom: '10px' }}>
            <label>Keyword: </label>
            <input
              type="text"
              name="keyword"
              value={newCriteria.keyword}
              onChange={handleInputChange}
              required
              style={{ marginLeft: '10px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Category: </label>
            <input
              type="text"
              name="category"
              value={newCriteria.category}
              onChange={handleInputChange}
              required
              style={{ marginLeft: '10px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Category ID: </label>
            <input
              type="text"
              name="category_id"
              value={newCriteria.category_id}
              onChange={handleInputChange}
              required
              style={{ marginLeft: '10px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Max Price: </label>
            <input
              type="number"
              name="maxPrice"
              value={newCriteria.maxPrice}
              onChange={handleInputChange}
              required
              style={{ marginLeft: '10px' }}
            />
          </div>
          <button
            type="submit"
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              cursor: 'pointer',
              borderRadius: '5px',
            }}
          >
            Add to Watchlist
          </button>
        </form>
      </div>
    </div>
  );
};

export default Watchlist;
