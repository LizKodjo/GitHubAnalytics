export default function InfoItem({ icon, label, value }) {
  return (
    <>
      <div className="flex items-center space-x-2">
        <div className="text-primary-600">{icon}</div>
        <div>
          <div className="text-xs text-github-text-secondary">{label}</div>
          <div className="text-sm font-medium">{value}</div>
        </div>
      </div>
    </>
  );
}
