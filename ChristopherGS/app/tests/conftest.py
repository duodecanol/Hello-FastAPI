from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import deps


async def override_reddit_dependency() -> MagicMock:
    # 4 We make use of the Python standard library unittest mock MagicMock (docs for those unfamiliar)
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock
    mock = MagicMock()
    reddit_stub = {
        "recipes": [
            "baz",
        ],
        "easyrecipes": [
            "bar",
        ],
        "TopSecretRecipes": [
            "foo"
        ],
    }
    # 5 We specify the return value of a particular method
    # in our mocked reddit client (get_reddit_top), here it will return dummy data
    mock.get_reddit_top.return_value = reddit_stub
    return mock


@pytest.fixture() # 1 We use the pytest fixture decorator to define a fixture
def client() -> Generator:
    # 2 We access the FastAPI built-in test client via a context manager so we can easily perform clean-up (see 7)
    with TestClient(app) as client:
        # 3 We use the FastAPI app dependency_overrides to replace dependencies.
        # We replace what the selected dependency (in this case get_reddit_client) callable is,
        # pointing to a new callable which will be used in testing (in this case override_reddit_dependency)
        app.dependency_overrides[deps.get_reddit_client] = override_reddit_dependency
        yield client  # 6 We yield the modified client
        app.dependency_overrides = {}  # 7 We perform clean up on the client, reverting the dependencies
