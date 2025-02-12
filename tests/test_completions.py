import pytest

from infomaniak_ai.openai.chat.completions import complete, _validate_inputs
from infomaniak_ai.session import Session


def test_raise(dummyenvvar):
    data = {}
    with pytest.raises(AttributeError):
        _validate_inputs(data, max_tokens=-1)
    with pytest.raises(AttributeError):
        _validate_inputs(data, max_tokens=5001)
    data = _validate_inputs(data, max_tokens=1024)
    assert data["max_tokens"] == 1024

    with pytest.raises(AttributeError):
        _validate_inputs(data, frequency_penalty=-2.01)
    with pytest.raises(AttributeError):
        _validate_inputs(data, frequency_penalty=10)
    data = _validate_inputs(data, frequency_penalty=0.1)
    assert data["frequency_penalty"] == 0.1

    with pytest.raises(AttributeError):
        _validate_inputs(data, presence_penalty=-2.01)
    with pytest.raises(AttributeError):
        _validate_inputs(data, presence_penalty=10)
    data = _validate_inputs(data, presence_penalty=0.1)
    assert data["presence_penalty"] == 0.1

    with pytest.raises(AttributeError):
        _validate_inputs(data, temperature=-1)
    with pytest.raises(AttributeError):
        _validate_inputs(data, temperature=2.01)

    data = _validate_inputs(data, temperature=0.1)
    assert data["temperature"] == 0.1

    with pytest.raises(AttributeError):
        _validate_inputs(data, top_p=-1)
    with pytest.raises(AttributeError):
        _validate_inputs(data, top_p=2.01)

    data = _validate_inputs(data, top_p=0.1)
    assert data["top_p"] == 0.1


@pytest.mark.asyncio
async def test_complete(dummyenvvar, mock_api_call):
    async with Session() as session:
        msg = "Write a letter to your future self."
        text = await complete(session=session, msg=msg)
        assert "Dear Future Self," in text


@pytest.mark.real_api_calls
@pytest.mark.asyncio
async def test_complete(dotenvvar):
    async with Session() as session:
        msg = "Write a letter to your future self."
        text = await complete(session=session, msg=msg)
        assert "Dear Future Self," in text
