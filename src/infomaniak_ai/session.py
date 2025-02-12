# SPDX-FileCopyrightText: 2025-present Gabriel Cuendet <gabriel.cuendet@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
from typing import Optional

import aiohttp


class Session:
    def __init__(self):
        self.product_id = os.environ.get("INFOMANIAK_PRODUCT_ID")
        self.infomaniak_api_version = 1
        if not self.product_id:
            msg = "Define INFOMANIAK_PRODUCT_ID=<product id> as an environment variable before opening a Session"
            raise RuntimeError(msg)

        self.base_url = f"https://api.infomaniak.com/{self.infomaniak_api_version}/ai/{self.product_id}/"
        self.access_token = os.environ.get("INFOMANIAK_ACCESS_TOKEN")
        if not self.access_token:
            msg = "Define INFOMANIAK_ACCESS_TOKEN=<access token> as an environment variable before opening a Session"
            raise RuntimeError(msg)

        self.authorization_header = {"Authorization": f"Bearer {self.access_token}"}
        self.client_session: Optional[aiohttp.ClientSession] = None
        self._missing_session_error_msg = "The Session has not been properly initialized. Use it in a 'async with' context."

    async def __aenter__(self):
        if self.client_session is None:
            self.client_session = aiohttp.ClientSession(
                base_url=self.base_url, headers=self.authorization_header
            )
            await self.client_session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client_session is not None:
            await self.client_session.__aexit__(exc_type, exc_val, exc_tb)
            self.client_session = None

    async def post(self, url: str, data: Optional[str] = None, headers=None):
        if self.client_session is None:
            raise RuntimeError(self._missing_session_error_msg)
        return await self.client_session.post(url=url, data=data, headers=headers)

    async def get(self, url: str, headers=None):
        if self.client_session is None:
            raise RuntimeError(self._missing_session_error_msg)
        return await self.client_session.get(url=url, headers=headers)
