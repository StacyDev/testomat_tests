import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    base_sing_in_url: str
    base_url_app: str
    email: str
    password: str
    token: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url_app=os.getenv("BASE_APP_URL"),
        base_sing_in_url=f"{os.getenv('BASE_APP_URL')}/users/sign_in",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL"),
        token=os.getenv("TOKEN"),
    )
