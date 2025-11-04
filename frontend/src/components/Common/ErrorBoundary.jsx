import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by boundary: ", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <>
          <div className="github-card p-6 border-l-4 border-red-500">
            <h2 className="text-lg font-semibold text-red-400 mb-2">
              Something went wrong
            </h2>
            <p className="text-github-text-secondary mb-4">
              There was an error rendering this component.
            </p>
            <details className="text-sm">
              <summary className="cursor-pointer mb-2">Error details</summary>
              <pre className="bg-github-border p-3 rounded overflow-auto text-xs">
                {this.state.error?.toString()}
              </pre>
            </details>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded transition-colors"
            >
              Try Again
            </button>
          </div>
        </>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
