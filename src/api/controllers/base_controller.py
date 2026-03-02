import logging

import requests

logger = logging.getLogger(__name__)


class BaseController:
    def __init__(self, base_url: str, api_token: str | None):
        self._base_url = base_url
        self._session = requests.Session()
        self._token = api_token
        self._jwt_token: str | None = None

    def _request_auth_token(self) -> str:  # noqa: F821
        if self._jwt_token is None:
            payload = {"api_token": self._token}
            url = self._url("/api/login")
            logger.info("POST %s | Body: {api_token: ***}", url)
            resp = requests.post(url, data=payload)
            logger.info("Response: %s", resp.status_code)
            self._jwt_token = resp.json()["jwt"]
        return self._jwt_token

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._request_auth_token()}"}

    def _post(self, path: str, data: dict[str, str]):
        url = self._url(path)
        logger.info("REQUEST POST %s | Body: %s", url, data)
        response = self._session.post(url, headers=self._headers(), json=data)
        logger.info("Response [%s]: %s", response.status_code, response.text)
        return response

    def _put(self, path: str, data: dict[str, str]):
        url = self._url(path)
        logger.info("REQUEST PUT %s | Body: %s", url, data)
        response = self._session.put(url, headers=self._headers(), json=data)
        logger.info("Response [%s]: %s", response.status_code, response.text)
        return response

    def _get(self, path: str):
        url = self._url(path)
        logger.info("REQUEST GET %s", url)
        response = self._session.get(url, headers=self._headers())
        logger.info("Response [%s]: %s", response.status_code, response.text)
        return response

    def _delete(self, path: str):
        url = self._url(path)
        logger.info("REQUEST DELETE %s", url)
        response = self._session.delete(url, headers=self._headers())
        logger.info("Response [%s]: %s", response.status_code, response.text)
        return response
