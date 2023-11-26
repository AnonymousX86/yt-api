# -*- coding: utf-8 -*-
"""
Adds video to playlist.
"""
from json import loads as json_loads

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from authentication import get_authenticated_service
from models import Thumbnail


class PlaylistItem:
    def __init__(self, payload: dict) -> None:
        self.kind: str = payload.get('kind')
        self.etag: str = payload.get('etag')
        self.id: str = payload.get('id')

        snippet: dict = payload.get('snippet', {})
        self.published_at: str = snippet.get('publishedAt')
        self.channel_id: str = snippet.get('channelId')
        self.title: str = snippet.get('title')
        self.description: str = snippet.get('description')
        self.thumbnails: list[Thumbnail] = Thumbnail.list_from_payload(
            payload.get('thumbnails')
        )
        self.channel_title: str = snippet.get('channelTitle')
        self.video_owner_channel_title: str = snippet.get('videoOwnerChannelTitle')
        self.video_owner_channel_id: str = snippet.get('videoOwnerChannelId')
        self.playlist_id: str = snippet.get('playlistId')
        self.position: int = snippet.get('position')

        resource_id: dict = snippet.get('resourceId')
        self.resource_kind: str = resource_id.get('kind')
        self.resource_video_id: str = resource_id.get('videoId')

        content_details: dict = payload.get('contentDetails', {})
        self.video_id: str = content_details.get('videoId')
        self.start_at: str = content_details.get('startAt')
        self.end_at: str = content_details.get('endAt')
        self.note: str = content_details.get('note')
        self.video_published_at: str = content_details.get('videoPublishedAt')

        status: dict = payload.get('status', {})
        self.privacy_status: str = status.get('privacyStatus')




def add_video(youtube: Resource, playlist_id: str, video_id: str) -> bool:
    """Adds video to playlist by IDs and return it as `PlaylistItem`."""
    response: dict = youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    ).execute()

    return PlaylistItem(response)


if __name__ == '__main__':
    # Connect to YouTube
    youtube = get_authenticated_service()

    playlist_id = 'PLHpqNKpoWiNX5Qbl0syonrL3El3Ojt9Kf'
    video_id = 'dQw4w9WgXcQ'

    try:
        playlist_item = add_video(youtube, playlist_id, video_id)
        if playlist_item:
            print(f'Video ID: {video_id} added to playlist ID {playlist_id}')
        else:
            print('Adding failed')
    except HttpError as e:
        code = e.resp.status
        message = json_loads(e.content).get('error', {}).get('message', 'Unknown error.')
        print(f'Error {code}: {message}')
