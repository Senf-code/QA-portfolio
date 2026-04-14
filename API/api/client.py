from __future__ import annotations

from urllib.parse import urljoin

import requests
from requests import Response, Session


class ApiClient:
    """Small wrapper around requests.Session for cleaner tests."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session: Session = requests.Session()

    def get(self, path: str, **kwargs) -> Response:
        return self.session.get(self._build_url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.session.post(self._build_url(path), timeout=self.timeout, **kwargs)

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path.lstrip("/"))
