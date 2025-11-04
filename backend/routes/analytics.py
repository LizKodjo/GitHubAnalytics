import asyncio
import logging
import traceback
from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Import services
try:
    from src.client.github_client import AsyncGitHubClient
    from src.services.advanced_analytics import AdvancedAnalyticsService
    from src.services.working_analytics_service import WorkingAnalyticsService as AnalyticsService
    # from src.services.simple_service import SimpleAnalyticsService as AnalyticsService
    # from src.services.analytics_service import AnalyticsService
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
    """Analyze a GitHub user profile with the working service"""
    print(f"🎯 Backend: Starting WORKING analysis for {username}")

    # Input validation
    if not username or len(username) > 39:
        return jsonify({"error": "Invalid username"}), 400

    try:
        async def perform_analysis():
            print(
                f"🔍 Backend: Creating client and WORKING service for {username}")
            client = AsyncGitHubClient()
            service = AnalyticsService(client)
            print(
                f"🚀 Backend: Starting WORKING analysis service for {username}")
            result = await service.get_comprehensive_analysis(username)
            print(f"✅ Backend: WORKING analysis completed for {username}")
            return result

        print(f"🔄 Backend: Running async analysis for {username}")
        analysis = asyncio.run(perform_analysis())
        print(f"📦 Backend: Analysis result ready for {username}")

        return jsonify({
            "success": True,
            "data": analysis.dict()
        })

    except Exception as e:
        print(f"💥 Backend: ERROR in WORKING analysis for {username}: {str(e)}")
        import traceback
        traceback.print_exc()

        error_message = str(e)
        if "not found" in error_message.lower():
            return jsonify({"error": f"GitHub user '{username}' not found"}), 404
        elif "rate limit" in error_message.lower():
            return jsonify({"error": "GitHub API rate limit exceeded"}), 429
        else:
            return jsonify({"error": f"Analysis failed: {error_message}"}), 500


@analytics_bp.route('/compare', methods=["POST"])
@analytics_limiter.limit("5 per minute")
def compare_users():
    """Compare multiple GitHub users"""
    data = request.get_json()

    if not data or 'usernames' not in data:
        return jsonify({"error": "Missing 'usernames' array in request body"}), 400

    usernames = data['usernames']
    if len(usernames) > 5:
        return jsonify({"error": "Maximum 5 users can be compared"}), 400
    if len(usernames) < 2:
        return jsonify({"error": "At least 2 usernames required"}), 400

    try:
        async def compare_all():
            client = AsyncGitHubClient()
            service = AnalyticsService(client)

            # Analyse all users concurrently
            tasks = [service.analyze_single_repository(
                username) for username in usernames]
            return await asyncio.gather(*tasks, return_exceptions=True)

        comparisons = asyncio.run(compare_all())

        comparison_data = []
        for i, result in enumerate(comparisons):
            if isinstance(result, Exception):
                comparison_data.append({
                    "username": usernames[i],
                    "success": False,
                    "error": str(result)
                })
            else:
                comparison_data.append({
                    "username": usernames[i],
                    "success": True,
                    "data": result.model_dump()
                })

        return jsonify({
            "success": True,
            "comparisons": comparison_data
        })
    except Exception as e:
        logger.error(f"Error comparing users: {e}")
        return jsonify({"error": "Comparison failed"}), 500


# Add this to backend/routes/analytics.py
@analytics_bp.route('/minimal/<username>')
def minimal_test(username):
    """Minimal test that should definitely work"""
    print(f"🧪 MINIMAL TEST for {username}")

    try:
        async def minimal_analysis():
            client = AsyncGitHubClient()

            # Just test basic GitHub API calls
            user_data = await client.get_user_profile(username)
            return {
                "success": True,
                "username": user_data.get('login'),
                "name": user_data.get('name'),
                "followers": user_data.get('followers'),
                "public_repos": user_data.get('public_repos')
            }

        result = asyncio.run(minimal_analysis())
        return jsonify(result)

    except Exception as e:
        print(f"💥 MINIMAL TEST failed: {e}")
        return jsonify({"error": f"Minimal test failed: {str(e)}"}), 500
