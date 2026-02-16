from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class Project:
    id: str  # From the main 'id' field
    title: str  # From attributes -> title
    tests_count: int  # From attributes -> tests-count
    status: str  # From attributes -> status
    api_key: str  # From attributes -> api-key


class ProjectStore:
    def __init__(self, raw_response: list | None = None) -> None:
        # We navigate to the 'data' list in your JSON
        self.projects: List[Project] = [
            Project(
                id=item["id"],
                title=item["attributes"]["title"],
                tests_count=item["attributes"]["tests-count"],
                status=item["attributes"]["status"],
                api_key=item["attributes"]["api-key"],
            )
            for item in raw_response.get("data", [])
        ]

    def __getitem__(self, index):
        return self.projects[index]

    def __len__(self) -> int:
        return len(self.projects)

    def __repr__(self):
        return f"ProjectStore(count={len(self.projects)})"

    def get_project_by_title(self, title: str) -> Optional[Project]:
        return next((p for p in self.projects if p.title == title), None)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return next((p for p in self.projects if p.id == project_id), None)

    @property
    def total_count(self) -> int:
        return len(self.projects)


class TestomatApiClient:
    def __init__(self, base_url, token):
        self._base_url = base_url
        self._session = requests.Session()
        self._token = token
        self._jwt_token: str | None = None
        self._all_projects: ProjectStore | None = None

    def _request_auth_token(self) -> TestomatApiClient:  # noqa: F821
        if self._jwt_token is None:
            payload = {"api_token": self._token}
            r = requests.post(self._base_url + "/api/login", data=payload)
            self._jwt_token = r.json()["jwt"]
        return self

    def _request_projects(self) -> TestomatApiClient:  # noqa: F821
        if self._jwt_token is None:
            self._request_auth_token()

        r = requests.get(
            self._base_url + "/api/projects", headers={"Authorization": f"Bearer {self._jwt_token}"}
        )
        self._all_projects = ProjectStore(r.json())
        return self

    def get_projects(self) -> ProjectStore:  # noqa: F821
        if self._all_projects is None:
            self._request_projects()
        return self._all_projects
