export default function FeatureCard({ icon, title, description }) {
  return (
    <>
      <div className="github-card p-6 text-center hover:transform hover:scale-105 transition-all duration-300">
        <div className="text-primary-600 mb-3 flex justify-center">{icon}</div>
        <h3 className="font-semibold mb-2">{title}</h3>
        <p className="text-github-text-secondary text-sm">{description}</p>
      </div>
    </>
  );
}
