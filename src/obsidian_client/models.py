from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, Literal, List, Union

@dataclass
class ObsidianConfig:
    """Configuration for the Obsidian client."""
    api_key: str
    verify_ssl: Optional[bool] = None
    timeout: Optional[int] = None
    max_content_length: Optional[int] = None
    max_body_length: Optional[int] = None

@dataclass
class ObsidianServerConfig:
    """Server configuration for Obsidian."""
    protocol: Literal["http", "https"]
    host: str
    port: int

DEFAULT_OBSIDIAN_CONFIG = ObsidianServerConfig(
    protocol="https",  # HTTPS required by default in Obsidian REST API plugin
    host="127.0.0.1",
    port=27124
)

@dataclass
class NoteJson:
    """JSON representation of an Obsidian note."""
    content: str
    frontmatter: Dict[str, Any]
    path: str
    stat: Dict[str, int]
    tags: List[str]

@dataclass
class ObsidianFile:
    """Obsidian file/folder information."""
    path: str
    type: Literal["file", "folder"]
    children: Optional[List['ObsidianFile']] = None

@dataclass
class ObsidianCommand:
    """Obsidian command."""
    id: str
    name: str

@dataclass
class ObsidianStatus:
    """Obsidian server status."""
    authenticated: bool
    ok: str
    service: str
    versions: Dict[str, str]

@dataclass
class PeriodType:
    """Period type for periodic notes."""
    type: Literal["daily", "weekly", "monthly", "quarterly", "yearly"]

@dataclass
class SearchMatch:
    """Search match with context."""
    context: str
    match: Dict[str, int]

@dataclass
class SearchResult:
    """Standard search result."""
    filename: str
    result: Any

@dataclass
class SimpleSearchResult:
    """Simple search result with context."""
    filename: str
    score: float
    matches: List[SearchMatch]

SearchResponse = Union[SearchResult, SimpleSearchResult]

@dataclass
class JsonLogicQuery:
    """JSON Logic query for complex searches."""
    query: Dict[str, Any]
