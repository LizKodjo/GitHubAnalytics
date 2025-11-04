import { useEffect, useState } from "react";
import { githubAnalyticsAPI } from "../../services/api";
import { Check, Wifi, X } from "lucide-react";

export default function ConnectionTest() {
  const [connectionStatus, setConnectionStatus] = useState("checking");
  const [message, setMessage] = useState("");

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      setConnectionStatus("checking");
      setMessage("Testing backend connection...");

      const health = await githubAnalyticsAPI.healthCheck();

      if (health.status === "healthy") {
        setConnectionStatus("connected");
        setMessage("Backend connection successful");
      } else {
        setConnectionStatus("error");
        setMessage("Backend returned unexpected response");
      }
    } catch (error) {
      setConnectionStatus("error");
      setMessage(
        "Cannot connect to backend server.  Make sure it's running on port 5000."
      );
      console.error("Connection test failed: ", error);
    }
  };

  const getStatusIcon = () => {
    switch (connectionStatus) {
      case "connected":
        return <Check className="w-5 h-5 text-green-500" />;
      case "error":
        return <X className="w-5 h-5 text-red-500" />;
      default:
        return <Wifi className="w-5 h-5 text-yellow-500 animate-pulse" />;
    }
  };

  const getStatusColor = () => {
    switch (connectionStatus) {
      case "connected":
        return "border-green-500 bg-green-500/10";
      case "error":
        return "border-red-500 bg-red-500/10";
      default:
        return "border-yellow-500 bg-yellow-500/10";
    }
  };

  return (
    <>
      <div className={`bg-github-card p-4 border-l-4 ${getStatusColor()} mb-4`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {getStatusIcon()}
            <div>
              <p className="font-medium">Backend Connection</p>
              <p className="text-sm text-github-text-secondary">{message}</p>
            </div>
          </div>

          <button
            onClick={testConnection}
            className="px-3 py-1 text-sm bg-primary-600 hover:bg-primary-700 rounded transition-color"
          >
            Test Again
          </button>
        </div>
      </div>
    </>
  );
}
