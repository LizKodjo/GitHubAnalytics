// const { default: axios } = require("axios");
import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const githubAnalyticsAPI = {
  // Get user profile analysis
  getUserProfile: async (username) => {
    const response = await api.get(`/analytics/profile/${username}`);
    return response.data;
  },

  // Compare multiple users
  compareUsers: async (usernames) => {
    const response = await api.post("/analytics/compare", { usernames });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get("/health");
    return response.data;
  },
};

export default api;
