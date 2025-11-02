import { Github, Home } from "lucide-react";

export default function Header({ onClear }) {
  return (
    <>
      <header className="border-b border-github-border bg-github-card/50 backdrop-blur-sm sticky top-0z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-lg bg-primary-600">
                <Github className="w-6 rounded-lg bg-primary-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-primary-600 to-blue-500 bg-clip-text text-transparent">
                  GitHub Analytics Pro
                </h1>
                <p className="text-xs text-github-text-secondary">
                  Advanced developer insights
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={onClear}
                className="flex items-center space-x-2 px-4 py-2 text-github-text-secondary hover:text-white hover:bg-github-border rounded-lg transition-colors"
              >
                <Home className="w-4 h-4" />
                <span>New Search</span>
              </button>
            </div>
          </div>
        </div>
      </header>
    </>
  );
}
