import os
from unittest import mock

import pytest


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
def dotenvvar():
    from dotenv import load_dotenv

    with mock.patch.dict(os.environ, clear=True):
        load_dotenv()
        yield  # This is the magical bit which restore the environment after
