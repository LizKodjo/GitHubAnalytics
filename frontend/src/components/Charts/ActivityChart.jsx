import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function ActivityChart({ userData }) {
  const { data } = userData;

  // Generate sample activity data (in the real app, this would come from GitHub events API)
  const generateActivityData = () => {
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];

    // Simulate activity based on user metrics
    const baseActivity = data.activity_score / 2;
    const commits = months.map(() =>
      Math.floor(Math.random() * 30 + baseActivity)
    );
    const prs = months.map(() =>
      Math.floor(Math.random() * 10 + baseActivity / 3)
    );
    const issues = months.map(() =>
      Math.floor(Math.random() * 8 + baseActivity / 4)
    );

    return { months, commits, prs, issues };
  };

  const activityData = generateActivityData();

  const chartData = {
    labels: activityData.months,
    datasets: [
      {
        label: "Commits",
        data: activityData.commits,
        borderColor: "#6e40c9",
        backgroundColor: "rgba(110, 64, 201, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Pull Requests",
        data: activityData.prs,
        borderColor: "#1a7f37",
        backgroundColor: "rgba(26, 127, 55, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Issues",
        data: activityData.issues,
        borderColor: "#db6d28",
        backgroundColor: "rgba(219, 109, 40, 0.1)",
        tension: 0.4,
        fill: true,
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
    },
  };
  return (
    <>
      <div className="github-card p-6">
        <h3 className="text-lg font-semibold mb-4">Activity Timeline</h3>
        <div className="h-64">
          <Line data={chartData} options={options} />
        </div>
      </div>
    </>
  );
}
