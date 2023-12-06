# -*- coding: utf-8 -*-
from unittest import TestCase, main as test_main

from yt_api.database import Track
from yt_api.tests.core import random_string


class TestTrack(TestCase):
    def setUp(self) -> None:
        self.spotify_id = random_string(22)
        self.youtoube_id = random_string(11)

    def test_add_and_get_track(self) -> None:
        Track.add_track(
            spotify_id=self.spotify_id,
            youtube_id=self.youtoube_id
        )
        track_by_spotify = Track.get_track(spotify_id=self.spotify_id)
        self.assertEqual(track_by_spotify.spotify_id, self.spotify_id)
        self.assertEqual(track_by_spotify.youtube_id, self.youtoube_id)
        track_by_youtube = Track.get_track(youtube_id=self.youtoube_id)
        self.assertEqual(track_by_youtube.spotify_id, self.spotify_id)
        self.assertEqual(track_by_youtube.youtube_id, self.youtoube_id)

    def test_remove_track(self) -> None:
        Track.add_track(
            spotify_id=self.spotify_id,
            youtube_id=self.youtoube_id
        )
        Track.remove_track(spotify_id=self.spotify_id)
        track = Track.get_track(spotify_id=self.spotify_id)
        self.assertIsNone(track)


if __name__ == '__main__':
    test_main()
