# -*- coding: utf-8 -*-
"""
Creates a playlist in the authorizing user's YouTube channel.
"""
from enum import Enum

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from authentication import get_authenticated_service
from models import Localization, Thumbnail


class PrivacyStatus(Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'
    UNLISTED = 'unlisted'


class Playlist:
    def __init__(self, payload: dict):
        self.kind: str = payload.get('kind')
        self.etag: str = payload.get('etag')
        self.id: str = payload.get('id')

        snippet: dict = payload.get('snippet', {})
        self.published_at: str = snippet.get('publishedAt')
        self.channel_id: str = snippet.get('channelId')
        self.title: str = snippet.get('title')
        self.description: str = snippet.get('description')
        self.thumbnails: list[Thumbnail] = Thumbnail.list_from_payload(
            snippet.get('thumbnails')
        )
        self.channel_title: str = snippet.get('channelTitle')
        self.default_language: str = snippet.get('defaultLanguage')
        localized: dict = snippet.get('localized', {})
        self.localized_title: str = localized.get('title')
        self.localized_description: str = localized.get('description')

        status: dict = payload.get('status', {})
        self.privacy_status: str = status.get('privacyStatus')

        content_details: dict = payload.get('contentDetails', {})
        self.item_count: int = int(content_details.get('itemCount', 0)) or None

        player: dict = payload.get('player', {})
        self.embed_html: str = player.get('embedHtml')

        self.localizations: list[Localization] = Localization.list_from_payload(
            payload.get('localizations', {})
        )



def add_playlist(
        youtube: Resource,
        title: str,
        description: str,
        privacy_status: PrivacyStatus = None
    ) -> Playlist:
    """Creates playlist then returns it as `Playlist`."""
    if not privacy_status:
        privacy_status = PrivacyStatus.UNLISTED
    response: dict = youtube.playlists().insert(
        part = 'snippet,status',
        body = dict(
            snippet = dict(
                title = title,
                description = description
            ),
            status = dict(
                privacyStatus = privacy_status.value
            )
        )
    ).execute()

    return Playlist(response)


if __name__ == '__main__':
    # Connect to YouTube
    youtube = get_authenticated_service()

    playlist_title = input('Playlist title: ') or 'Test playlist'
    playlist_description = input('Playlist description: ') or 'Playlist created with `yt_api` by AnonymousX86.'

    # Create playlist
    try:
        new_playlist = add_playlist(youtube, playlist_title, playlist_description)
        print(f'New playlist ID: {new_playlist.id}')
    except HttpError as e:
        print('An HTTP error {0.resp.status} occurred: {0.content}'.format(e))
