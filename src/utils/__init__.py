"""Utility functions and classes for the Obsidian MCP Server."""

# Error handling
from .errors import (
    ApiError,
    ObsidianError,
    get_error_code_from_status,
)

# ID generation
from .id_generator import (
    generate_short_id,
    generate_prefixed_id,
)

# Logging
from .logging import (
    Logger,
    LogLevel,
    ErrorCategoryType,
    create_logger,
    root_logger,
)

# Rate limiting
from .rate_limiting import (
    RateLimiter,
    RateLimitConfig,
    DEFAULT_RATE_LIMIT_CONFIG,
    rate_limiter,
)

# Token counting
from .tokenization import (
    TokenCounter,
    MAX_TOKENS,
    TRUNCATION_MESSAGE,
    token_counter,
)

# Validation
from .validation import (
    McpErrorCode,
    validate_file_path,
    sanitize_header,
    validate_tool_arguments,
)

__all__ = [
    # Error handling
    "ApiError",
    "ObsidianError",
    "get_error_code_from_status",
    
    # ID generation
    "generate_short_id",
    "generate_prefixed_id",
    
    # Logging
    "Logger",
    "LogLevel",
    "ErrorCategoryType",
    "create_logger",
    "root_logger",
    
    # Rate limiting
    "RateLimiter",
    "RateLimitConfig",
    "DEFAULT_RATE_LIMIT_CONFIG",
    "rate_limiter",
    
    # Token counting
    "TokenCounter",
    "MAX_TOKENS",
    "TRUNCATION_MESSAGE",
    "token_counter",
    
    # Validation
    "McpErrorCode",
    "validate_file_path",
    "sanitize_header",
    "validate_tool_arguments",
]