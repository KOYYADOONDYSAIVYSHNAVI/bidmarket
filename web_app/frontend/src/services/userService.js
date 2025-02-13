import axios from 'axios';
import config from '../config';

const API_URL = config.USER_SERVICE_URL;

const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/users/signup`, userData, {
    headers: {
      'Content-Type': 'application/json',
    }
  });
  return response.data;
};

const login = async (userData) => {
    const response = await axios.post(`${API_URL}/users/`, userData);
    console.log('Login successful');
    localStorage.setItem('authToken', response.data.token);
    localStorage.setItem('userId', response.data.user_id)
    return response.data;
};

const logout = () => {
    localStorage.removeItem('authToken');
};


const getProfile = (token, userId) => {
    return axios.get(`${API_URL}/users/profile/${userId}`, {
        headers: {Authorization: `Bearer ${token}`},
    });
};

const updateProfile = (token, userId, data) => {
    return axios.put(`${API_URL}/users/profile/${userId}`, data, {
        headers: {Authorization: `Bearer ${token}`},
    });
};

const getCart = async (userId) => {
    const token = localStorage.getItem('authToken');
    const headers = {Authorization: `Bearer ${token}`};
    const response = await axios.get(`${API_URL}/users/cart/${userId}`, {headers});
    return response.data;
};

// Remove an item from the cart
const removeFromCart = async (userId, itemId) => {
    const token = localStorage.getItem('authToken');
    const headers = {Authorization: `Bearer ${token}`};
    const response = await axios.delete(`${API_URL}/users/cart/${userId}`, {
        headers,
        data: {item_id: itemId}, // Ensure backend handles this
    });
    return response.data;
};


const getItems = async (userId) => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error("User is not authenticated.");
    }

    const headers = {Authorization: `Bearer ${token}`};
    const response = await axios.get(`${API_URL}/users/bids/${userId}`, {headers});
    return response.data;
};

const createAuction = async (auctionData, sellerID) => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error("User is not authenticated.");
    }

    const headers = {Authorization: `Bearer ${token}`};
    const response = await axios.post(`${API_URL}/users/auctions/${sellerID}`, auctionData, {headers});
    return response.data;
};

const getWatchlist = async (userId) => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error("User is not authenticated.");
    }

    const headers = { Authorization: `Bearer ${token}` };
    const response = await axios.get(`${API_URL}/users/watchlist/${userId}`, { headers });
    return response.data;
};

// Add a new criteria to the watchlist
const addToWatchlist = async (userId, category_id, newCriteria) => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error("User is not authenticated.");
    }

    const headers = { Authorization: `Bearer ${token}` };
    const response = await axios.post(`${API_URL}/users/watchlist/${userId}/${category_id}`, newCriteria, { headers });
    return response.data;
};

// Delete a criteria from the watchlist
const deleteFromWatchlist = async (userId, category_id) => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error("User is not authenticated.");
    }

    const headers = { Authorization: `Bearer ${token}`, 'Content-Type':'application/json' };
    const response = await axios.delete(`${API_URL}/users/watchlist/${userId}/${category_id}`, { headers });
    return response.data;
};


export default {signup, login, logout, getProfile, updateProfile, getCart, removeFromCart, getItems, createAuction, addToWatchlist, getWatchlist, deleteFromWatchlist};