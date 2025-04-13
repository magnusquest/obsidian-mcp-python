import uuid

def generate_short_id() -> str:
  """
  Generates a unique, URL-friendly, 6-character alphanumeric ID.
  Uses nanoid's default alphabet (A-Za-z0-9_-).

  Returns:
    A 6-character string ID.
  """
  return uuid.uuid4().hex[:6]

def generate_prefixed_id(prefix: str, length: int = 10) -> str:
  """
  Generates a unique ID with a specified prefix and length.

  Args:
    prefix: The prefix for the ID (e.g., 'prj', 'tsk', 'knw').
    length: The desired length of the random part of the ID (default: 10).

  Returns:
    A prefixed ID string (e.g., 'prj_aBcDeFgHiJ').
  """
  return f"{prefix}_{uuid.uuid4().hex[:length]}"