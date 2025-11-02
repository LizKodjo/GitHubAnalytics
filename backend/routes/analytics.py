import asyncio
import logging
from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Import services
try:
    from src.client.github_client import AsyncGitHubClient
    from src.services.advanced_analytics import AdvancedAnalyticsService
    from src.services.analytics_service import AnalyticsService
    from src.utils.validators import validate_username
except ImportError as e:
    print(f"Warning: Could not import analytics modules: {e}")


logger = logging.getLogger(__name__)
analytics_bp = Blueprint('analytics', __name__)

# Initialize limiter for this blueprint
analytics_limiter = Limiter(
    get_remote_address,
    default_limits=["10 per minute"],
    storage_uri="memory://"
)


@analytics_bp.route('/profile/<username>')
@analytics_limiter.limit("10 per minute")
def analyze_profile(username):
    """Analyse a GitHub user profile"""
    # Simple validation
    if not username or len(username) > 39:
        return jsonify({"error": "Invalid username"}), 400

    try:
        async def perform_analysis():
            client = AsyncGitHubClient()
            service = AnalyticsService(client)
            return await service.analyze_user(username)

        analysis = asyncio.run(perform_analysis())

        return jsonify({
            "success": True,
            "data": analysis.model_dump()
        })

    except Exception as e:
        logger.error(f"Error analysing {username}: {e}")
        error_message = str(e)
        if 'not found' in error_message.lower():
            return jsonify({"error": f"GitHub user '{username}' not found"}), 404
        elif "rate limit" in error_message.lower():
            return jsonify({"error": "GitHub API rate limit exceeded"}), 429
        else:
            return jsonify({"error": "Failed to analyse profile"}), 500


@analytics_bp.route('/compare', methods=["POST"])
@analytics_limiter.limit("5 per minute")
def compare_profiles():
    """Compare multiple GitHub profiles"""
    data = request.get_json()

    if not data or 'usernames' not in data:
        return jsonify({"error": "Missing 'usernames' array in request body"}), 400

    usernames = data['usernames']
    if len(usernames) > 5:
        return jsonify({"error": "Maximum 5 users can be compared"}), 400

    try:
        async def compare_all():
            client = AsyncGitHubClient()
            service = AnalyticsService(client)

            # Analyse all users concurrently
            tasks = [service.analyze_user(username) for username in usernames]
            return await asyncio.gather(*tasks, return_exceptions=True)
        results = asyncio.run(compare_all())

        comparisons = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                comparisons.append({
                    "username": usernames[i],
                    "success": False,
                    "error": str(result)
                })
            else:
                comparisons.append({
                    "username": usernames[i],
                    "success": True,
                    "data": result.model_dump()
                })

        return jsonify({
            "success": True,
            "comparisons": comparisons
        })
    except Exception as e:
        logger.error(f"Error comparing users: {e}")
        return jsonify({"error": "Comparison failed"}), 500
