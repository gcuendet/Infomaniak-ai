
import aiofiles
import pytest

from infomaniak_ai.openai.audio.transcriptions import transcribe
from infomaniak_ai.session import Session


@pytest.mark.parametrize("testfile", ["tests/audio.mp3"])
@pytest.mark.asyncio
async def test_transcribe(testfile,dotenvvar):
    session = await Session.create()

    async with aiofiles.open(testfile, "rb") as audiofile:
        content = await audiofile.read()
        text = await transcribe(session=session, audio=content)
    assert "Jeanne" in text
