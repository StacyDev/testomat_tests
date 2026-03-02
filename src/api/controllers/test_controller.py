import requests

from src.api.controllers.base_controller import BaseController
from src.api.models.test_models import TestBodyPropsRelaxed, TestBodyPropsStrict


def preprocess_response(response) -> tuple[requests.Response, TestBodyPropsStrict | None]:
    model = None
    if response.status_code == 200:
        json_payload = response.json()
        data_content = json_payload.get("data")  # Safe way to access

        if data_content:
            model = TestBodyPropsStrict.model_validate(data_content)

    return response, model


class TestController(BaseController):
    def create(
        self, data_value: TestBodyPropsRelaxed | None, project_id: str
    ) -> tuple[requests.Response, TestBodyPropsStrict | None]:
        # converting the model to a dictionary and placing it as data property value in request body
        body: dict = {"data": data_value.build()}

        response = self._post(f"/api/{project_id}/tests", body)

        return preprocess_response(response)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._request_auth_token()}",
            "Content-Type": "application/json",
        }

    def update(
        self, test_id: str, data_value: TestBodyPropsRelaxed | None, project_id: str
    ) -> tuple[requests.Response, TestBodyPropsStrict | None]:
        body: dict = {"data": data_value.build()}

        response = self._put(f"/api/{project_id}/tests/{test_id}", body)
        return preprocess_response(response)

    def get_single(
        self, test_id: str, project_id: str
    ) -> tuple[requests.Response, TestBodyPropsStrict | None]:
        response = self._get(f"/api/{project_id}/tests/{test_id}")

        return preprocess_response(response)

    def get(self, project_id: str) -> tuple[requests.Response, TestBodyPropsStrict | None]:
        response = self._get(f"/api/{project_id}/tests")

        return preprocess_response(response)

    def delete(self, test_id: str, project_id: str) -> requests.Response:
        return self._delete(f"/api/{project_id}/tests/{test_id}")
