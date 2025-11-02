import { AlertCircle } from "lucide-react";

export default function ErrorMessage({ message, className = "" }) {
  return (
    <>
      <div className={`github-card border-l-4 border-red-500 p-4 ${className}`}>
        <div className="flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
          <div>
            <p className="text-red-400 font-medium">Error</p>
            <p className="text-github-text-secondary text-sm">{message}</p>
          </div>
        </div>
      </div>
    </>
  );
}
