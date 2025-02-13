import React, { useEffect, useState } from 'react';
import userService from '../services/userService'; // Service to interact with user microservice
import { useNavigate, useParams } from 'react-router-dom';

const Profile = () => {
  const [user, setUser] = useState({
    name: '',
    email: '',
    phoneNumber: '',
    address: '',
    userType: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { user_id } = useParams();

  const token = localStorage.getItem('token'); // Get token from localStorage

  useEffect(() => {
    if (!token) {
      navigate('/');
      return;
    }

    // Fetch the user profile from the backend
    const fetchProfile = async () => {
      try {
        const response = await userService.getProfile(token, user_id);
        setUser(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load profile');
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token, navigate]);

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    try {
      await userService.updateProfile(token, user_id, user);
      alert('Profile updated successfully');
    } catch (err) {
      setError('Failed to update profile');
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Profile</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form>
        <div>
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={user.name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={user.email}
            onChange={handleChange}
            disabled
          />
        </div>
        <div>
          <label>Phone Number:</label>
          <input
            type="text"
            name="phoneNumber"
            value={user.phoneNumber}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Address:</label>
          <input
            type="text"
            name="address"
            value={user.address}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>User Type:</label>
          <input
            type="text"
            name="userType"
            value={user.userType}
            onChange={handleChange}
          />
        </div>
        
        <button type="button" onClick={handleSave}>
          Save
        </button>
      </form>
    </div>
  );
};

export default Profile;
