import re
from typing import Any, Dict, List, Union

"""
Validation utilities for the Obsidian MCP Server
"""

class McpErrorCode:
  BAD_REQUEST = "BAD_REQUEST"

class ObsidianError(Exception):
  def __init__(self, message: str, code: str):
    super().__init__(message)
    self.code = code

def validate_file_path(filepath: str) -> None:
  """
  Validates a file path to prevent path traversal attacks and other security issues.
  :param filepath: The path to validate
  :raises ObsidianError: if the path is invalid
  """
  # Prevent path traversal attacks
  normalized_path = filepath.replace("\\", "/")
  if "../" in normalized_path or "..\\" in normalized_path:
    raise ObsidianError(
      "Invalid file path: Path traversal not allowed",
      McpErrorCode.BAD_REQUEST
    )
  
  # Additional path validations (check for absolute paths Unix or Windows style)
  if normalized_path.startswith("/") or re.match(r"^[a-zA-Z]:", normalized_path):
    raise ObsidianError(
      "Invalid file path: Absolute paths not allowed",
      McpErrorCode.BAD_REQUEST
    )

def sanitize_header(value: str) -> str:
  """
  Sanitizes a header value to prevent header injection attacks.
  :param value: The header value to sanitize
  :return: The sanitized header value
  """
  # Remove any potentially harmful characters from header values
  return re.sub(r"[^\w\s\-\._~:/?#\[\]@!$&'()*+,;=]", "", value)

def validate_tool_arguments(args: Any, schema: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
  """
  Validates tool arguments against a JSON schema.
  :param args: The arguments to validate
  :param schema: The JSON schema to validate against
  :return: Validation result with errors if any
  """
  if not isinstance(args, dict):
    return {"valid": False, "errors": ["Arguments must be an object"]}

  errors = []
  required = schema.get("required", [])
  
  # Check required fields
  for field in required:
    if field not in args:
      errors.append(f"Missing required field: {field}")

  # Check field types
  properties = schema.get("properties", {})
  for key, value in args.items():
    prop_schema = properties.get(key)
    if not prop_schema:
      errors.append(f"Unknown field: {key}")
      continue

    # Skip validation for undefined optional fields
    if value is None and key not in required:
      continue

    # Type validation
    if prop_schema.get("type") == "string" and not isinstance(value, str):
      errors.append(f"Field {key} must be a string")
    elif prop_schema.get("type") == "number" and not isinstance(value, (int, float)):
      errors.append(f"Field {key} must be a number")
    elif prop_schema.get("type") == "boolean" and not isinstance(value, bool):
      errors.append(f"Field {key} must be a boolean")
    elif prop_schema.get("type") == "array" and not isinstance(value, list):
      errors.append(f"Field {key} must be an array")

    # Enum validation
    if "enum" in prop_schema and value not in prop_schema["enum"]:
      errors.append(f"Field {key} must be one of: {', '.join(map(str, prop_schema['enum']))}")

    # Format validation for paths
    if prop_schema.get("format") == "path" and isinstance(value, str):
      try:
        validate_file_path(value)
      except ObsidianError as error:
        errors.append(f"Field {key}: {str(error)}")

  return {"valid": len(errors) == 0, "errors": errors}
