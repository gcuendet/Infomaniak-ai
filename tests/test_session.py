import pytest

from infomaniak_ai.session import Session


def test_init_throw_without_env_var(clearenvvar):
    with pytest.raises(RuntimeError):
        Session()


@pytest.mark.asyncio
async def test_session_context(dummyenvvar):
    async with Session() as s:
        assert s.product_id == "DUMMY"
        assert s.access_token == "DUMMY"
        assert (
            s.base_url
            == f"https://api.infomaniak.com/{s.infomaniak_api_version}/ai/{s.product_id}/"
        )
        assert "Authorization" in s.authorization_header
        assert s.authorization_header["Authorization"] == f"Bearer {s.access_token}"


@pytest.mark.asyncio
async def test_session_throw_without_context(dummyenvvar):
    s = Session()
    with pytest.raises(RuntimeError):
        await s.post("/")
    with pytest.raises(RuntimeError):
        await s.get("/")

    async with Session() as session:
        await session.get("/")
