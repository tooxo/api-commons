import asyncio
import unittest

import spotify

import os

spotifyApi = spotify.SpotifyApi(
    client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"]
)


class TestSpotifyAlbum(unittest.TestCase):
    def test_album_parse(self):
        album: spotify.Album = spotify.Album.from_id(
            "20r762YmB5HeofjMCiPMLv", spotifyApi.get_auth_token()
        )
        self.assertEqual(album.name, "My Beautiful Dark Twisted Fantasy")
        self.assertEqual(album.tracks.__len__(), 13)
        self.assertEqual(album.album_type, "album")
        self.assertEqual(album.uri, "spotify:album:20r762YmB5HeofjMCiPMLv")

    def test_album_parse_async(self):
        t = asyncio.run(spotifyApi.get_auth_token_async())
        album: spotify.Album = asyncio.run(
            spotify.Album.from_id_async("20r762YmB5HeofjMCiPMLv", t)
        )
        self.assertEqual(album.name, "My Beautiful Dark Twisted Fantasy")
        self.assertEqual(album.tracks.__len__(), 13)
        self.assertEqual(album.album_type, "album")
        self.assertEqual(album.uri, "spotify:album:20r762YmB5HeofjMCiPMLv")


class TestSpotifyTrack(unittest.TestCase):
    def test_track_extract(self):
        track: spotify.Track = spotifyApi.extract_track(
            "https://open.spotify.com/track/4qikXelSRKvoCqFcHLB2H2?si"
            "=WObyUyrNTySu3DCkEqT7Fg"
        )
        self.assertEqual(track.name, "Mercy")

    def test_track_extract_async(self):
        track: spotify.Track = asyncio.run(
            spotifyApi.extract_track_async(
                "https://open.spotify.com/track/4qikXelSRKvoCqFcHLB2H2?si"
                "=WObyUyrNTySu3DCkEqT7Fg"
            )
        )
        self.assertEqual(track.name, "Mercy")


class TestSpotifyPlaylist(unittest.TestCase):
    def test_playlist_extract(self):
        playlist: spotify.Playlist = spotifyApi.extract_playlist(
            "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si"
            "=gUkqHK2nQi-gSChD8sEygQ"
        )
        self.assertEqual(len(playlist.tracks), 50)
        self.assertEqual(playlist.name, "Global Top 50")

    def test_playlist_extract_async(self):
        playlist: spotify.Playlist = asyncio.run(
            spotifyApi.extract_playlist_async(
                "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si"
                "=gUkqHK2nQi-gSChD8sEygQ"
            )
        )
        self.assertEqual(len(playlist.tracks), 50)
        self.assertEqual(playlist.name, "Global Top 50")


if __name__ == "__main__":
    unittest.main()
