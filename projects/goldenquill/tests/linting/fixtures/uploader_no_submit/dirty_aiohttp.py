"""R-UPLOADER-NO-SUBMIT — aiohttp.ClientSession (must fire)."""

from __future__ import annotations

import aiohttp


async def submit(url: str, payload: bytes) -> None:
    async with aiohttp.ClientSession() as session:
        await session.post(url, data=payload)
