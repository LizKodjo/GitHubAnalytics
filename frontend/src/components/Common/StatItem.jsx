export default function StatItem({ label, value }) {
  return (
    <>
      <div className="flex justify-between items-center py-2 border-b border-github-border last:border-b-0">
        <span className="text-github-text-secondary">{label}</span>
        <span className="font-semibold">{value}</span>
      </div>
    </>
  );
}
