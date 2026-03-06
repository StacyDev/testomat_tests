import pytest
from faker import Faker

from src.api.controllers.suite_controller import SuiteController
from src.api.models.suite_models import (
    SuiteAttributesRelaxed,
    SuiteBodyPropsRelaxed,
    SuiteBodyPropsStrict,
)
from tests.fixtures.api import ApiContextHolder
from tests.fixtures.config import Config

fake = Faker()


def get_data_for_create_suite_case() -> SuiteBodyPropsRelaxed:
    attributes_value = SuiteAttributesRelaxed()
    attributes_value.title = f"{fake.sentence()} Stacy Suite"
    attributes_value.description = fake.sentence()
    return SuiteBodyPropsRelaxed(type="suite", attributes=attributes_value.build())


def test_creating_suite(project_context: ApiContextHolder, configs: Config) -> None:
    # arrange: preparing test data
    data_prop = get_data_for_create_suite_case()
    controller = SuiteController(base_url=configs.base_url_app, api_token=configs.token)

    # act
    model: SuiteBodyPropsStrict | None
    response, model = controller.create(data_prop, project_id=project_context.project_id)

    # assert
    assert response.status_code == 200, (
        f"Expected 200 but got {response.status_code}: {response.text}"
    )
    assert model is not None, "Expected model data but got None"
    assert model.attributes.description == data_prop.attributes.description, (
        f"Expected title {data_prop.attributes.description} but got {model.attributes.description}"
    )

    # pass cleanup data
    project_context.suite_id = model.id


def get_data_for_create_suite_no_title_case() -> SuiteBodyPropsRelaxed:
    attributes_value = SuiteAttributesRelaxed()
    attributes_value.description = fake.sentence()
    return SuiteBodyPropsRelaxed(type="suite", attributes=attributes_value.build())


def test_creating_suite_no_title(project_context: ApiContextHolder, configs: Config) -> None:
    # arrange: preparing test data
    data_prop = get_data_for_create_suite_no_title_case()
    controller = SuiteController(base_url=configs.base_url_app, api_token=configs.token)

    # act + assert (validating response against model)
    model: SuiteBodyPropsStrict | None
    response, model = controller.create(data_prop, project_id=project_context.project_id)

    # assert
    assert response.status_code == 400, (
        f"Expected 400 but got {response.status_code}: {response.text}"
    )
    assert model is None, "Expected no model data but got data instead"

    # pass cleanup data
    if model is not None:
        project_context.suite_id = model.id
