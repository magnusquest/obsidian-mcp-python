class ObsidianClientError(Exception):
    """Base exception for Obsidian client errors."""
    pass

class VaultNotFoundError(ObsidianClientError):
    """Raised when the specified vault cannot be found."""
    pass

class NoteNotFoundError(ObsidianClientError):
    """Raised when a requested note cannot be found."""
    pass