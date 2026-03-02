import pytest
from faker import Faker

from src.api.controllers.test_controller import TestController
from src.api.models.test_models import (
    TestAttributesRelaxed,
    TestBodyPropsRelaxed,
    TestBodyPropsStrict,
)
from tests.fixtures.api import ApiContextHolder
from tests.fixtures.config import Config

fake = Faker()


def test_creating_testcase(suite_context: ApiContextHolder, configs: Config) -> None:
    # arrange
    attributes_value = TestAttributesRelaxed()
    attributes_value.suite_id = suite_context.suite_id
    attributes_value.title = f"{fake.sentence()} Stacy"
    data_prop = TestBodyPropsRelaxed(type="test", attributes=attributes_value.build())

    controller = TestController(base_url=configs.base_url_app, api_token=configs.token)

    # act + assert (validating response against model)
    model: TestBodyPropsStrict | None
    response, model = controller.create(data_prop, project_id=suite_context.project_id)

    # assert
    assert response.status_code == 200, (
        f"Expected 201 but got {response.status_code}: {response.text}"
    )
    assert model is not None, "Expected model data but got None"
    assert model.attributes.title == attributes_value.title, (
        f"Expected title {attributes_value.title} but got {model.attributes.title}"
    )

    # passing cleanup data
    if model and model.id:
        suite_context.test_id = model.id


def test_creating_testcase_suite_id_none(suite_context: ApiContextHolder, configs: Config) -> None:
    # arrange
    attributes_value = TestAttributesRelaxed()
    attributes_value.suite_id = None
    attributes_value.title = f"{fake.sentence()} Stacy"
    data_prop = TestBodyPropsRelaxed(type="test", attributes=attributes_value.build())

    controller = TestController(base_url=configs.base_url_app, api_token=configs.token)

    # act + assert (validating response against model)
    model: TestBodyPropsStrict | None
    response, model = controller.create(data_prop, project_id=suite_context.project_id)

    # assert
    assert response.status_code == 404, (
        f"Expected 404 but got {response.status_code}: {response.text}"
    )
    assert model is None, "Expected no model data but got data instead"

    # passing cleanup data
    if model and model.id:
        suite_context.test_id = model.id
