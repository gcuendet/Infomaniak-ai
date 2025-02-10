# SPDX-FileCopyrightText: 2025-present Gabriel Cuendet <gabriel.cuendet@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from enum import Enum
from typing import Optional
import asyncio

from requests_toolbelt.multipart.encoder import MultipartEncoder

from infomaniak_ai.session import Session


class ResponseFormat(str, Enum):
    """Enum containing the different possible values for the response_format"""

    JSON = "json"
    SRT = "srt"
    TEXT = "text"
    VERBOSE_JSON = "verbose_json"
    VTT = "vtt"


class Model(str, Enum):
    """Enum containing the different models available"""

    WHISPER = "whisper"
    WHISPER_V2 = "whisperV2"


async def transcribe(
    session: Session,
    audio: bytes,
    model: Model = Model.WHISPER,
    response_format: ResponseFormat = ResponseFormat.TEXT,
    prompt: Optional[str] = None,
    language: Optional[str] = None,
    chunk_length: Optional[int] = None,
):
    """Transcribe an audio file into different formats of text

    Parameters:
    -----------
    session: Session

    audio: bytes
        The audio content to transcribe

    model: Model (default=WHISPER)
        ID of the model to use.

    format: ResponseFormat (default=TEXT)
        The format of the transcript output

    prompt: str
        An optional text to guide the model's style or continue a previous audio
        segment. The prompt should match the audio language.

    language: str
        The language of the input audio. Supplying the input language will
        translate the output.

    chunk_length: int
        Defines the maximum duration for an active segment in sec. For subtitle
        tasks, it's recommended to set this to a short duration (5-10 seconds)
        to avoid long sentences.

    Returns:
    --------
    file_string: str
        String representation of the content of the file. In the case of a text
        file, that's simply the transcription

    filename: str
        Filename, with the correct extension, corresponding to the response
        format.

    file_content: bytes
        Content of the file
    """
    arguments = {
        "model": model,
        "response_format": response_format,
        # plain file object, no filename or mime type produces a
        # Content-Disposition header with just the part name
        "file": ("audio", audio),
    }
    if prompt:
        arguments["prompt"] = prompt
    if language:
        arguments["language"] = language
    if chunk_length:
        arguments["chunk_length"] = chunk_length

    mp_encoder = MultipartEncoder(fields=arguments)

    r = await session.post(
        url="openai/audio/transcriptions",
        data=mp_encoder.to_string(),
        headers={"Content-Type": mp_encoder.content_type},
    )
    async with r:
        json_body = await r.json()
        if not r.ok:
            msg = json_body["error"]["description"] if "error" in json_body else ""
            raise ConnectionError(msg)

    # Fetch the result
    batch_id = json_body["batch_id"]
    status = "pending"

    while status == "pending":
        await asyncio.sleep(1)
        r = await session.get(url=f"results/{batch_id}")
        async with r:
            json_body = await r.json()
            if not r.ok:
                msg = json_body["error"]["description"] if "error" in json_body else ""
                raise ConnectionError(msg)
            status = json_body["status"]

    # Download data
    truncated_url = json_body["url"].replace(session.base_url, "")
    r = await session.get(url=truncated_url)

    file_content = await r.content.read()
    filename = json_body["file_name"]
    file_string = json_body["data"].strip()
    return file_string, filename, file_content
