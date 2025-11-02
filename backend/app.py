# backend/app.py
from datetime import datetime
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
from flask import Flask, jsonify
import os
import sys

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


try:
    from config import settings
    print("✅ Config imported successfully!")
except ImportError as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY

    # Rate limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["100 per hour"],
        storage_uri="memory://"
    )

    # CORS
    CORS(app)

    # Import and register blueprints
    try:
        from backend.routes.analytics import analytics_bp
        app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')
        print("✅ Analytics routes registered!")
    except ImportError as e:
        print(f"⚠️  Could not register analytics routes: {e}")

    @app.route('/')
    def home():
        return jsonify({
            "message": "GitHub Analytics Pro API 🚀",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "endpoints": {
                "health": "/health",
                "user_analysis": "/api/v1/analytics/profile/<username>",
                "compare_users": "/api/v1/analytics/compare"
            }
        })

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "github-analytics"})

    return app


# if __name__ == '__main__':
#     print("🚀 Starting GitHub Analytics Pro API...")
#     print("📍 API URL: http://localhost:5000")
#     print("📍 Try these endpoints:")
#     print("   - http://localhost:5000/api/v1/analytics/profile/octocat")
#     print("   - http://localhost:5000/health")
#     app.run(debug=settings.DEBUG, host='0.0.0.0', port=5000)
