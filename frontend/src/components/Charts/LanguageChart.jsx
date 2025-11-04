import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const LanguageChart = ({ userData }) => {
  const { data } = userData;

  console.log("📊 LanguageChart received data:", data); // Debug log

  // Safely aggregate language data from all repositories
  const languageData = data.repository_analysis.reduce((acc, repo) => {
    // Check if language_percentages exists and is an object
    if (
      repo.language_percentages &&
      typeof repo.language_percentages === "object"
    ) {
      Object.entries(repo.language_percentages).forEach(
        ([lang, percentage]) => {
          acc[lang] = (acc[lang] || 0) + percentage;
        }
      );
    }
    return acc;
  }, {});

  console.log("📊 Aggregated language data:", languageData); // Debug log

  // If no language data, show a message
  if (Object.keys(languageData).length === 0) {
    return (
      <div className="github-card p-6">
        <h3 className="text-lg font-semibold mb-4">Language Distribution</h3>
        <div className="h-64 flex items-center justify-center">
          <p className="text-github-text-secondary">
            No language data available
          </p>
        </div>
      </div>
    );
  }

  const chartData = {
    labels: Object.keys(languageData),
    datasets: [
      {
        data: Object.values(languageData),
        backgroundColor: [
          "#6e40c9",
          "#1a7f37",
          "#d29922",
          "#db6d28",
          "#58a6ff",
          "#ea4aaa",
          "#3fb950",
          "#8b949e",
          "#ffd33d",
          "#f778ba",
        ],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#8b949e",
          font: {
            size: 11,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const label = context.label || "";
            const value = context.raw || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((value / total) * 100);
            return `${label}: ${percentage}%`;
          },
        },
      },
    },
    cutout: "60%",
  };

  return (
    <div className="github-card p-6">
      <h3 className="text-lg font-semibold mb-4">Language Distribution</h3>
      <div className="h-64">
        <Doughnut data={chartData} options={options} />
      </div>
    </div>
  );
};

export default LanguageChart;
