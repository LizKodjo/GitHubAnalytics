import hashlib
import logging
from typing import Any, Dict, List, Optional

import httpx

from src.exceptions import GitHubAPIError, RateLimitExceeded, UserNotFound
from src.utils.cache import MemoryCache


logger = logging.getLogger(__name__)


class AsyncGitHubClient:
    """Async GitHub API client with caching"""

    def __init__(self, token: Optional[str] = None):
        self.base_url = 'https://api.github.com'
        self.token = token
        self.cache = MemoryCache()

        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Analytics-Pro/1.0",
        }

        if self.token:
            self.headers["Authorization"] = f"Token {self.token}"

    def _get_cache_key(self, endpoint: str) -> str:
        return f"github:{hashlib.md5(endpoint.encode()).hexdigest()}"

    async def _make_request(self, endpoint: str, use_cache: bool = True) -> Dict[str, Any]:
        cache_key = self._get_cache_key(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Try cache first
        if use_cache:
            cached_data = await self.cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit for {endpoint}")
                return cached_data

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                logger.info(f"Fetching from GitHub API: {endpoint}")
                response = await client.get(url, headers=self.headers)

                # Handle rate limiting
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    raise RateLimitExceeded("GitHub API rate limit exceeded")

                if response.status_code == 404:
                    if 'users' in endpoint:
                        raise UserNotFound(
                            f"GitHub user not found: {endpoint}")
                    else:
                        raise GitHubAPIError(f"Resource not found: {endpoint}")

                if response.status_code != 200:
                    raise GitHubAPIError(
                        f"API error {response.status_code}: {response.text}")

                data = response.json()

                # Cache successful response (5 minutes)
                if use_cache and response.status_code == 200:
                    await self.cache.set(cache_key, data, ttl=300)

                return data

            except httpx.TimeoutException:
                raise GitHubAPIError("Request timeout")
            except httpx.NetworkError:
                raise GitHubAPIError("Network error")

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        return await self._make_request(f"/users/{username}")

    async def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        return await self._make_request(f"/users/{username}/repos?sort=updated&per_page=100")

    async def get_repository_languages(self, username: str, repo: str) -> Dict[str, Any]:
        return await self._make_request(f"/repos/{username}/{repo}/languages")
