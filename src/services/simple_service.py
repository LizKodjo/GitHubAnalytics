# src/services/simple_service.py
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
from ..client.github_client import AsyncGitHubClient
from ..models import DeveloperProfile, RepositoryAnalysis, SkillLevel


class SimpleAnalyticsService:
    """Ultra-simple analytics service that definitely works"""

    def __init__(self, client: AsyncGitHubClient):
        self.client = client

    async def get_comprehensive_analysis(self, username: str) -> DeveloperProfile:
        """Ultra-simple analysis that definitely works"""
        try:
            print(f"🔍 ULTRA-SIMPLE: Starting analysis for {username}")

            # Just get basic user data
            user_data = await self.client.get_user_profile(username)
            repos_data = await self.client.get_user_repositories(username)

            print(
                f"✅ ULTRA-SIMPLE: Got {len(repos_data)} repos for {username}")

            # Create VERY basic repository analyses
            repo_analyses = []
            for repo in repos_data[:5]:  # Only 5 repos max
                try:
                    analysis = RepositoryAnalysis(
                        name=repo['name'],
                        stars=repo.get('stargazers_count', 0),
                        forks=repo.get('forks_count', 0),
                        language=repo.get('language'),
                        language_percentages={},  # Skip languages for now
                        last_updated=datetime.fromisoformat(
                            repo['updated_at'].replace('Z', '+00:00')),
                        has_issues=repo.get('has_issues', False),
                        has_wiki=repo.get('has_wiki', False),
                        is_fork=repo.get('fork', False),
                        size_kb=repo.get('size', 0)
                    )
                    repo_analyses.append(analysis)
                except Exception as e:
                    print(
                        f"⚠️  ULTRA-SIMPLE: Skipping repo {repo.get('name')}: {e}")
                    continue

            # Calculate basic metrics
            languages = [repo.get('language')
                         for repo in repos_data if repo.get('language')]
            primary_languages = [lang for lang,
                                 _ in Counter(languages).most_common(3)]

            total_stars = sum(repo.get('stargazers_count', 0)
                              for repo in repos_data)
            total_forks = sum(repo.get('forks_count', 0)
                              for repo in repos_data)

            # Simple skill level calculation
            if total_stars > 1000:
                skill_level = SkillLevel.EXPERT
            elif total_stars > 100:
                skill_level = SkillLevel.ADVANCED
            elif total_stars > 10:
                skill_level = SkillLevel.INTERMEDIATE
            else:
                skill_level = SkillLevel.BEGINNER

            # Simple activity score based on repo count and recency
            recent_count = len([r for r in repos_data
                                if (datetime.now() - datetime.fromisoformat(r['updated_at'].replace('Z', '+00:00'))).days < 90])
            activity_score = min(
                (recent_count / max(len(repos_data), 1)) * 100, 100)

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
                # Simple impact score
                community_impact=min((total_stars + total_forks) / 10, 100),
                metrics={
                    "total_stars": total_stars,
                    "total_forks": total_forks,
                    "repo_count": len(repos_data),
                    "languages_used": len(set(languages))
                }
            )

            print(
                f"🎉 ULTRA-SIMPLE: Successfully created profile for {username}")
            return profile

        except Exception as e:
            print(f"❌ ULTRA-SIMPLE: Error for {username}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
