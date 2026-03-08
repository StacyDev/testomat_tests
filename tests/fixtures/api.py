from typing import Generator

import pytest
from faker.proxy import Faker

from src.api.controllers.suite_controller import SuiteController
from src.api.controllers.test_controller import TestController
from src.api.models.suite_models import SuiteAttributesRelaxed, SuiteBodyPropsRelaxed
from src.api.testomat_api_client import ApiClient
from tests.fixtures.config import Config

fake = Faker()


class ApiContextHolder:
    def __init__(self) -> None:
        self.project_id: str | None = None
        self.suite_id: str | None = None
        self.test_id: str | None = None


@pytest.fixture(scope="session")
def project_context(configs) -> Generator[ApiContextHolder, None, None]:
    client = ApiClient(configs.base_url_app, configs.token)
    infra = ApiContextHolder()
    all_projects = client.get_projects()
    infra.project_id = all_projects[1].id
    yield infra
    if infra.suite_id is not None:
        suite_controller = SuiteController(base_url=configs.base_url_app, api_token=configs.token)
        suite_controller.delete(infra.suite_id, project_id=infra.project_id)
        infra.suite_id = None


@pytest.fixture(scope="function")
def suite_context(
    project_context: ApiContextHolder,
    suite_controller: SuiteController,
    test_controller: TestController,
) -> Generator[ApiContextHolder, None, None]:

    infra = project_context
    attributes_value = SuiteAttributesRelaxed()
    attributes_value.title = fake.sentence()
    data_prop = SuiteBodyPropsRelaxed(type="suite", attributes=attributes_value.build())

    response, model = suite_controller.create(data_prop, project_id=project_context.project_id)

    assert response.status_code == 200

    infra.suite_id = model.id
    yield infra

    if infra.test_id is not None:
        test_controller.delete(infra.test_id, project_id=infra.project_id)
        infra.test_id = None
    suite_controller.delete(infra.suite_id, project_id=infra.project_id)
    infra.suite_id = None


@pytest.fixture
def suite_controller(configs: Config) -> SuiteController:
    return SuiteController(base_url=configs.base_url_app, api_token=configs.token)


@pytest.fixture
def test_controller(configs: Config) -> TestController:
    return TestController(base_url=configs.base_url_app, api_token=configs.token)
