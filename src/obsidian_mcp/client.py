"""Obsidian MCP Python client."""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin

class ObsidianClient:
    def __init__(self, api_url: str, api_key: str):
        """Initialize Obsidian REST API client.
        
        Args:
            api_url: Base URL for the Obsidian Local REST API (e.g., 'http://localhost:27124')
            api_key: API key from Obsidian Local REST API plugin settings
        """
        self.api_url = api_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = False  # Local API uses self-signed cert

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to Obsidian API."""
        url = urljoin(self.api_url, endpoint)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get_active_file(self) -> Dict[str, Any]:
        """Get the content of the currently active file."""
        response = self._make_request('GET', '/active-file')
        return response.json()

    def update_active_file(self, content: str) -> Dict[str, Any]:
        """Update the content of the currently active file."""
        response = self._make_request('PUT', '/active-file', json={'content': content})
        return response.json()

    def delete_active_file(self) -> Dict[str, Any]:
        """Delete the currently active file."""
        response = self._make_request('DELETE', '/active-file')
        return response.json()

    def get_active_file_metadata(self) -> Dict[str, Any]:
        """Get metadata about the currently active file."""
        response = self._make_request('GET', '/active-file/metadata')
        return response.json()