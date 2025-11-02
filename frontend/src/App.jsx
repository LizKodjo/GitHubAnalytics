import { useState } from "react";

import "./App.css";
import { useGitHubAnalytics } from "./hooks/useGitHubAnalytics";
import { GitBranch, Github, Star, Users } from "lucide-react";
import FeatureCard from "./components/Common/FeatureCard";
import SearchBar from "./components/Common/SearchBar";
import UserProfile from "./components/User/UserProfile";
import Header from "./components/Layout/Header";
import LoadingSpinner from "./components/Common/LoadingSpinner";
import UserStats from "./components/User/UserStats";
import RepositoryList from "./components/User/RepositoryList";
import LanguageChart from "./components/Charts/LanguageChart";
import SkillRadar from "./components/Charts/SkillRadar";
import ActivityChart from "./components/Charts/ActivityChart";
import StatItem from "./components/Common/StatItem";

function App() {
  const { userData, loading, error, analyzeUser, clearData } =
    useGitHubAnalytics();
  const [currentView, setCurrentView] = useState("overview");

  const handleSearch = async (username) => {
    try {
      await analyzeUser(username);
    } catch (error) {
      // Error handled in hook
    }
  };

  const handleClear = () => {
    clearData();
    setCurrentView("overview");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-github-dark flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <>
      <div className="min-h-screen bg-github-dark text-github-text-primary">
        <Header onClear={handleClear} />

        <main className="container mx-auto px-4 py-8">
          {!userData ? (
            <div className="text-center max-w-2xl mx-auto mt-16">
              <div className="flex justify-center mb-6">
                <div className="p-4 rounded-full bg-primary-600/20">
                  <Github className="2-12 h-12 text-primary-600" />
                </div>
              </div>
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-primary-600 to-blue-500 bg-clip-text text-transparent">
                GitHub Analytics Pro
              </h1>
              <p className="text-github-text-secondary text-lg mb-8">
                Advanced analytics and insights for GitHub profiles. Discover
                coding patterns, skill levels and community impact.
              </p>

              <SearchBar onSearch={handleSearch} />

              {error && <ErrorMessage message={error} className="mt-4" />}

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <FeatureCard
                  icon={<Star className="w-6 h-6" />}
                  title="Skill Assessment"
                  description="AI-powered analysis of programming expertise"
                />
                <FeatureCard
                  icon={<GitBranch className="w-6 h-6" />}
                  title="Repository Analytics"
                  description="Deep insights into your code projects"
                />
                <FeatureCard
                  icon={<Users className="w-6 h-6" />}
                  title="Community Imapact"
                  description="Measure your open-source influence"
                />
              </div>
            </div>
          ) : (
            // Results View
            <div className="space-y-6">
              {/* Navigation Tabs */}
              <div className="flex space-x-1 p-1 github-card rounded-lg w-fit">
                {["overview", "repositories", "analytics"].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setCurrentView(tab)}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                      currentView == tab
                        ? "bg-primary-600 text-white shadow-lg"
                        : "text-github-text-secondary hover:text-white hover:bg-github-border"
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
              {/* Content based on current view */}
              {currentView === "overview" && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2 space-y-6">
                    <UserProfile userData={userData} />
                    <UserStats userData={userData} />
                  </div>
                  <div className="space-y-6">
                    <SkillRadar userData={userData} />
                    <LanguageChart userData={userData} />
                  </div>
                </div>
              )}

              {currentView === "repositories" && (
                <RepositoryList userData={userData} />
              )}

              {currentView === "analytics" && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <LanguageChart userData={userData} />
                  <SkillRadar userData={userData} />
                  <ActivityChart userData={userData} />
                  <div className="github-card p-6">
                    <h3 className="text-lg font-semibold mb-4">Quick Stats</h3>
                    <div className="space-y-3">
                      <StatItem
                        label="Most Used Language"
                        value={data.primary_language[0] || "N/A"}
                      />
                      <StatItem
                        label="Total Projects"
                        value={data.metrics.repo_count}
                      />
                      <StatItem label="Skill Level" value={data.skill_level} />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </>
  );
}

export default App;
