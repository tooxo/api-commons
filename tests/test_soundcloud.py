import asyncio
import unittest
import api_commons.soundcloud as soundcloud
import urllib.request

sc = soundcloud.SoundCloudApi()
sc_a = soundcloud.SoundCloudApiAsync()


class TestSoundCloud(unittest.TestCase):
    def test_track_extraction(self):
        trk = soundcloud.Track.get_by_url(
            "https://soundcloud.com/iamcardib/wap-feat-megan-thee-stallion",
            sc.get_api_token(),
        )
        self.assertEqual(trk.title, "WAP feat. Megan Thee Stallion")

        res = urllib.request.urlopen(
            urllib.request.Request(url=trk.streams[0].url, method="HEAD")
        )
        self.assertEqual(res.code, 200)

    def test_set_extraction(self):
        sc_set = soundcloud.Set.get_from_url(
            "https://soundcloud.com/kellen-jones-450995894/sets/charts",
            sc.get_api_token(),
        )
        self.assertEqual(sc_set.title, "Charts")
        self.assertEqual(len(sc_set.tracks), 355)

    def test_track_extraction_async(self):
        trk = asyncio.run(
            soundcloud.Track.get_by_url_async(
                "https://soundcloud.com/iamcardib/wap-feat-megan-thee-stallion",
                asyncio.run(sc_a.get_api_token()),
            )
        )
        self.assertEqual(trk.title, "WAP feat. Megan Thee Stallion")

        res = urllib.request.urlopen(
            urllib.request.Request(url=trk.streams[0].url, method="HEAD")
        )
        self.assertEqual(res.code, 200)

    def test_set_extraction_async(self):
        sc_set = asyncio.run(
            soundcloud.Set.get_from_url_async(
                "https://soundcloud.com/kellen-jones-450995894/sets/charts",
                asyncio.run(sc_a.get_api_token()),
            )
        )
        self.assertEqual(sc_set.title, "Charts")
        self.assertEqual(len(sc_set.tracks), 355)


if __name__ == "__main__":
    unittest.main()
