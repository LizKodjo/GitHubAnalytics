import { Award, GitBranch, Star, TrendingUp, Users } from "lucide-react";

export default function ComparisonTable({ comparisonData }) {
  const successfulComparisons = comparisonData.comparisons.filter(
    (c) => c.success
  );

  const metrics = [
    {
      key: "activity_score",
      label: "Activity Score",
      icon: <TrendingUp className="w-4 h-4" />,
      format: (v) => `${Math.round(v)}%`,
    },
    {
      key: "community_impact",
      label: "Community Impact",
      icon: <Users className="w-4 h-4" />,
      format: (v) => `${Math.round(v)}%`,
    },
    {
      key: "followers",
      label: "Followers",
      icon: <Users className="w-4 h-4" />,
      format: (v) => v.toLocaleString(),
    },
    {
      key: "public_repos",
      label: "Public Repos",
      icon: <GitBranch className="2-4 h-4" />,
      format: (v) => v.toLocaleString(),
    },
    {
      key: "total_stars",
      label: "Total Stars",
      icon: <Star className="w-4 h-4" />,
      format: (v) => v.toLocaleString(),
    },
    {
      key: "total_forks",
      label: "Total Forks",
      icon: <GitBranch className="w-4 h-4" />,
      format: (v) => v.toLocaleString(),
    },
    {
      key: "skill_level",
      label: "Skill Level",
      icon: <Award className="w-4 h-4" />,
      format: (v) => v.charAt(0).toUpperCase() + v.slice(1),
    },
  ];

  return (
    <>
      <div className="github-card p-6 overflow-x-auto">
        <h3 className="text-lg font-semibold mb-4">Detailed Comparison</h3>
        <table className="w-full">
          <thead>
            <tr className="border-b border-github-border">
              <th className="text-left py-3 text-github-text-secondary">
                Metric
              </th>
              {successfulComparisons.map((user, index) => (
                <th key={index} className="text-center py-3">
                  <div className="flex items-center justify-center space-x-2">
                    <img
                      src={user.data.avatar_url}
                      alt={user.data.username}
                      className="w-6 h-6 rounded-full"
                    />
                    <span className="font-semibold">{user.data.username}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric, metricIndex) => (
              <tr
                key={metric.key}
                className="border-b border-github-border last:border-b-0"
              >
                <td className="py-3">
                  <div className="flex items-center space-x-2">
                    <div className="text-primary-600">{metric.icon}</div>
                    <span className="font-medium">{metric.label}</span>
                  </div>
                </td>
                {successfulComparisons.map((user, userIndex) => (
                  <td key={userIndex} className="py-3 text-center">
                    {metric.key === "total_stars" ||
                    metric.key === "total_forks"
                      ? metric.format(user.data.metrics[metric.key])
                      : metric.format(user.data[metric.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
