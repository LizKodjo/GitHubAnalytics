import asyncio
import logging
from flask import Blueprint, jsonify, request
from flask_limiter import Limiter

# from ..  src.client.github_client import AsyncGitHubClient
from src.client.github_client import AsyncGitHubClient
from src.services.advanced_analytics import AdvancedAnalyticsService
from src.utils.validators import validate_username


logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__)
limiter = Limiter()

@analytics_bp.route('/profile/<username>')
@limiter.limit("10 per minute")
async def get_advanced_analysis(username):
    """Get comprehensive developer profile analysis"""
    # Input validation
    validation_error = validate_username(username)
    if validation_error:
        return jsonify({"error": validation_error}), 400
    
    try:
        # Run async function
        async def analyse():
            client = AsyncGitHubClient()
            service = AdvancedAnalyticsService(client)
            return await service.get_comprehensive_analysis(username)
        
        analysis = asyncio.run(analyse())
        
        return jsonify({
            "success": True,
            "data": analysis.model_dump(),
            "cache_hit": getattr(analysis, '_cache_hit', False)
        })
        
    except Exception as e:
        logger.error(f"Error analysing user {username}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
@analytics_bp.route('/compare', methods=["POST"])
@limiter.limit("5 per minute")
async def compare_developers():
    """Compare multiple developers"""
    data = request.get_json()
    
    if not data or 'usernames' not in data:
        return jsonify({"error": "usernames array required"}), 400
    
    usernames = data['usernames']
    if len(usernames) > 5:
        return jsonify({"error": "Maximun 5 users can be compared"}), 400
    
    try:
        async def compare_all():
            client = AsyncGitHubClient()
            service = AdvancedAnalyticsService(client)
            
            # Analyse all users concurrently
            tasks = [service.get_comprehensive_analysis(username) for username in usernames]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        comparisons = asyncio.run(compare_all())
        
        # Process results
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
                    "data": result.model_dump()})
                
        return jsonify({
            "success": True,
            "comparisons": comparison_data
        })
        
    except Exception as e:
        logger.error(f"Error comparing users: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400