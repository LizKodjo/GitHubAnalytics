import { TrendingUp, Users } from "lucide-react";
import { useState } from "react";
import ComparisonChart from "./ComparisonChart";
import ComparisonTable from "./ComparisonTable";

export default function ComparisonDashboard() {
  const [usernames, setUsernames] = useState(["", "", ""]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCompare = async () => {
    const validUsernames = usernames.filter((u) => u.trim());
    if (validUsernames.length < 2) {
      setError("Please enter at least 2 usernames");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/v11/analytics/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usernames: validUsernames }),
      });

      const data = await response.json();

      if (data.success) {
        setComparisonData(data);
      } else {
        setError(data.error || "Comparison failed");
      }
    } catch (error) {
      setError("Network error: Could not reach the server");
    } finally {
      setLoading(false);
    }
  };

  const addUserField = () => {
    if (usernames.lengt < 5) {
      setUsernames([...usernames, ""]);
    }
  };

  const removeUserField = (index) => {
    if (usernames.length > 2) {
      const newUsernames = usernames.filter((_, i) !== index);
      setUsernames(newUsernames);
    }
  };

  return (
    <>
      <div className="space-y-6">
        {/* Comparison Input Section */}
        <div className="github-card p-6">
          <div className="flex items-center space-x-3 mb-6">
            <Users className="w-6 h-6 text-primary-600" />
            <h2 className="tet-2xl font-bold">Compare Developers</h2>
          </div>

          <div className="spacy-y-4">
            {usernames.map((username, index) => (
              <div key={index} className="flex space-x-2">
                <input
                  type="text"
                  placeholder={`GitHub username ${index + 1}`}
                  value={username}
                  onChange={(e) => {
                    const newUsernames = [...usernames];
                    newUsernames[index] = e.target.value;
                    setUsernames(newUsernames);
                  }}
                  className="flex-1 p-3 github-card border border-github-border rounded-lg focus:border-primary-600 focus:outline-none"
                />
                {usernames.length > 2 && (
                  <button
                    onClick={() => removeUserField(index)}
                    className="px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
            {usernames.length < 5 && (
              <button
                onClick={addUserField}
                className="w-full p-3 border-2 border-dashed border-github-border text-github-text-secondary hover:text-white hover:border-primary-600 rounded-lg transition-colors"
              >
                + Add Another Developer
              </button>
            )}
            <button
              onClick={handleCompare}
              disabled={loading}
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold disabled:opacity-50 flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Comparing...</span>
                </>
              ) : (
                <>
                  <TrendingUp className="w-4 h-4" />
                  <span>Compare Developers</span>
                </>
              )}
            </button>

            {error && (
              <div className="p-3 bg-red-600/20 border border-red-600 rounded-lg text-red-400">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Comparison Results */}
        {comparisonData && (
          <div className="space-y-6">
            <ComparisonChart comparisonData={comparisonData} />
            <ComparisonTable comparisonData={comparisonData} />
          </div>
        )}
      </div>
    </>
  );
}
