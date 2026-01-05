import logging
from typing import Any, Dict

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class AnalyzeServiceError(Exception):
    pass


class AnalyzeServiceClient:
    def __init__(self, base_url: str | None = None, timeout_seconds: int = 5) -> None:
        self.base_url = base_url or settings.ANALYZE_SERVICE_BASE_URL
        self.timeout_seconds = timeout_seconds

    def analyze(self, description: str, company_id: int) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/api/analyze"
        payload = {"description": description, "company_id": company_id}
        try:
            response = requests.post(url, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise AnalyzeServiceError(f"Analyze service request failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise AnalyzeServiceError("Analyze service returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise AnalyzeServiceError("Analyze service returned unexpected payload type")

        missing = [k for k in ("category", "priority", "team_assignment") if k not in data]
        if missing:
            raise AnalyzeServiceError(f"Analyze service missing keys: {', '.join(missing)}")

        return data
