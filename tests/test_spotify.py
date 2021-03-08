import asyncio
import unittest

from typing import List

import api_commons.spotify as spotify

import os

spotifyApi = spotify.SpotifyApi(
    client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"]
)


class TestSpotifyAlbum(unittest.TestCase):
    PART_ALBUM = spotify.Album.from_api_response(
        '{"album_type": "album", "artists": [{"external_urls": {"spotify": '
        '"https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau"}, "href": '
        '"https://api.spotify.com/v1/artists/1r4hJ1h58CWwUQe3MxPuau", '
        '"id": "1r4hJ1h58CWwUQe3MxPuau", "name": "Maluma", "type": "artist", '
        '"uri": "spotify:artist:1r4hJ1h58CWwUQe3MxPuau"}], '
        '"available_markets": ["AD", "AE", "AL", "AR", "AT", "AU", "BA", '
        '"BE", "BG", "BH", "BO", "BR", "BY", "CA", "CH", "CL", "CO", "CR", '
        '"CY", "CZ", "DE", "DK", "DO", "DZ", "EC", "EE", "EG", "ES", "FI", '
        '"FR", "GB", "GR", "GT", "HK", "HN", "HR", "HU", "ID", "IE", "IL", '
        '"IN", "IS", "IT", "JO", "JP", "KW", "KZ", "LB", "LI", "LT", "LU", '
        '"LV", "MA", "MC", "MD", "ME", "MK", "MT", "MX", "MY", "NI", "NL", '
        '"NO", "NZ", "OM", "PA", "PE", "PH", "PL", "PS", "PT", "PY", "QA", '
        '"RO", "RS", "RU", "SA", "SE", "SG", "SI", "SK", "SV", "TH", "TN", '
        '"TR", "TW", "UA", "US", "UY", "VN", "XK", "ZA"], "external_urls": {'
        '"spotify": "https://open.spotify.com/album/0p2yf6DucEgvj8Uk8KXJJv"}, '
        '"href": "https://api.spotify.com/v1/albums/0p2yf6DucEgvj8Uk8KXJJv", '
        '"id": "0p2yf6DucEgvj8Uk8KXJJv", "images": [{"height": 640, "url": '
        '"https://i.scdn.co/image/ab67616d0000b27387d15f78ec75621d40028baf", '
        '"width": 640}, {"height": 300, "url": '
        '"https://i.scdn.co/image/ab67616d00001e0287d15f78ec75621d40028baf", '
        '"width": 300}, {"height": 64, "url": '
        '"https://i.scdn.co/image/ab67616d0000485187d15f78ec75621d40028baf", '
        '"width": 64}], "name": "PAPI JUANCHO", "release_date": "2020-08-21", '
        '"release_date_precision": "day", "total_tracks": 22, "type": '
        '"album", "uri": "spotify:album:0p2yf6DucEgvj8Uk8KXJJv"}'
    )

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

    def test_complete_album(self):
        self.assertIsNone(TestSpotifyAlbum.PART_ALBUM.popularity)
        completed = TestSpotifyAlbum.PART_ALBUM.complete(
            spotifyApi.get_auth_token()
        )
        self.assertIsNotNone(completed.popularity)
        completed2 = completed.complete(spotifyApi.get_auth_token())
        self.assertEqual(completed, completed2)

    def test_complete_album_async(self):
        self.assertIsNone(TestSpotifyAlbum.PART_ALBUM.popularity)
        completed = asyncio.run(
            TestSpotifyAlbum.PART_ALBUM.complete_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertIsNotNone(completed.popularity)
        completed2 = asyncio.run(
            completed.complete_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertEqual(completed, completed2)


class TestSpotifyTrack(unittest.TestCase):
    PART_TRACK = spotify.Track.from_api_response(
        '{"artists": [{"external_urls": {"spotify": '
        '"https://open.spotify.com/artist/0Y5tJX1MQlPlqiwlOH1tJY"}, "href": '
        '"https://api.spotify.com/v1/artists/0Y5tJX1MQlPlqiwlOH1tJY", '
        '"id": "0Y5tJX1MQlPlqiwlOH1tJY", "name": "Travis Scott", "type": '
        '"artist", "uri": "spotify:artist:0Y5tJX1MQlPlqiwlOH1tJY"}], '
        '"available_markets": ["AD", "AE", "AL", "AR", "AT", "AU", "BA", '
        '"BE", "BG", "BH", "BO", "BR", "BY", "CA", "CH", "CL", "CO", "CR", '
        '"CY", "CZ", "DE", "DK", "DO", "DZ", "EC", "EE", "EG", "ES", "FI", '
        '"FR", "GB", "GR", "GT", "HK", "HN", "HR", "HU", "ID", "IE", "IL", '
        '"IN", "IS", "IT", "JO", "JP", "KW", "KZ", "LB", "LI", "LT", "LU", '
        '"LV", "MA", "MC", "MD", "ME", "MK", "MT", "MX", "MY", "NI", "NL", '
        '"NO", "NZ", "OM", "PA", "PE", "PH", "PL", "PS", "PT", "PY", "QA", '
        '"RO", "RS", "RU", "SA", "SE", "SG", "SI", "SK", "SV", "TH", "TN", '
        '"TR", "TW", "UA", "US", "UY", "VN", "XK", "ZA"], "disc_number": 1, '
        '"duration_ms": 270714, "explicit": true, "external_urls": {'
        '"spotify": "https://open.spotify.com/track/7wBJfHzpfI3032CSD7CE2m"}, '
        '"href": "https://api.spotify.com/v1/tracks/7wBJfHzpfI3032CSD7CE2m", '
        '"id": "7wBJfHzpfI3032CSD7CE2m", "is_local": false, "name": '
        '"STARGAZING", "preview_url": '
        '"https://p.scdn.co/mp3-preview'
        "/d2d23f9ea674dffde91d99783732b092655ccaf6?cid"
        '=a569a0d732104f2992bab508cf278f76", "track_number": 1, "type": '
        '"track", "uri": "spotify:track:7wBJfHzpfI3032CSD7CE2m"}'
    )

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

    def test_track_complete(self):
        self.assertIsNone(TestSpotifyTrack.PART_TRACK.popularity)
        completed = TestSpotifyTrack.PART_TRACK.complete(
            spotifyApi.get_auth_token()
        )
        self.assertIsNotNone(completed.popularity)

    def test_track_complete_async(self):
        self.assertIsNone(TestSpotifyTrack.PART_TRACK.popularity)
        completed = asyncio.run(
            TestSpotifyTrack.PART_TRACK.complete_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertIsNotNone(completed.popularity)


class TestSpotifyPlaylist(unittest.TestCase):
    PART_PLAYLIST = spotify.Playlist.from_api_response(
        '{"collaborative": false, "description": "Your daily update of the '
        'most played tracks right now.", "external_urls": {"spotify": '
        '"https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"}, "href": '
        '"https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF", '
        '"id": "37i9dQZEVXbMDoHDwVN2tF", "images": [{"height": null, "url": '
        '"https://charts-images.scdn.co/REGIONAL_GLOBAL_LARGE.jpg", "width": '
        'null}], "name": "Global Top 50", "owner": {"display_name": '
        '"spotifycharts", "external_urls": {"spotify": '
        '"https://open.spotify.com/user/spotifycharts"}, "href": '
        '"https://api.spotify.com/v1/users/spotifycharts", "id": '
        '"spotifycharts", "type": "user", "uri": '
        '"spotify:user:spotifycharts"}, "primary_color": null, "public": '
        'null, "snapshot_id": '
        '"NjUxOTI3NDAyLDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDY1NmU'
        '=", "tracks": {"href": '
        '"https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks'
        '", "total": 50}, "type": "playlist", "uri": '
        '"spotify:playlist:37i9dQZEVXbMDoHDwVN2tF"}'
    )

    def test_playlist_extract(self):
        playlist: spotify.Playlist = spotifyApi.extract_playlist(
            "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si"
            "=gUkqHK2nQi-gSChD8sEygQ"
        )
        self.assertEqual(len(playlist.tracks), 50)
        self.assertEqual(playlist.name, "Top 50 - Global")

    def test_playlist_extract_async(self):
        playlist: spotify.Playlist = asyncio.run(
            spotifyApi.extract_playlist_async(
                "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si"
                "=gUkqHK2nQi-gSChD8sEygQ"
            )
        )
        self.assertEqual(len(playlist.tracks), 50)
        self.assertEqual(playlist.name, "Top 50 - Global")

    def test_long_playlist_extract(self):
        playlist: spotify.Playlist = spotifyApi.extract_playlist(
            "https://open.spotify.com/playlist/54M8OXtk3d4rQrAhHnOPhk?si"
            "=vMrbgbXwRoCUhjQezfsNcQ"
        )
        self.assertGreaterEqual(playlist.tracks.__len__(), 200)

    def test_long_playlist_extract_async(self):
        playlist: spotify.Playlist = asyncio.run(
            spotifyApi.extract_playlist_async(
                "https://open.spotify.com/playlist/54M8OXtk3d4rQrAhHnOPhk?si"
                "=vMrbgbXwRoCUhjQezfsNcQ"
            )
        )
        self.assertGreaterEqual(playlist.tracks.__len__(), 200)

    def test_complete(self):
        self.assertIsNone(TestSpotifyPlaylist.PART_PLAYLIST.tracks)
        playlist: spotify.Playlist = TestSpotifyPlaylist.PART_PLAYLIST.complete(
            spotifyApi.get_auth_token()
        )
        self.assertIsNotNone(playlist.tracks)

    def test_complete_async(self):
        self.assertIsNone(TestSpotifyPlaylist.PART_PLAYLIST.tracks)
        playlist: spotify.Playlist = asyncio.run(
            TestSpotifyPlaylist.PART_PLAYLIST.complete_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertIsNotNone(playlist.tracks)


class TestSpotifySearch(unittest.TestCase):
    def test_search_song(self):
        results = spotify.search(
            "runaway kanye west",
            spotifyApi.get_auth_token(),
            5,
            spotify.SearchType.TRACK,
        )
        self.assertEqual(results[0].id, "3DK6m7It6Pw857FcQftMds")

    def test_search_artist(self):
        results = spotify.search(
            "kanye west",
            spotifyApi.get_auth_token(),
            5,
            spotify.SearchType.ARTIST,
        )
        self.assertEqual(results[0].id, "5K4W6rqBFWDnAN6FQUkS6x")

    def test_search_album(self):
        results = spotify.search(
            "my beautiful dark twisted fantasy",
            spotifyApi.get_auth_token(),
            5,
            spotify.SearchType.ALBUM,
        )
        self.assertEqual(results[0].id, "20r762YmB5HeofjMCiPMLv")

    def test_search_playlist(self):
        results = spotify.search(
            "global top 50",
            spotifyApi.get_auth_token(),
            5,
            spotify.SearchType.PLAYLIST,
        )
        self.assertEqual(results[0].id, "37i9dQZEVXbMDoHDwVN2tF")

    def test_search_song_async(self):
        results = asyncio.run(
            spotify.search_async(
                "runaway kanye west",
                asyncio.run(spotifyApi.get_auth_token_async()),
                5,
                spotify.SearchType.TRACK,
            )
        )
        self.assertEqual(results[0].id, "3DK6m7It6Pw857FcQftMds")

    def test_search_artist_async(self):
        results = asyncio.run(
            spotify.search_async(
                "kanye west",
                asyncio.run(spotifyApi.get_auth_token_async()),
                5,
                spotify.SearchType.ARTIST,
            )
        )
        self.assertEqual(results[0].id, "5K4W6rqBFWDnAN6FQUkS6x")

    def test_search_album_async(self):
        results = asyncio.run(
            spotify.search_async(
                "my beautiful dark twisted fantasy",
                asyncio.run(spotifyApi.get_auth_token_async()),
                5,
                spotify.SearchType.ALBUM,
            )
        )
        self.assertEqual(results[0].id, "20r762YmB5HeofjMCiPMLv")

    def test_search_playlist_async(self):
        results = asyncio.run(
            spotify.search_async(
                "global top 50",
                asyncio.run(spotifyApi.get_auth_token_async()),
                5,
                spotify.SearchType.PLAYLIST,
            )
        )
        self.assertEqual(results[0].id, "37i9dQZEVXbMDoHDwVN2tF")


class TestSpotifyArtist(unittest.TestCase):
    PART_ARTIST = spotify.Artist.from_api_response(
        '{"external_urls": {"spotify": '
        '"https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau"}, "href": '
        '"https://api.spotify.com/v1/artists/1r4hJ1h58CWwUQe3MxPuau", '
        '"id": "1r4hJ1h58CWwUQe3MxPuau", "name": "Maluma", "type": "artist", '
        '"uri": "spotify:artist:1r4hJ1h58CWwUQe3MxPuau"}'
    )

    def test_extract_artist(self):
        artist: spotify.Artist = spotify.Artist.from_id(
            "0xOeVMOz2fVg5BJY3N6akT", spotifyApi.get_auth_token()
        )
        self.assertEqual(artist.name, "Jaden")

    def test_get_albums(self):
        albums: List[spotify.Album] = spotify.Artist.from_id(
            "0xOeVMOz2fVg5BJY3N6akT", spotifyApi.get_auth_token()
        ).get_albums(spotifyApi.get_auth_token())
        self.assertGreaterEqual(20, len(albums))

    def test_top_tracks(self):
        tracks: List[spotify.Track] = spotify.Artist.from_id(
            "0xOeVMOz2fVg5BJY3N6akT", spotifyApi.get_auth_token()
        ).get_top_tracks(spotifyApi.get_auth_token())
        self.assertEqual(len(tracks), 10)

    def test_extract_artist_async(self):
        artist: spotify.Artist = asyncio.run(
            spotify.Artist.from_id_async(
                "0xOeVMOz2fVg5BJY3N6akT",
                asyncio.run(spotifyApi.get_auth_token_async()),
            )
        )
        self.assertEqual(artist.name, "Jaden")

    def test_get_albums_async(self):
        albums: List[spotify.Album] = asyncio.run(
            asyncio.run(
                spotify.Artist.from_id_async(
                    "0xOeVMOz2fVg5BJY3N6akT",
                    asyncio.run(spotifyApi.get_auth_token_async()),
                )
            ).get_albums_async(asyncio.run(spotifyApi.get_auth_token_async()))
        )
        self.assertGreaterEqual(20, len(albums))

    def test_top_tracks_async(self):
        tracks: List[spotify.Track] = asyncio.run(
            asyncio.run(
                spotify.Artist.from_id_async(
                    "0xOeVMOz2fVg5BJY3N6akT",
                    asyncio.run(spotifyApi.get_auth_token_async()),
                )
            ).get_top_tracks_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertEqual(len(tracks), 10)

    def test_complete(self):
        self.assertIsNone(TestSpotifyArtist.PART_ARTIST.followers)
        completed = TestSpotifyArtist.PART_ARTIST.complete(
            spotifyApi.get_auth_token()
        )
        self.assertIsNotNone(completed.followers)

    def test_complete_async(self):
        self.assertIsNone(TestSpotifyArtist.PART_ARTIST.followers)
        completed = asyncio.run(
            TestSpotifyArtist.PART_ARTIST.complete_async(
                asyncio.run(spotifyApi.get_auth_token_async())
            )
        )
        self.assertIsNotNone(completed.followers)


if __name__ == "__main__":
    unittest.main()
