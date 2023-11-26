# -*- coding: utf-8 -*-
class Localization:
    def __init__(self, name: str, payload: dict) -> None:
        self.name: str = name
        self.title: str = payload.get('title')
        self.description: str = payload.get('description')

    @staticmethod
    def list_from_payload(payload: dict[str, dict[str, str]]) -> list['Localization']:
        """Models YouTube API response of 'localizations'."""
        return [Localization(l, payload[l]) for l in payload]
