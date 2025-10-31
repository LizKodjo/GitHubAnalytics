from datetime import datetime, timezone
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import sentry_sdk
from ..config import settings
from sentry_sdk.integrations.flask import FlaskIntegration

# Configrue logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialise Sentry for error tracking
# if settings.SENTRY_DSN:
#     sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FlaskIntegration()], traces_sample_rate=0.1)
    
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    
    # Security headers
    if not settings.DEBUG:
        Talisman(app, force_https=True)
        
    # Rate limiting
    limiter = Limiter(get_remote_address, app=app, default_limits=[f"{settings.RATE_LIMIT_PER_HOUR} per hour"], storage_uri="memory://")
    
    # CORS
    CORS(app)
    
    # Register blueprints
    # from .routes.analytics import analytics_bp
    from routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')
    
    # Home route
    @app.route('/')
    def home():
        return jsonify({
            "message": "GitHub Analytics Pro API",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "endpoints": {
                "health": "/health",
                "user_analysis": "/api/v1/analytics/profile/<username>",
                "compare_users":"/api/v1/analytics/compare"
            }
        })
    
  
    
    # Health check endpoint
    @app.route('/health')
    @limiter.exempt
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0"
        })
        
    # Error handlers
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Rate limit exceeded",
            "message": "Too many requests",
            "retry_after": 3600
        }), 429
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"Internal server error: {error}")
        return jsonify({
            "error": "Internal server error",
            "message": "Something went wrong on our end",
        }), 500
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=settings.DEBUG, host='0.0.0.0', port=5000)