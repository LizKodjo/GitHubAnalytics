from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    
class RepositoryAnalysis(BaseModel):
    """Detailed repository analysis"""
    name: str
    stars: int = Field(..., ge=0)
    forks: int = Field(..., ge=0)
    language: Optional[str]
    language_percentages: Dict[str, float] = Field(default_factory=dict)
    last_updated: datetime
    has_issues: bool
    has_wiki: bool
    is_fork: bool
    size_kb: int
    
    @property
    def popularity_score(self) -> float:
        """Calculate repository popularity score"""
        return (self.stars * 2 + self.forks) / (self.size_kb / 1000 + 1)
    
class DeveloperProfile(BaseModel):
    """Comprehensive developer profile analysis"""
    username: str
    name: Optional[str]
    avatar_url: Optional[str]
    joined_date: datetime
    public_repos: int
    followers: int
    following: int
    
    # Analysis results
    primary_languages: List[str]
    skill_level: SkillLevel
    repository_analysis: List[RepositoryAnalysis]
    activity_score: float = Field(..., ge=0, le=100)
    community_impact: float = Field(..., ge=0, le=100)
    
    # Metrics
    metrics: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class SecurityAnalysis(BaseModel):
    """Security and compliance analysis"""
    has_2fa: bool
    email_verified: bool
    account_age_days: int
    recent_activity: bool
    repo_security_indicators: Dict[str,bool] = Field(default_factory=dict)
    
    @property
    def security_score(self) -> float:
        """Calculate security score (0-100)"""
        score = 0
        if self.has_2fa:
            score += 40
        if self.email_verified:
            score += 20
        if self.recent_activity:
            score += 20
        if len(self.repo_security_indicators) > 0:
            secure_repos = sum(self.repo_security_indicators.values())
            score += (secure_repos / len(self.repo_security_indicators)) * 20
        return min(score, 100)