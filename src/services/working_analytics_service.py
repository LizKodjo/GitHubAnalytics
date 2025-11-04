# src/services/working_analytics_service.py
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
from ..client.github_client import AsyncGitHubClient
from ..models import DeveloperProfile, RepositoryAnalysis, SkillLevel


class WorkingAnalyticsService:
    """Analytics service that definitely works - based on the minimal test"""

    def __init__(self, client: AsyncGitHubClient):
        self.client = client

    async def get_comprehensive_analysis(self, username: str) -> DeveloperProfile:
        """Working analysis based on the minimal test approach"""
        try:
            print(f"🔍 WORKING: Starting analysis for {username}")

            # Get user data and repositories
            user_data = await self.client.get_user_profile(username)
            repos_data = await self.client.get_user_repositories(username)

            print(
                f"✅ WORKING: Got {len(repos_data)} repositories for {username}")

            # Create basic repository analyses
            repo_analyses = []
            for repo in repos_data[:10]:  # Limit to 10 repos for performance
                try:
                    # Try to get languages, but skip if it fails
                    languages = {}
                    try:
                        languages = await self.client.get_repository_languages(username, repo['name'])
                    except Exception as lang_error:
                        print(
                            f"⚠️  Could not get languages for {repo['name']}: {lang_error}")

                    analysis = RepositoryAnalysis(
                        name=repo['name'],
                        stars=repo.get('stargazers_count', 0),
                        forks=repo.get('forks_count', 0),
                        language=repo.get('language'),
                        language_percentages=languages,
                        last_updated=datetime.fromisoformat(
                            repo['updated_at'].replace('Z', '+00:00')),
                        has_issues=repo.get('has_issues', False),
                        has_wiki=repo.get('has_wiki', False),
                        is_fork=repo.get('fork', False),
                        size_kb=repo.get('size', 0)
                    )
                    repo_analyses.append(analysis)
                    print(f"✅ Analyzed repository: {repo['name']}")

                except Exception as e:
                    print(
                        f"⚠️  Failed to analyze repo {repo.get('name', 'unknown')}: {e}")
                    continue

            # Calculate metrics
            metrics = self._calculate_metrics(user_data, repos_data)
            primary_languages = self._get_primary_languages(repos_data)
            skill_level = self._calculate_skill_level(metrics)
            activity_score = self._calculate_activity_score(repos_data)
            community_impact = self._calculate_community_impact(metrics)

            # Create the profile
            profile = DeveloperProfile(
                username=user_data['login'],
                name=user_data.get('name'),
                avatar_url=user_data.get('avatar_url'),
                joined_date=datetime.fromisoformat(
                    user_data['created_at'].replace('Z', '+00:00')),
                public_repos=user_data.get('public_repos', 0),
                followers=user_data.get('followers', 0),
                following=user_data.get('following', 0),
                primary_languages=primary_languages,
                skill_level=skill_level,
                repository_analysis=repo_analyses,
                activity_score=activity_score,
                community_impact=community_impact,
                metrics=metrics
            )

            print(f"🎉 WORKING: Successfully created profile for {username}")
            return profile

        except Exception as e:
            print(f"❌ WORKING: Error analyzing {username}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def _calculate_metrics(self, user_data: Dict[str, Any], repos_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate basic metrics"""
        total_stars = sum(repo.get('stargazers_count', 0)
                          for repo in repos_data)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)

        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "repo_count": len(repos_data),
            "average_stars": round(total_stars / len(repos_data), 2) if repos_data else 0,
            "average_forks": round(total_forks / len(repos_data), 2) if repos_data else 0,
            "most_starred_repo": max(repos_data, key=lambda x: x.get('stargazers_count', 0))['name'] if repos_data else "None",
            "languages_used": len(set(repo.get('language') for repo in repos_data if repo.get('language')))
        }

    def _get_primary_languages(self, repos_data: List[Dict[str, Any]]) -> List[str]:
        """Get primary programming languages"""
        languages = [repo.get('language')
                     for repo in repos_data if repo.get('language')]
        return [lang for lang, _ in Counter(languages).most_common(5)]

    def _calculate_skill_level(self, metrics: Dict[str, Any]) -> SkillLevel:
        """Calculate skill level based on metrics"""
        total_stars = metrics.get('total_stars', 0)
        total_forks = metrics.get('total_forks', 0)
        repo_count = metrics.get('repo_count', 0)

        score = 0
        if total_stars > 1000:
            score += 3
        elif total_stars > 100:
            score += 2
        elif total_stars > 10:
            score += 1

        if total_forks > 500:
            score += 2
        elif total_forks > 50:
            score += 1

        if repo_count > 50:
            score += 2
        elif repo_count > 10:
            score += 1

        if score >= 5:
            return SkillLevel.EXPERT
        elif score >= 3:
            return SkillLevel.ADVANCED
        elif score >= 2:
            return SkillLevel.INTERMEDIATE
        else:
            return SkillLevel.BEGINNER

    def _calculate_activity_score(self, repos_data: List[Dict[str, Any]]) -> float:
        """Calculate activity score based on repository updates"""
        if not repos_data:
            return 0.0

        # Count repos updated in last 90 days
        recent_threshold = datetime.now().timestamp() - (90 * 24 * 60 * 60)
        recent_repos = [
            repo for repo in repos_data
            if datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00')).timestamp() > recent_threshold
        ]

        recent_ratio = len(recent_repos) / len(repos_data)
        return min(recent_ratio * 100, 100)

    def _calculate_community_impact(self, metrics: Dict[str, Any]) -> float:
        """Calculate community impact score"""
        total_stars = metrics.get('total_stars', 0)
        total_forks = metrics.get('total_forks', 0)
        followers = metrics.get('followers', 0)

        star_score = min(total_stars / 1000 * 100, 100)
        fork_score = min(total_forks / 500 * 100, 100)
        follower_score = min(followers / 1000 * 100, 100)

        return (star_score * 0.4) + (fork_score * 0.3) + (follower_score * 0.3)
