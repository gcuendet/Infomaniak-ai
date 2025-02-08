# SPDX-FileCopyrightText: 2025-present Gabriel Cuendet <gabriel.cuendet@gmail.com>
#
# SPDX-License-Identifier: MIT
from infomaniak_ai.session import Session


async def complete(session: Session):
    {
        "messages": [{"content": "Write a letter to your future self", "role": "user"}],
        "model": "mixtral",
    }
