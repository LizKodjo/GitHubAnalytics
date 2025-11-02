import { Award, Eye, GitBranch, Star, TrendingUp, Users } from "lucide-react";

export default function UserStats({ userData }) {
  const { data } = userData;
  const { metrics } = data;

  const stats = [
    {
      icon: <Star className="w-5 h-5" />,
      label: "Total Stars",
      value: metrics.total_stars,
      color: "text-yellow-400",
    },
    {
      icon: <GitBranch className="w-5 h-5" />,
      label: "Total Forks",
      value: metrics.total_forks,
      color: "text-green-400",
    },
    {
      icon: <Users className="w-5 h-5" />,
      label: "Followers",
      value: data.followers,
      color: "text-blue-400",
    },
    {
      icon: <Eye className="w-5 h-5" />,
      label: "Following",
      value: data.following,
      color: "text-purple-400",
    },
    {
      icon: <TrendingUp className="w-5 h-5" />,
      label: "Public Repos",
      value: data.public_repos,
      color: "text-orange-400",
    },
    {
      icon: <Award className="w-5 h-5" />,
      label: "Activity Score",
      value: `${Math.round(data.activity_score)}%`,
      color: "text-pink-400",
    },
  ];

  const scoreCards = [
    {
      label: "Activity Score",
      value: Math.round(data.activity_score),
      max: 100,
      color: "bg-blue-500",
    },
    {
      label: "Community Impact",
      value: Math.round(data.community_impact),
      max: 100,
      color: "bg-green-500",
    },
  ];

  return (
    <>
      <div className="space-y-6">
        {/* Main Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {stats.map((stat, index) => (
            <div key={index} className="github-card p-4 text-center">
              <div className={`${stat.color} mb-2 flex justify-center`}>
                {stat.icon}
              </div>
              <div className="text-2xl font-bold mb-1">{stat.value}</div>
              <div className="text-xs text-github-text-secondary">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
        {/* Score Progress Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scoreCards.map((card, index) => (
            <div key={index} className="github-card p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-github-text-secondary">
                  {card.label}
                </span>
                <span className="text-sm font-bold">{card.value}%</span>
              </div>
              <div className="w-full bg-github-border rounded-full h-2">
                <div
                  className={`${card.color} h2 rounded-full transition-all duration-500`}
                  style={{ width: `${card.value}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
        {/* Language Highlights */}
        <div className="github-card p-4">
          <h3 className="font-semibold mb-3">Primary Languages</h3>
          <div className="flex flex-wrap gap-2">
            {data.primary_languages.map((language, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-primary-600/20 text-primary-400 rounded-full text-sm font-medium"
              >
                {language}
              </span>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
