# SPDX-FileCopyrightText: 2025-present Gabriel Cuendet <gabriel.cuendet@gmail.com>
#
# SPDX-License-Identifier: MIT

from requests_toolbelt.multipart.encoder import MultipartEncoder

from infomaniak_ai.session import Session


async def transcribe(session: Session, audio):
    mp_encoder = MultipartEncoder(
        fields={
            "model": "whisperV2",
            "response_format": "text",
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            "file": ("audio", audio),
        }
    )

    r = await session.post(
        url="openai/audio/transcriptions",
        data=mp_encoder.to_string(),
        headers={"Content-Type": mp_encoder.content_type},
    )
    async with r:
        if not r.ok:
            raise ConnectionError
        json_body = await r.json()

    # Fetch the result
    batch_id = json_body["batch_id"]
    status = "pending"

    while status == "pending":
        r = await session.get(url=f"results/{batch_id}")
        async with r:
            if not r.ok:
                raise ConnectionError
            json_body = await r.json()
            status = json_body["status"]

    return json_body["data"].strip()
