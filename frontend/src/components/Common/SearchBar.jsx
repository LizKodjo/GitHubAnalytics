import { Search } from "lucide-react";
import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [username, setUsername] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (username.trim()) {
      onSearch(username.trim());
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit} className="w-full max-w-md mx-auto">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-github-text-secondary w-5 h-5" />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter GitHub username..."
            className="w-full pl-10 pr-4 py-3 github-card border-2 border-github-border rounded-xl focus:border-primary-600 focus:outline-none transition-colors"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-1 rounded-lg transition-colors"
          >
            Analyse
          </button>
        </div>
      </form>
    </>
  );
}
