export default function LoadingSpinner({ size = "large" }) {
  const sizeClasses = {
    small: "w-6 h-6",
    medium: "w-12 h-12",
    large: "w-16 h-16",
  };

  return (
    <>
      <div className="flex flex-col items-center justify-center space-y-4">
        <div
          className={`${sizeClasses[size]} border-4 border-primary-600 border-t-transparent rounded-full animate-spin`}
        ></div>
        <p className="text-github-text-secondary">
          Analysing GitHub profile...
        </p>
      </div>
    </>
  );
}
