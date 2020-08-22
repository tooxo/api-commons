import asyncio
import unittest

import spotify


class TestSpotifyAlbum(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.spotifyApi = spotify.SpotifyApi(
            client_id="",
            client_secret="")

    def test_album_parse(self):
        album: spotify.Album = \
            spotify.Album.from_id("20r762YmB5HeofjMCiPMLv",
                                  self.spotifyApi.get_auth_token())
        self.assertEqual(album.name, "My Beautiful Dark Twisted Fantasy")
        self.assertEqual(album.tracks.__len__(), 13)
        self.assertEqual(album.album_type, "album")
        self.assertEqual(album.uri, 'spotify:album:20r762YmB5HeofjMCiPMLv')

    def test_album_parse_async(self):
        album: spotify.Album = \
            asyncio.run(
                spotify.Album.from_id_async("20r762YmB5HeofjMCiPMLv",
                                            asyncio.run(
                                                self.spotifyApi.get_auth_token_async())))
        self.assertEqual(album.name, "My Beautiful Dark Twisted Fantasy")
        self.assertEqual(album.tracks.__len__(), 13)
        self.assertEqual(album.album_type, "album")
        self.assertEqual(album.uri, 'spotify:album:20r762YmB5HeofjMCiPMLv')


class TestSpotifyTrack(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.spotifyApi = spotify.SpotifyApi(
            client_id="a569a0d732104f2992bab508cf278f76",
            client_secret="0d4d8a8d657445a98e7f77ae6b538289")

    def test_track_extract(self):
        track: spotify.Track = self.spotifyApi.extract_track(
            "https://open.spotify.com/track/4qikXelSRKvoCqFcHLB2H2?si"
            "=WObyUyrNTySu3DCkEqT7Fg")
        self.assertEqual(track.name, "Mercy")

    def test_track_extract_async(self):
        track: spotify.Track = asyncio.run(self.spotifyApi.extract_track_async(
            "https://open.spotify.com/track/4qikXelSRKvoCqFcHLB2H2?si"
            "=WObyUyrNTySu3DCkEqT7Fg"
        ))
        self.assertEqual(track.name, "Mercy")


if __name__ == '__main__':
    unittest.main()
