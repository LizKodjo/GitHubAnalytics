import { useState } from "react";
import { githubAnalyticsAPI } from "../services/api";

export const useGitHubAnalytics = () => {
  const [userData, setUserData] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeUser = async (username) => {
    setLoading(true);
    setError(null);

    try {
      const data = await githubAnalyticsAPI.getUserProfile(username);
      setUserData(data);
      return data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.error || "Failed to analyse user";
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const compareUsers = async (usernames) => {
    setLoading(true);
    setError(null);

    try {
      const data = await gethubAnalyticsAPI.compareUsers(usernames);
      setComparisonData(data);
      return data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.error || "Failed to compare users";
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
  };

  return {
    userData,
    comparisonData,
    loading,
    error,
    analyzeUser,
    compareUsers,
    clearData,
  };
};
