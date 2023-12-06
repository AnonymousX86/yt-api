# -*- coding: utf-8 -*-
from unittest import TestCase, main as test_main

from yt_api.database import Playlist
from yt_api.tests.core import random_string


class TestPlaylist(TestCase):
    def setUp(self) -> None:
        self.spotify_id = random_string(22)
        self.youtoube_id = random_string(34)

    def test_add_and_get_playlist(self) -> None:
        Playlist.add_playlist(
            spotify_id=self.spotify_id,
            youtube_id=self.youtoube_id
        )
        playlist_by_spotify = Playlist.get_playlist(spotify_id=self.spotify_id)
        self.assertEqual(playlist_by_spotify.spotify_id, self.spotify_id)
        self.assertEqual(playlist_by_spotify.youtube_id, self.youtoube_id)
        playlist_by_youtube = Playlist.get_playlist(youtube_id=self.youtoube_id)
        self.assertEqual(playlist_by_youtube.spotify_id, self.spotify_id)
        self.assertEqual(playlist_by_youtube.youtube_id, self.youtoube_id)

    def test_remove_playlist(self) -> None:
        Playlist.add_playlist(
            spotify_id=self.spotify_id,
            youtube_id=self.youtoube_id
        )
        Playlist.remove_playlist(spotify_id=self.spotify_id)
        playlist = Playlist.get_playlist(spotify_id=self.spotify_id)
        self.assertIsNone(playlist)


if __name__ == '__main__':
    test_main()
