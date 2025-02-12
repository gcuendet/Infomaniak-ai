import os
import io
import asyncio
from typing import Optional

from unittest import mock
import pytest

from infomaniak_ai.session import Session


def pytest_addoption(parser):
    parser.addoption(
        "--real-api-calls",
        action="store_true",
        default=False,
        help="makes real calls to the API",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "real-api-calls: mark test as making real api calls"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--real-api-calls"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_real_calls = pytest.mark.skip(
        reason="real_api_calls: need --real-api-calls option to run"
    )
    for item in items:
        if "real_api_calls" in item.keywords:
            item.add_marker(skip_real_calls)


@pytest.fixture
def clearenvvar():
    with mock.patch.dict(os.environ, clear=True):
        yield  # This is the magical bit which restore the environment after


@pytest.fixture
def dummyenvvar(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "INFOMANIAK_PRODUCT_ID": "DUMMY",
            "INFOMANIAK_ACCESS_TOKEN": "DUMMY",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after


@pytest.fixture
def dotenvvar(monkeypatch):
    from dotenv import load_dotenv

    with mock.patch.dict(os.environ, clear=True):
        load_dotenv()
        yield  # This is the magical bit which restore the environment after


@pytest.fixture
def mock_api_call(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.ok = True

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

    class CompletePostMockResponse(MockResponse):
        async def json(self):
            return {"choices": [{"message": {"content": "Dear Future Self,"}}]}

    class TranscribePostMockResponse(MockResponse):
        async def json(self):
            return {"batch_id": "xxx"}

    class TranscribeGetMockResponse(MockResponse):
        def __init__(self):
            class DummyReader:
                async def read(self):
                    return b"Jeanne"

            super().__init__()
            self.content = DummyReader()

        async def json(self):
            return {
                "status": "ok",
                "url": "https://api.infomaniak.com/1/ai/DUMMY/results",
                "file_name": "transcription.txt",
                "data": "Jeanne",
            }

    async def dummy_post_api_call(url, data=None, headers=None):
        if url == "openai/chat/completions":
            return CompletePostMockResponse()
        elif url == "openai/audio/transcriptions":
            return TranscribePostMockResponse()

    async def dummy_get_api_call(url, headers=None):
        return TranscribeGetMockResponse()

    post_mock = mock.AsyncMock(Session.post, side_effect=dummy_post_api_call)
    get_mock = mock.AsyncMock(Session.get, side_effect=dummy_get_api_call)
    monkeypatch.setattr(Session, "post", post_mock)
    monkeypatch.setattr(Session, "get", get_mock)
