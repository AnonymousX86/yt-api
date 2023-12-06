# -*- coding: utf-8 -*-
class Thumbnail:
    def __init__(self, name: str, payload: dict) -> None:
        self.name: str = name
        self.url: str = payload.get('url')
        self.width: int = int(payload.get('width', 0)) or None
        self.height: int = int(payload.get('height', 0)) or None

    @staticmethod
    def list_from_payload(payload: dict[str, dict[str, str | str, int]]) -> list['Thumbnail']:
        """Models YouTube API response of 'thumbails'."""
        return [Thumbnail(t, payload[t]) for t in payload]
