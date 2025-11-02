import { Chart as ChartJS, ArcElement, Legend, Tooltip } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function LanguageChart({ userData }) {
  const { data } = userData;

  // Aggregate languarge data from all repositories
  const languageData = data.repository_analysis.reduce((acc, repo) => {
    Object.entries(repo, language_percentage).forEach(([lang, percentage]) => {
      acc[lang] = (acc[lang] || 0) + percentage;
    });
    return acc;
  }, {});

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
    },
    cutout: "60%",
  };

  return (
    <>
      <div className="github-card p-6">
        <h3 className="text-lg font-semibold mb-4">Language Distribution</h3>
        <div className="h-64">
          <Doughnut data={chartData} options={options} />
        </div>
      </div>
    </>
  );
}
