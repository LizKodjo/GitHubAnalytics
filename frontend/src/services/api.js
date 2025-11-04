// const { default: axios } = require("axios");
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

console.log("🔗 API Base URL:", API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false,
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 Making API request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error("❌ API request error: ", error);
    return Promise.reject(error);
  }
);

// Request interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API response received from: `, response.status);
    return response;
  },
  (error) => {
    console.error("❌ API response error: ", error);

    if (error.response == "ECONNABORTED") {
      console.error(
        "⏰ Request timeout - backend is taking too long to respond."
      );
    }
    return Promise.reject(error);
  }
);

export const githubAnalyticsAPI = {
  // Get user profile analysis
  getUserProfile: async (username) => {
    try {
      console.log(`🔍 Fetching profile for: ${username}`);
      const response = await api.get(`/api/v1/analytics/profile/${username}`);
      return response.data;
    } catch (error) {
      console.error(`❌ Error fetching profile for ${username}:`, error);
      throw error;
    }
  },

  // Compare multiple users
  compareUsers: async (usernames) => {
    try {
      console.log(`🔍 Comparing users: `, usernames);
      const response = await api.post("/api/v1/analytics/compare", {
        usernames,
      });
      return response.data;
    } catch (error) {
      console.error("❌ Error comparing users: ", error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get("/health");
      return response.data;
    } catch (error) {
      console.error("❌ Health check failed: ", error);
      throw error;
    }
  },
};

export default api;
