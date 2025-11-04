import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function ({ comparisonData }) {
  const successfulComparisons = comparisonData.comparisons.filter(
    (c) => c.success
  );

  const chartData = {
    labels: successfulComparisons.map((c) => c.data.username),
    datasets: [
      {
        label: "Activity Score",
        data: successfulComparisons.map((c) => c.data.activity_score),
        backgroundColor: "rgba(110, 64, 201, 0.8)",
      },
      {
        label: "Community Impact",
        data: successfulComparisons.map((c) => c.data.community_impact),
        backgroundColor: "rgba(26, 127, 55, 0.8)",
      },
      {
        label: "Total Stars",
        data: successfulComparisons.map(
          (c) => c.data.metrics.total_stars / 100
        ),
        backgroundColor: "rgba(210, 09, 40, 0.8)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#8b949e",
        },
      },
      title: {
        display: true,
        text: "Developer Comparison",
        color: "#f0f6fc",
      },
    },
    scales: {
      x: {
        grid: {
          color: "rgba(139, 148, 158, 0.3)",
        },
        ticks: {
          color: "#8b949e",
        },
      },
      y: {
        grid: {
          color: "rgba(139, 148, 158, 0.3)",
        },
        ticks: {
          color: "#8b949e",
        },
      },
    },
  };

  return (
    <>
      <div className="github-card p-6">
        <h3 className="text-lg font-semibold mb-4">Metrics Comparison</h3>
        <div className="h-80">
          <Bar data={chartData} options={options} />
        </div>
      </div>
    </>
  );
}
