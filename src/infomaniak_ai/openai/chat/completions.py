# SPDX-FileCopyrightText: 2025-present Gabriel Cuendet <gabriel.cuendet@gmail.com>
#
# SPDX-License-Identifier: MIT
from infomaniak_ai.session import Session
import json


async def complete(session: Session, msg: str):
    data = {
        "messages": [{"content": msg, "role": "user"}],
        "model": "mixtral",
    }

    r = await session.post(
        url="openai/chat/completions",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    async with r:
        json_body = await r.json()
        if not r.ok:
            print(json_body)
            raise ConnectionError

    print(json_body)
    return json_body["choices"][0]["message"]["content"]
