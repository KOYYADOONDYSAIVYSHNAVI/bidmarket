import axios from 'axios';
import config from "../config";

const API_URL = config.ITEM_SERVICE_URL;

const getItems = async () => {
  const response = await axios.get(`${API_URL}/items`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`, 
    },
  });
  return response.data;
};

export default {
  getItems,
};
