# System Architecture

## Overview

GitHub Analytics Pro follows a modern full-stack architecture with clear separation of concerns between frontend and backend.

## Backend Architecture

- **Flask**: REST API framework
- **Redis**: Caching and rate limiting
- **Pydantic**: Data validation and serialization
- **Async/await**: Non-blocking API calls to GitHub

## Frontend Architecture

- **React 18**: Component-based UI
- **Tailwind CSS**: Utility-first styling
- **Chart.js**: Data visualization
- **Axios**: HTTP client for API communication

## Data Flow

1. User enters GitHub username
2. Frontend calls backend API
3. Backend fetches data from GitHub API
4. Analytics service processes data
5. Results cached in Redis
6. Formatted data returned to frontend
7. Frontend renders visualizations
