// src/hooks/useGitHubAnalytics.js
import { useState, useEffect } from "react";
import { githubAnalyticsAPI } from "../services/api";

export const useGitHubAnalytics = () => {
  const [userData, setUserData] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);

  // Test backend connection on component mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      console.log("🔗 Checking backend connection...");
      await githubAnalyticsAPI.healthCheck();
      console.log("✅ Backend connection successful");
    } catch (error) {
      console.error("❌ Backend connection failed:", error);
      setError(
        "Cannot connect to the backend server. Make sure it's running on port 5000."
      );
    }
  };

  const analyzeUser = async (username) => {
    if (!username || username.trim() === "") {
      setError("Please enter a GitHub username");
      return;
    }

    console.log("🎯 Starting analysis for:", username);
    setLoading(true);
    setError(null);
    setUserData(null);
    setProgress(10);

    try {
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return 90;
          return prev + 15;
        });
      }, 1000);

      const data = await githubAnalyticsAPI.getUserProfile(username);

      clearInterval(progressInterval);
      setProgress(100);

      console.log("📦 API response:", data);

      if (data && data.success) {
        console.log("✅ Analysis successful");
        setUserData(data);

        // Reset progress after showing completion
        setTimeout(() => setProgress(0), 500);
      } else {
        throw new Error(data?.error || "Analysis failed");
      }

      return data;
    } catch (err) {
      console.error("💥 Analysis error:", err);
      setProgress(0);

      let errorMessage = "Failed to analyze user";

      if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.code === "ECONNABORTED") {
        errorMessage =
          "Request timeout - analysis is taking too long. Please try again.";
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const clearData = () => {
    setUserData(null);
    setComparisonData(null);
    setError(null);
    setProgress(0);
  };

  return {
    userData,
    comparisonData,
    loading,
    error,
    progress,
    analyzeUser,
    clearData,
  };
};
