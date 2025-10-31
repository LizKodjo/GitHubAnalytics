import re
from typing import Optional


def validate_username(username: str) -> Optional[str]:
    """Validate GitHub username"""
    if not username or not username.strip():
        return "Username is required"
    
    if len(username) > 39:
        return "Username must be 39 or less"
    
    # GitHub username patter: alphanumeric and hyphens, cannot start/end with hyphen
    pattern = r'^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$'
    if not re.match(pattern, username):
        return "Invalid GitHub username format"
    
    return None