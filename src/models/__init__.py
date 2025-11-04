# src/models/__init__.py - Add better error handling
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class RepositoryAnalysis(BaseModel):
    name: str
    stars: int = Field(default=0, ge=0)
    forks: int = Field(default=0, ge=0)
    language: Optional[str] = None
    language_percentages: Dict[str, float] = Field(default_factory=dict)
    last_updated: datetime
    has_issues: bool = False
    has_wiki: bool = False
    is_fork: bool = False
    size_kb: int = Field(default=0, ge=0)

    @validator('last_updated', pre=True)
    def parse_last_updated(cls, v):
        if isinstance(v, str):
            # Handle different datetime formats from GitHub API
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v


class DeveloperProfile(BaseModel):
    username: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    joined_date: datetime
    public_repos: int = Field(default=0, ge=0)
    followers: int = Field(default=0, ge=0)
    following: int = Field(default=0, ge=0)
    primary_languages: List[str] = Field(default_factory=list)
    skill_level: SkillLevel = SkillLevel.BEGINNER
    repository_analysis: List[RepositoryAnalysis] = Field(default_factory=list)
    activity_score: float = Field(default=0.0, ge=0, le=100)
    community_impact: float = Field(default=0.0, ge=0, le=100)
    metrics: Dict[str, Any] = Field(default_factory=dict)

    @validator('joined_date', pre=True)
    def parse_joined_date(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
