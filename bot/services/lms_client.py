"""LMS API client - async HTTP client for querying the LMS backend.

Usage:
    from services.lms_client import LMSClient

    client = LMSClient()
    items = await client.get_items()
    pass_rates = await client.get_pass_rates("lab1")
"""

import httpx
from config import settings


class LMSClient:
    """Async HTTP client for the LMS API with Bearer authentication."""

    def __init__(self):
        self.base_url = settings.LMS_API_BASE_URL
        self.api_key = settings.LMS_API_KEY
        self.timeout = 10.0  # seconds

    async def get_items(self) -> list | str:
        """Fetch all items from the LMS API.

        Returns:
            list: List of items on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/items/"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            return f"Timeout connecting to LMS API at {url}"
        except httpx.ConnectError:
            return f"Could not connect to LMS API at {url}"
        except httpx.HTTPStatusError as e:
            return f"LMS API returned error: {e.response.status_code} {e.response.reason_phrase}"
        except httpx.RequestError as e:
            return f"Request failed: {str(e)}"

    async def get_pass_rates(self, lab: str) -> dict | str:
        """Fetch pass rates for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab1").

        Returns:
            dict: Pass rates data on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/pass-rates"
        params = {"lab": lab}
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            return f"Timeout connecting to LMS API at {url}"
        except httpx.ConnectError:
            return f"Could not connect to LMS API at {url}"
        except httpx.HTTPStatusError as e:
            return f"LMS API returned error: {e.response.status_code} {e.response.reason_phrase}"
        except httpx.RequestError as e:
            return f"Request failed: {str(e)}"
