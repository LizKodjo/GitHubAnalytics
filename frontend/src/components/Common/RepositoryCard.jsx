import { Calendar, ExternalLink, Eye, GitBranch, Star } from "lucide-react";

export default function RepositoryCard({ repo, username }) {
  console.log("📄 RepositoryCard rendering:", repo.name); // Debug log

  const formatDate = (date) => {
    try {
      return new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch (e) {
      return "Invalid date";
    }
  };

  const getPopularityColor = (score) => {
    if (!score && score !== 0) return "text-github-text-secondary";
    if (score > 50) return "text-green-400";
    if (score > 20) return "text-yellow-400";
    return "text-github-text-secondary";
  };

  // Safely calculate popularity score
  const popularityScore =
    repo.popularity_score !== undefined
      ? repo.popularity_score
      : (repo.stars * 2 + repo.forks) / (repo.size_kb / 1000 + 1);

  return (
    <div className="github-card p-4 hover:border-primary-600 transition-all duration-300 group">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-lg group-hover:text-primary-400 transition-colors truncate">
            {repo.name || "Unnamed Repository"}
          </h3>
          {repo.language && (
            <div className="flex items-center space-x-2 mt-1">
              <div className="w-3 h-3 rounded-full bg-primary-600"></div>
              <span className="text-sm text-github-text-secondary">
                {repo.language}
              </span>
            </div>
          )}
        </div>
        <a
          href={`https://github.com/${username}/${repo.name}`}
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 text-github-text-secondary hover:text-primary-600 hover:bg-primary-600/10 rounded-lg transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>

      {repo.description && (
        <p className="text-github-text-secondary text-sm mb-4 line-clamp-2">
          {repo.description}
        </p>
      )}

      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1 text-github-text-secondary">
            <Star className="w-4 h-4" />
            <span>{repo.stars || 0}</span>
          </div>
          <div className="flex items-center space-x-1 text-github-text-secondary">
            <GitBranch className="w-4 h-4" />
            <span>{repo.forks || 0}</span>
          </div>
          <div className="flex items-center space-x-1 text-github-text-secondary">
            <Eye className="w-4 h-4" />
            <span className={getPopularityColor(popularityScore)}>
              {Math.round(popularityScore)}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-1 text-github-text-secondary">
          <Calendar className="w-4 h-4" />
          <span className="text-xs">{formatDate(repo.last_updated)}</span>
        </div>
      </div>

      {/* Language Distribution Bar */}
      {repo.language_percentages &&
        Object.keys(repo.language_percentages).length > 0 && (
          <div className="mt-3">
            <div className="flex h-2 rounded-full overflow-hidden">
              {Object.entries(repo.language_percentages)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 4)
                .map(([lang, percentage], index) => (
                  <div
                    key={lang}
                    className="h-full"
                    style={{
                      width: `${percentage}%`,
                      backgroundColor: getLanguageColor(lang),
                    }}
                    title={`${lang}: ${percentage.toFixed(1)}%`}
                  />
                ))}
            </div>
          </div>
        )}
    </div>
  );
}

// Helper function for language colors
const getLanguageColor = (language) => {
  const colors = {
    JavaScript: "#f1e05a",
    Python: "#3572A5",
    Java: "#b07219",
    TypeScript: "#2b7489",
    "C++": "#f34b7d",
    PHP: "#4F5D95",
    Ruby: "#701516",
    Go: "#00ADD8",
    Rust: "#dea584",
    CSS: "#563d7c",
    HTML: "#e34c26",
    Swift: "#ffac45",
    Kotlin: "#F18E33",
    Default: "#6e40c9",
  };
  return colors[language] || colors.Default;
};
