import pytest

from infomaniak_ai.openai.chat.completions import complete
from infomaniak_ai.session import Session


@pytest.mark.asyncio
async def test_complete(dotenvvar):
    session = await Session.create()
    msg = "Write a letter to your future self."
    text = await complete(session=session, msg=msg)
    assert "Dear Future Self," in text
    await session.close()
