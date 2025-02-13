import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const Navbar = () => {
  const token = localStorage.getItem('token'); 
  const navigate = useNavigate();
  const location = useLocation(); // Get the current location
  const user_id = localStorage.getItem('userId');
  // Paths where the Navbar should not be displayed
  const excludedPaths = ['/', '/signup'];

  // Check if the current path is in the excluded paths
  if (excludedPaths.includes(location.pathname)) {
    return null; // Do not render Navbar
  }

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token from localStorage
    navigate('/'); // Redirect to login page
  };

  return (
    <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 20px', backgroundColor: '#f8f9fa' }}>
      <div>Hawkdev Auction</div>
      <ul style={{ display: 'flex', alignItems: 'center', listStyleType: 'none', padding: 0, margin: 0 }}>
        <li style={{ margin: '0 10px' }}>
          <Link to={`/profile/${user_id}`}>
            Profile
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <Link to="/items">
            Home
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <Link to={`/cart/${user_id}`}>
            Cart
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <Link to={`/sell-item/${user_id}`}>
            Sell Item
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <Link to={`/bidding/${user_id}`}>
            Bidding
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <Link to={`/watchlist/${user_id}`}>
            Watchlist
          </Link>
        </li>
        <li style={{ margin: '0 10px' }}>
          <button onClick={handleLogout}>
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;