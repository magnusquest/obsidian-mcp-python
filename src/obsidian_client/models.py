from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Vault:
    """Represents an Obsidian vault."""
    path: str
    name: str

@dataclass
class Note:
    """Represents an Obsidian note."""
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None
