from typing import Any

from pydantic import BaseModel, Field

from src.api.models.common_models import RequestMixin


class TestAttributesStrict(BaseModel):
    __test__ = False  # This tells pytest "I am not a test suite"
    title: str | None = Field(...)
    state: str | None = Field(...)
    emoji: str | None = Field(...)
    # API was missing this key, added default=None
    recordings_count: str | None = Field(default=None, alias="recordings-count")
    code: str | None = Field(...)
    file: str | None = Field(...)
    priority: str | None = Field(...)
    sync: bool | None = Field(...)
    # API was missing this key, added default=None
    last_sync_id: str | None = Field(default=None, alias="last-sync-id")
    run_statuses: list[dict[str, Any]] | None = Field(..., alias="run-statuses")
    assigned_to: str | None = Field(..., alias="assigned-to")
    description: str | None = Field(...)
    suite_id: str | None = Field(..., alias="suite-id")
    has_examples: str | None = Field(..., alias="has-examples")
    params: list[dict[str, Any]] | None = Field(...)
    public_title: str | None = Field(..., alias="public-title")
    tags: list[dict[str, Any]] | None = Field(...)
    # API was missing this key, added default=None
    previous_description: str | None = Field(default=None, alias="previous-description")
    import_id: str | None = Field(..., alias="import-id")
    # API was missing this key, added default=None
    play_url: str | None = Field(default=None, alias="play-url")
    # API returned [] (list) for this, updated type hint
    jira_issues: list | str | None = Field(..., alias="jira-issues")
    attachments: str | None = Field(...)


class TestBodyPropsStrict(BaseModel):
    __test__ = False  # This tells pytest "I am not a test suite"
    id: str = Field(...)
    type: str = Field(...)
    attributes: TestAttributesStrict
    relationships: dict[str, Any]
    labels_ids: list[str] | None = None


class TestAttributesRelaxed(RequestMixin):
    __test__ = False  # This tells pytest "I am not a test suite"
    # 'Any | None' accepts any data type OR a missing field
    title: Any | None = Field(default=None)
    state: Any | None = Field(default=None)
    emoji: Any | None = Field(default=None)
    recordings_count: Any | None = Field(default=None, alias="recordings-count")
    code: Any | None = Field(default=None)
    file: Any | None = Field(default=None)
    priority: Any | None = Field(default=None)
    sync: Any | None = Field(default=None)
    last_sync_id: Any | None = Field(default=None, alias="last-sync-id")
    run_statuses: Any | None = Field(default=None, alias="run-statuses")
    assigned_to: Any | None = Field(default=None, alias="assigned-to")
    description: Any | None = Field(default=None)
    suite_id: Any | None = Field(default=None, alias="suite-id")
    has_examples: Any | None = Field(default=None, alias="has-examples")
    params: Any | None = Field(default=None)
    public_title: Any | None = Field(default=None, alias="public-title")
    tags: Any | None = Field(default=None)
    previous_description: Any | None = Field(default=None, alias="previous-description")
    import_id: Any | None = Field(default=None, alias="import-id")
    play_url: Any | None = Field(default=None, alias="play-url")
    jira_issues: Any | None = Field(default=None, alias="jira-issues")
    attachments: Any | None = Field(default=None)


class TestBodyPropsRelaxed(RequestMixin):
    __test__ = False  # This tells pytest "I am not a test suite"
    id: Any | None = Field(default=None)
    type: Any | None = Field(default=None)
    attributes: TestAttributesRelaxed | None = Field(default_factory=TestAttributesRelaxed)
    relationships: Any | None = Field(default=None)
