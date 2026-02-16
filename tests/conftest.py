from pathlib import Path
from typing import Any, Generator

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"


def pytest_configure(config: pytest.Config) -> None:
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo
) -> Generator[None, Any, None]:
    outcome = yield
    rep = outcome.get_result()
    # store result for each phase rep_setup, rep_call, rep_teardown
    setattr(item, f"rep_{rep.when}", rep)


pytest_plugins = [
    "tests.fixtures.app",
    "tests.fixtures.config",
    "tests.fixtures.cookie_helper",
    "tests.fixtures.infrastructure_handler",
    "tests.fixtures.playwright",
    "tests.fixtures.api",
]
