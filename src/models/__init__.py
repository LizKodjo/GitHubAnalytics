# src/models/__init__.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

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
    primary_languages: List[str] = Field(default_factory=list)
    skill_level: SkillLevel
    repository_analysis: List[RepositoryAnalysis] = Field(default_factory=list)
    activity_score: float = Field(..., ge=0, le=100)
    community_impact: float = Field(..., ge=0, le=100)
    
    # Metrics
    metrics: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }