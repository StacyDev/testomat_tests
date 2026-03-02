from typing import Any

import requests

from src.api.controllers.base_controller import BaseController
from src.api.models.suite_models import (
    SuiteBodyPropsRelaxed,
    SuiteBodyPropsStrict,
)


def preprocess_response(response) -> tuple[requests.Response, SuiteBodyPropsStrict | None]:
    model = None
    if response.status_code == 200:
        json_payload = response.json()
        data_content = json_payload.get("data")  # Safe way to access

        if data_content:
            model = SuiteBodyPropsStrict.model_validate(data_content)

    return response, model


class SuiteController(BaseController):
    def create(
        self, data_value: SuiteBodyPropsRelaxed | None, project_id: str
    ) -> tuple[requests.Response, SuiteBodyPropsStrict]:
        # converting the model to a dictionary and placing it as data property value in request body
        body: dict = {"data": data_value.build()}

        response = self._post(f"/api/{project_id}/suites", body)

        return preprocess_response(response)

    def update(
        self, suite_id: str, data_value: SuiteBodyPropsRelaxed | None, project_id: str
    ) -> tuple[requests.Response, SuiteBodyPropsStrict]:
        body: dict = {"data": data_value.build()}

        response = self._put(f"/api/{project_id}/suites/{suite_id}", body)

        return preprocess_response(response)

    def get_single(
        self, suite_id: str, project_id: str
    ) -> tuple[requests.Response, SuiteBodyPropsStrict]:
        response = self._get(f"/api/{project_id}/suites/{suite_id}")

        return preprocess_response(response)

    def get(self, suite_id: str, project_id: str) -> tuple[requests.Response, SuiteBodyPropsStrict]:
        response = self._get(f"/api/{project_id}/suites")

        return preprocess_response(response)

    def delete(self, suite_id: str, project_id: str) -> requests.Response:
        return self._delete(f"/api/{project_id}/suites/{suite_id}")
