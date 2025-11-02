
#!/usr/bin/env python3
"""
Run script for GitHub Analytics Pro API
"""
from backend.app import create_app
import os
import sys

# Add current directory to path (optional, but safe)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting GitHub Analytics Pro API from run.py...")
    print("📍 API URL: http://localhost:5000")
    print("📍 Health: http://localhost:5000/health")
    # print("   - http://localhost:5000/api/v1/analytics/profile/octocat")
    app.run(debug=True, host='0.0.0.0', port=5000)
