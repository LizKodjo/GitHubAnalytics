class GitHubAPIError(Exception):
    """Base exception for GitHub API errors"""
    pass

class RateLimitExceeded(GitHubAPIError):
    def __init__(self, reset_time=None):
        self.reset_time=reset_time
        message = "GitHub API rate limit exceeded"
        if reset_time:
            message += f". Resets at {reset_time}"
        super().__init__(message)
        
class UserNotFound(GitHubAPIError):
    pass

class RepositoryNotFound(GitHubAPIError):
    pass

class AuthenticationError(GitHubAPIError):
    pass

class NetworkError(GitHubAPIError):
    pass