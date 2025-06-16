import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5050";

export const getPrice = async (symbol) => {
  const res = await axios.get(`${API_BASE_URL}/price/${symbol}`);
  return res.data;
};

export const getSpotBalance = async (symbol) => {
  const res = await axios.get(`${API_BASE_URL}/spot_balance/${symbol}`);
  return res.data;
};
