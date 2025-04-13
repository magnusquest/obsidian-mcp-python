from threading import Lock, Timer
from time import time

"""
Rate limiting utilities for the Obsidian MCP Server
"""

class ObsidianError(Exception):
  def __init__(self, message, code):
    super().__init__(message)
    self.code = code


class RateLimitConfig:
  def __init__(self, window_ms: int, max_requests: int):
    self.window_ms = window_ms
    self.max_requests = max_requests


DEFAULT_RATE_LIMIT_CONFIG = RateLimitConfig(
  window_ms=15 * 60 * 1000,  # 15 minutes
  max_requests=200
)


class RateLimiter:
  def __init__(self, config: RateLimitConfig = DEFAULT_RATE_LIMIT_CONFIG):
    self.config = config
    self.request_counts = {}
    self.lock = Lock()
    self.cleanup_interval = 60  # Clean up every minute
    self.cleanup_timer = Timer(self.cleanup_interval, self.cleanup)
    self.cleanup_timer.start()

  def check_rate_limit(self, key: str) -> bool:
    """
    Check if a request is within rate limits.
    :param key: Identifier for the rate limit bucket (e.g., toolName)
    :return: Whether the request is allowed
    """
    now = int(time() * 1000)
    with self.lock:
      request_info = self.request_counts.get(key)

      if not request_info or now > request_info['reset_time']:
        # Reset counter for new window
        self.request_counts[key] = {
          'count': 1,
          'reset_time': now + self.config.window_ms
        }
        return True

      if request_info['count'] >= self.config.max_requests:
        return False

      request_info['count'] += 1
      return True

  def enforce_rate_limit(self, key: str) -> None:
    """
    Check rate limit and throw an error if exceeded.
    :param key: Identifier for the rate limit bucket
    :raises ObsidianError: If rate limit is exceeded
    """
    if not self.check_rate_limit(key):
      raise ObsidianError(
        f"Rate limit exceeded for {key}. Please try again later.",
        42900  # 42900 = Rate limit exceeded
      )

  def get_rate_limit_info(self, key: str):
    """
    Get information about current rate limit status.
    :param key: Identifier for the rate limit bucket
    :return: Rate limit information or None if no requests have been made
    """
    with self.lock:
      request_info = self.request_counts.get(key)
      if not request_info:
        return None

      return {
        'remaining': max(0, self.config.max_requests - request_info['count']),
        'reset_time': request_info['reset_time']
      }

  def cleanup(self):
    """
    Clean up expired rate limit entries.
    """
    now = int(time() * 1000)
    with self.lock:
      keys_to_delete = [
        key for key, info in self.request_counts.items()
        if now > info['reset_time']
      ]
      for key in keys_to_delete:
        del self.request_counts[key]

    # Restart the cleanup timer
    self.cleanup_timer = Timer(self.cleanup_interval, self.cleanup)
    self.cleanup_timer.start()

  def dispose(self):
    """
    Clean up resources (e.g., when shutting down).
    """
    if self.cleanup_timer:
      self.cleanup_timer.cancel()


# Export a singleton instance with default configuration
rate_limiter = RateLimiter()
