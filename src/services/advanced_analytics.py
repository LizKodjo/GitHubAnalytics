import asyncio
from collections import Counter
import statistics
from typing import Any, Dict, List
from src.client.github_client import AsyncGitHubClient
from src.models import DeveloperProfile, RepositoryAnalysis, SkillLevel
from datetime import datetime


class AdvancedAnalyticsService:
    """Advanced analytics service for GitHub profiles"""
    
    def __init__(self, client: AsyncGitHubClient):
        self.client = client
    
    async def get_comprehensive_analysis(self, username: str) -> DeveloperProfile:
        """Get comprehensive analysis of a GitHub user"""
        # Fetch data concurrently
        user_data, repos_data = await asyncio.gather(self.client.get_user_profile(username), self.client.get_user_repositories(username), return_exceptions=True)
        
        # Handle errors
        if isinstance(user_data, Exception):
            raise user_data
        if isinstance(repos_data, Exception):
            raise repos_data
        
        # Analysis repositories
        repo_analyses = []
        for repo in repos_data[:10]:
            try:
                languages = await self.client.get_repository_languages(username, repo['name'])
                repo_analysis = RepositoryAnalysis(
                    name=repo['name'],
                    stars=repo['stargazers_count'],
                    forks=repo['forks_count'],
                    language=repo['language'],
                    language_percentages=languages,
                    last_updated=datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00')),
                    has_issues=repo['has_issues'],
                    has_wiki=['has_wiki'],
                    is_fork=repo['fork'],
                    size_kb=repo['size'],
                )
                repo_analyses.append(repo_analysis)
            except Exception as e:
                # Continue with other repos if one fails
                continue
            
            # Calculate metrics
            languages = self._analyse_languages(repos_data)
            skill_level = self._calculate_skill_level(repos_data, repo_analyses)
            activity_score = self._calculate_activity_score(user_data, repos_data)
            community_impact = self._calculate_commnunity_impact(user_data, repos_data)
            
            return DeveloperProfile(
                username=user_data['login'],
                name=user_data.get('name'),
                avatar_url=user_data.get('avatar_url'),
                joined_date=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00')),
                public_repos=user_data['public_repos'],
                followers=user_data['followers'],
                following=user_data['following'],
                primary_languages=languages,
                skill_level=skill_level,
                repository_analysis=repo_analyses,
                activity_score=activity_score,
                community_impact=community_impact,
                metrics=self._calculate_metrics(user_data, repos_data)
            )
            
    def _analyse_languages(self, repos_data: List[Dict[str, Any]]) -> List[str]:
        """Extract primary programming languages"""
        languages = [repo.get('languages') for repo in repos_data if repo.get('language')]
        language_counts = Counter(languages)
        return [lang for lang, _ in language_counts.most_common(5)]
    
    def _calculate_skill_level(self, repos_data: List[Dict[str, Any]], repo_analyses: List[RepositoryAnalysis]) -> SkillLevel:
        """Calculate developer skill level based on repository metrics"""
        if not repos_data:
            return SkillLevel.BEGINNER
        
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
        account_age = (datetime.now() - datetime.fromisoformat(repos_data[0]['created_at'].replace('Z', '+00:00'))).days
        
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
            
        if account_age > 365 * 3:
            score += 2
        elif account_age > 365:
            score += 1
            
        if len(repo_analyses) > 20:
            score +=2
        elif len(repo_analyses) > 5:
            score += 1
            
        if score >= 6:
            return SkillLevel.EXPERT
        elif score >= 4:
            return SkillLevel.ADVANCED
        elif score >= 2:
            return SkillLevel.INTERMEDIATE
        else:
            return SkillLevel.BEGINNER
       
    def _calculate_activity_score(self, user_data: Dict[str, Any], repos_data: List[Dict[str, Any]]) -> float:
        """Calculate user activity score (0-100)"""
        if not repos_data:
            return 0.0
        
        # Recent activity (last 90 days)
        recent_threshold = datetime.now().timestamp() - (90 * 24 * 60 * 60)
        recent_repos = [
            repo for repo in repos_data
            if datetime.fromisoformat(repo['updated_at'].replace(('Z', '+00:00')).timestamp() > recent_threshold)
        ]
        
        recent_activity_ratio = len(recent_repos) / len(repos_data)
        
        # Followers to following ratio
        followers = user_data['followers']
        following = user_data['following']
        follower_ratio = followers / max(1, following)
        
        # Repository activity
        repo_activity = min(len(repos_data) / 50 * 100, 100)
        
        score = (recent_activity_ratio * 40) + (min(follower_ratio, 5) * 20) + (repo_activity * 0.4)
        return min(score, 100)
    
    def _calculate_community_impact(self, user_data: Dict[str, Any], repos_data: List[Dict[str, Any]]) -> float:
        """Calculate community impact score (0-100)"""
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
        followers = user_data['followers']
        
        # Normalise scors
        star_score = min(total_stars / 1000 * 100, 100) 
        fork_score = min(total_forks / 500 * 100, 100)
        follower_score = min(followers / 100 * 100, 100)
        
        return (star_score * 0.4) + (fork_score * 0.3) + (follower_score * 0.3)
    
    def _calculate_metrics(self, user_data: Dict[str, Any], repos_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate various developer metrics"""
        if not repos_data:
            return {}
        
        stars = [repo.get('stargazers_count', 0) for repo in repos_data]
        forks = [repo.get('forks_count', 0) for repo in repos_data]
        sizes = [repo.get('size', 0) for repo in repos_data]
        
        return {
            "total_stars": sum(stars),
            "average_stars": round(statistics.mean(stars), 2) if stars else 0,
            "total_forks": sum(forks),
            "average_forks": round(statistics.mean(forks), 2) if forks else 0,
            "total_repo_size_mb": round(sum(sizes) / 1024, 2),
            "most_starred_repo": max(repos_data, key=lambda x: x.get('stargazers_count', 0))['name'],
            "repo_count": len(repos_data),
            "languages_used": len(set(repo.get('language') for repo in repos_data if repo.get('language')))
        }