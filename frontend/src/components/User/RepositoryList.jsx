// src/components/User/RepositoryList.jsx
import { useState } from "react";
import { Code2 } from "lucide-react";
import RepositoryCard from "../Common/RepositoryCard";

export default function RepositoryList({ userData }) {
  const { data } = userData;
  const [sortBy, setSortBy] = useState("stars");
  const [filterLanguage, setFilterLanguage] = useState("all");

  console.log("📁 RepositoryList received data:", data); // Debug log

  // Check if we have valid data
  if (!data || !data.repository_analysis) {
    return (
      <div className="github-card p-8 text-center">
        <Code2 className="w-12 h-12 text-github-text-secondary mx-auto mb-4" />
        <p className="text-github-text-secondary">
          No repository data available
        </p>
        <p className="text-sm text-github-text-secondary mt-2">
          Data structure: {JSON.stringify(Object.keys(data || {}))}
        </p>
      </div>
    );
  }

  // Get unique languages for filter
  const languages = [
    "all",
    ...new Set(
      data.repository_analysis.map((repo) => repo.language).filter(Boolean)
    ),
  ];

  // Sort and filter repositories
  const sortedRepos = [...data.repository_analysis]
    .filter(
      (repo) => filterLanguage === "all" || repo.language === filterLanguage
    )
    .sort((a, b) => {
      switch (sortBy) {
        case "stars":
          return b.stars - a.stars;
        case "forks":
          return b.forks - a.forks;
        case "recent":
          return new Date(b.last_updated) - new Date(a.last_updated);
        case "name":
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

  console.log("📁 Sorted repositories:", sortedRepos.length); // Debug log

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="github-card p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-github-text-secondary mb-2">
              Sort by
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full github-card border border-github-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary-600"
            >
              <option value="stars">Most Stars</option>
              <option value="forks">Most Forks</option>
              <option value="recent">Recently Updated</option>
              <option value="name">Name</option>
            </select>
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-github-text-secondary mb-2">
              Filter by Language
            </label>
            <select
              value={filterLanguage}
              onChange={(e) => setFilterLanguage(e.target.value)}
              className="w-full github-card border border-github-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary-600"
            >
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang === "all" ? "All Languages" : lang}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Repository Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sortedRepos.map((repo, index) => (
          <RepositoryCard
            key={repo.name || index}
            repo={repo}
            username={data.username}
          />
        ))}
      </div>

      {sortedRepos.length === 0 && (
        <div className="github-card p-8 text-center">
          <Code2 className="w-12 h-12 text-github-text-secondary mx-auto mb-4" />
          <p className="text-github-text-secondary">
            No repositories found with the current filters.
          </p>
        </div>
      )}
    </div>
  );
}
