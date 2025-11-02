import {
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  PointElement,
  RadialLinearScale,
  Tooltip,
} from "chart.js";
import { Radar } from "lucide-react";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

export default function SkillRadar({ userData }) {
  const { data } = userData;

  // Calculate skill metrics based on user data
  const calculateSkills = () => {
    const repos = data.repository_analysis;

    // Code quality
    const codeQuality = Math.min(
      data.metrics.average_stars * 10 + data.metrics.average_foks * 5,
      100
    );

    // Activity level
    const activityLevel = data.activity_score;

    // Community level
    const communityImpact = data.community_impact;

    // Project Scale
    const projectScale = Math.min(
      data.metrics.repo_count * 2 + data.metrics.total_repo_size_mb / 10,
      100
    );

    // Language Diversity
    const languageDiversity = Math.min(data.metrics.languages_used * 15, 100);

    // Experience level
    const accountAgeDays =
      (new Date() - new Date(data.joined_date)) / (1000 * 60 * 60 * 24);
    const experienceLevel = Math.min(accountAgeDays / 36.5, 100);

    return {
      codeQuality: Math.round(codeQuality),
      activityLevel: Math.round(activityLevel),
      communityImpact: Math.round(communityImpact),
      projectScale: Math.round(projectScale),
      languageDiversity: Math.round(languageDiversity),
      experienceLevel: Math.round(experienceLevel),
    };
  };

  const skills = calculateSkills();

  const chartData = {
    labels: [
      "Code Quality",
      "Activity Level",
      "Community Impact",
      "Project Scale",
      "Language Diversity",
      "Experience Level",
    ],
    datasets: [
      {
        label: "Skill Assessment",
        data: [
          skills.codeQuality,
          skills.activityLevel,
          skills.communityImpact,
          skills.projectScale,
          skills.languageDiversity,
          skills.experienceLevel,
        ],
        backgroundColor: "rgba(110, 64, 201, 0.2)",
        borderColor: "#6e40c9",
        borderWidth: 2,
        pointBackgroundColor: "#6e40c9",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#6e40c9",
      },
    ],
  };
  const options = {
    scales: {
      r: {
        angleLines: {
          color: "rgba(139, 148, 158, 0.3)",
        },
        grid: {
          color: "rgba(139, 148, 158, 0.3)",
        },
        pointLabels: {
          color: "#8b949e",
          font: {
            size: 11,
          },
        },
        ticks: {
          display: false,
          stepSize: 20,
        },
        min: 0,
        max: 100,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.label}: ${context.raw}%`;
          },
        },
      },
    },
    maintainAspectRatio: false,
  };

  return (
    <>
      <div className="github-card p-6">
        <h3 className="text-lg font-semibold mb-4">Skill Radar</h3>
        <div className="h-64">
          <Radar data={chartData} options={options} />
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
          {Object.entries(skills).map(([skill, value]) => (
            <div key={skill} className="flex justify-between">
              <span className="text-github-text-secondary capitalize">
                {skill.replace(/([A-Z])/g, " $1").trim()}:
              </span>
              <span className="font-semibold">{value}%</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
