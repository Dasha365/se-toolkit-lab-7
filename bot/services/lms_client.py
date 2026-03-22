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

    async def get_learners(self) -> list | str:
        """Fetch all enrolled learners from the LMS API.

        Returns:
            list: List of learners on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/learners/"
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

    async def get_scores(self, lab: str) -> list | str:
        """Fetch score distribution for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab-01").

        Returns:
            list: Score distribution (4 buckets) on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/scores"
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

    async def get_timeline(self, lab: str) -> list | str:
        """Fetch submission timeline for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab-01").

        Returns:
            list: Submissions per day on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/timeline"
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

    async def get_groups(self, lab: str) -> list | str:
        """Fetch per-group performance for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab-01").

        Returns:
            list: Per-group scores and student counts on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/groups"
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

    async def get_top_learners(self, lab: str, limit: int = 10) -> list | str:
        """Fetch top learners by average score for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab-01").
            limit: Number of top learners to return (default: 10).

        Returns:
            list: Top learners with avg_score and attempts on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/top-learners"
        params = {"lab": lab, "limit": limit}
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

    async def get_completion_rate(self, lab: str) -> dict | str:
        """Fetch completion rate for a specific lab from the LMS API.

        Args:
            lab: The lab identifier (e.g., "lab-01").

        Returns:
            dict: Completion rate percentage with passed/total counts on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/analytics/completion-rate"
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

    async def trigger_sync(self) -> dict | str:
        """Trigger a data sync from the autochecker API.

        Returns:
            dict: Sync summary on success.
            str: Error message on failure.
        """
        url = f"{self.base_url}/pipeline/sync"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers)
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
