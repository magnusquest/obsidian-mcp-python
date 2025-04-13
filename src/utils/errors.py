from typing import Any, Dict

"""
Error handling utilities for the Obsidian MCP Server
"""

class ApiError:
  """
  Standard error interface for API responses
  """
  def __init__(self, error_code: int, message: str):
    self.error_code = error_code  # 5-digit error code
    self.message = message        # Message describing the error

  def to_dict(self) -> Dict[str, Any]:
    return {
      "errorCode": self.error_code,
      "message": self.message
    }


class ObsidianError(Exception):
  """
  Error class for Obsidian MCP Server specific errors
  """
  def __init__(self, message: str, error_code: int = 50000, details: Any = None):
    super().__init__(message)
    self.name = "ObsidianError"
    self.details = details

    # Ensure 5-digit error code
    if error_code < 10000 or error_code > 99999:
      # Convert HTTP status codes to 5-digit codes
      # 4xx -> 4xxxx
      # 5xx -> 5xxxx
      self.error_code = error_code * 100 if error_code < 1000 else 50000
    else:
      self.error_code = error_code

  def to_api_error(self) -> ApiError:
    """
    Convert to API error format
    """
    return ApiError(self.error_code, str(self))


def get_error_code_from_status(status: int) -> int:
  """
  Maps HTTP status codes to internal error codes
  """
  if status == 400:
    return 40000  # Bad request
  elif status == 401:
    return 40100  # Unauthorized
  elif status == 403:
    return 40300  # Forbidden
  elif status == 404:
    return 40400  # Not found
  elif status == 405:
    return 40500  # Method not allowed
  elif status == 409:
    return 40900  # Conflict
  elif status == 429:
    return 42900  # Too many requests
  elif status == 500:
    return 50000  # Internal server error
  elif status == 501:
    return 50100  # Not implemented
  elif status == 502:
    return 50200  # Bad gateway
  elif status == 503:
    return 50300  # Service unavailable
  elif status == 504:
    return 50400  # Gateway timeout
  elif 400 <= status < 500:
    return 40000 + (status - 400) * 100
  elif 500 <= status < 600:
    return 50000 + (status - 500) * 100
  else:
    return 50000