from requests.exceptions import SSLError, ConnectionError, HTTPError
from .utils.errors import ObsidianError, get_error_code_from_status

"""
Error handling for Obsidian client
"""


def create_ssl_error_message(error: Exception, config: dict) -> str:
    return (
        "SSL certificate verification failed. You have two options:\n\n"
        "Option 1 - Enable HTTP (not recommended for production):\n"
        "1. Go to Obsidian Settings > Local REST API\n"
        "2. Enable 'Enable Non-encrypted (HTTP) Server'\n"
        "3. Update your client config to use 'http' protocol\n\n"
        "Option 2 - Configure HTTPS (recommended):\n"
        "1. Go to Obsidian Settings > Local REST API\n"
        "2. Under 'How to Access', copy the certificate\n"
        "3. Add the certificate to your system's trusted certificates:\n"
        "   - On macOS: Add to Keychain Access\n"
        "   - On Windows: Add to Certificate Manager\n"
        "   - On Linux: Add to ca-certificates\n"
        "   For development only: Set verifySSL: False in client config\n\n"
        f"Original error: {str(error)}"
    )


def create_connection_refused_message(host: str, port: int) -> str:
    return (
        "Connection refused. To fix this:\n"
        "1. Ensure Obsidian is running\n"
        "2. Verify the 'Local REST API' plugin is enabled in Obsidian Settings\n"
        f"3. Check that you're using the correct host ({host}) and port ({port})\n"
        "4. Make sure HTTPS is enabled in the plugin settings"
    )


def create_auth_failed_message() -> str:
    return (
        "Authentication failed. To fix this:\n"
        "1. Go to Obsidian Settings > Local REST API\n"
        "2. Copy your API key from the settings\n"
        "3. Update your configuration with the new API key\n"
        "Note: The API key changes when you regenerate certificates"
    )


def create_missing_api_key_message() -> str:
    return (
        "Missing API key. To fix this:\n"
        "1. Install the 'Local REST API' plugin in Obsidian\n"
        "2. Enable the plugin in Obsidian Settings\n"
        "3. Copy your API key from Obsidian Settings > Local REST API\n"
        "4. Provide the API key in your configuration"
    )


def handle_requests_error(error: Exception, host: str, port: int) -> ObsidianError:
    if isinstance(error, SSLError):
        return ObsidianError(
            create_ssl_error_message(error, {"verifySSL": True}),
            50001,  # SSL error code
            {"code": "SSL_ERROR"}
        )

    if isinstance(error, ConnectionError):
        return ObsidianError(
            create_connection_refused_message(host, port),
            50002,  # Connection refused
            {"code": "CONNECTION_REFUSED"}
        )

    if isinstance(error, HTTPError) and error.response is not None and error.response.status_code == 401:
        return ObsidianError(
            create_auth_failed_message(),
            40100,  # Unauthorized
            {"code": "UNAUTHORIZED"}
        )

    # For other errors, use API error code if available
    response = getattr(error, "response", None)
    error_data = getattr(response, "json", lambda: {})() if response else {}
    error_code = error_data.get("errorCode", get_error_code_from_status(response.status_code if response else 500))
    message = error_data.get("message", str(error) or "Unknown error")
    return ObsidianError(message, error_code, error_data)
