import hashlib
import logging
import time
from typing import Any, Dict, List, Optional
import httpx
import asyncio

from src.exceptions import AuthenticationError, GitHubAPIError, NetworkError, RateLimitExceeded, RepositoryNotFound, UserNotFound
from src.utils.cache import MemoryCache, RedisCache

logger = logging.getLogger(__name__)

class AsyncGitHubClient:
    """Advanced async GitHub API client with caching and retry logic"""
    
    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com", cache_url: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url
        self.token = token
        self.timeout = timeout
        
        # Initialise cache
        if cache_url:
            self.cache = RedisCache(cache_url)
        else:
            self.cache = MemoryCache()
            
        # Headers for GitHub API
        
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Analytics-Pro/1.0",}
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            
    def _get_cache_key(self, endpoint: str) -> str:
        """Generate cache key for endpoint"""
        return f"github:{hashlib.md5(endpoint.encode()).hexdigest()}"
    
    async def _make_request(self, endpoint: str, use_cache: bool = True, cache_ttl: int = 300) -> Dict[str, Any]:
        """Make authenticated request with caching and retry logic"""
        cache_key = self._get_cache_key(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Try cache first
        if use_cache and self.cache:
            cached_data = await self.cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit for {endpoint}")
                cached_data['_cache_hit'] = True
                return cached_data
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(3):
                try:
                    logger.debug(f"Making request to {url} (attempt {attempt + 1})")
                    response = await client.get(url, headers=self.headers)
                    
                    # Handle rate limitin
                    remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
                    if response.status_code == 403 and remaining == 0:
                        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                        wait_time = max(0, reset_time - time.time())
                        raise RateLimitExceeded(f"Rate limit exceeded.  Resets in {wait_time:.0f} seconds")
                    
                    # Handle errors
                    if response.status_code == 401:
                        raise AuthenticationError("Invalid or missing GitHub token")
                    elif response.status_code == 403:
                        raise GitHubAPIError("API forbidden - check token permissions.")
                    elif response.status_code == 404:
                        if 'users' in endpoint:
                            raise UserNotFound(f"User not found: {endpoint}")
                        else:
                            raise RepositoryNotFound(f"Repository not found: {endpoint}")
                   
                    elif response.status_code != 200:
                        raise GitHubAPIError(f"API error {response.status_code}: {response.text}")
                    
                    data = response.json()
                    data['_cache_hit'] = False
                    
                    # Cache successful responses
                    if use_cache and self.cache and response.status_code == 200:
                        await self.cache.set(cache_key, data, ttl=cache_ttl)
                        
                    return data
                except httpx.TimeoutException:
                    logger.warning(f"Request timeout (attempt {attempt + 1})")
                    if attempt == 2:
                        raise NetworkError("Request timeout after 3 attempts")
                    await asyncio.sleep(1 * (attempt + 1))
                    
                except httpx.NetworkError:
                    logger.warning(f"Network error (attempt {attempt + 1})")
                    if attempt == 2:
                        raise NetworkError("Network error after 3 attempts")
                    await asyncio.sleep(1 * (attempt + 1))
    
    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get comprehensive user profile"""
        return await self._make_request(f"/users/{username}")
    
    async def get_user_repositories(self, username: str, sort: str = "updated", per_page: int = 100) -> List[Dict[str, Any]]:
        """Get user repositories with pagination support"""
        return await self._make_request(f"/users/{username}/repos?sort={sort}&per_page={per_page}")
    
    async def get_repository_languages(self, username: str, repo: str) -> Dict[str, Any]:
        """Get repository language statistics"""
        return await self._make_request(f"/repos/{username}/{repo}/languages")
    
    async def get_user_activity(self, username:str) -> List[Dict[str, Any]]:
        """Get user recent activity"""
        return await self._make_request(f"/users/{username}/events?per_page=50")
    
    async def get_organisation_members(self, org: str) -> List[Dict[str,Any]]:
        """Get Organisation members"""
        return await self._make_request(f"/orgs/{org}/members")
    
    async def close(self):
        """Close client connections"""
        if hasattr(self.cache, 'close'):
            await self.cache.close()
    
    