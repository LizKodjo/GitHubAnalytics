import hashlib
import logging
import time
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
        if use_cache and self.cache:
            cached_data = await self.cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit for {endpoint}")
                return cached_data

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                print(f"🌐 Making request to GitHub API:: {url}")
                # logger.info(f"Fetching from GitHub API: {endpoint}")
                response = await client.get(url, headers=self.headers)

                # Check rate limits
                remaining = int(response.headers.get(
                    'X-RateLimit-Remaining', 1))
                limit = int(response.headers.get('X-RateLimit-Limit', 60))
                print(
                    f"📊 GitHub API Rate Limits: {remaining}/{remaining} remaining")

                if remaining == 0:
                    reset_time = int(response.headers.get(
                        'X-RateLimit-Reset', 0))
                    wait_time = max(0, reset_time - time.time())
                    raise Exception(
                        f"GitHub API rate limit exceeded.  Resets in {wait_time:.0f} seconds")

                # Handle rate limiting
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    raise RateLimitExceeded("GitHub API rate limit exceeded")

                if response.status_code == 404:
                    if 'users' in endpoint:
                        raise Exception(
                            f"GitHub user not found: {endpoint}")
                    else:
                        raise Exception(f"Resource not found: {endpoint}")

                if response.status_code == 401:
                    raise Exception(
                        "GitHub API authentication failed - check token")

                if response.status_code != 200:
                    raise Exception(
                        f"GitHub API error {response.status_code}: {response.text}")

                data = response.json()

                # Cache successful response (5 minutes)
                if use_cache and response.status_code == 200:
                    await self.cache.set(cache_key, data, ttl=300)

                return data

            except httpx.TimeoutException:
                raise Exception("GitHub API request timeout")
            except httpx.NetworkError:
                raise Exception("Network error connecting to GitHub API")

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        return await self._make_request(f"/users/{username}")

    async def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        return await self._make_request(f"/users/{username}/repos?sort=updated&per_page=100")

    async def get_repository_languages(self, username: str, repo: str) -> Dict[str, Any]:
        return await self._make_request(f"/repos/{username}/{repo}/languages")
