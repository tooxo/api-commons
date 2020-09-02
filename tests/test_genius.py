import asyncio
import functools
import unittest
import api_commons.genius as genius
from common.error import NoResultsFound

KANYE_WEST_RUNAWAY_LYRICS = (
    "[Produced by Kanye West, co-produced by Emile, Jeff Bhasker, & Mike "
    "Dean]\n\n[Intro: Rick James & James Brown]\nLook at ya, look at ya, "
    "look at ya, look at ya\nLook at ya, look at ya, look at ya, look at "
    "ya\nLook at ya, look at ya, look at ya, look at ya\nLook at ya, look at "
    "ya, look at ya, look at ya\nLadies and gentlemen, ladies-ladies and "
    "gentlemen\n\n[Pre-Chorus: Kanye West]\nAnd I always find, yeah, I always "
    "find something wrong\nYou been putting up with my shit just way too "
    "long\nI'm so gifted at finding what I don't like the most\nSo I think "
    "it's time for us to have a toast\n\n[Chorus: Kanye West]\nLet's have a "
    "toast for the douchebags\nLet's have a toast for the assholes\nLet's "
    "have a toast for the scumbags\nEvery one of them that I know\nLet's have "
    "a toast for the jerk-offs\nThat'll never take work off\nBaby, I got a "
    "plan\nRun away fast as you can\n\n[Verse 1: Kanye West]\nShe find "
    "pictures in my e-mail\nI sent this bitch a picture of my dick\nI don't "
    "know what it is with females\nBut I'm not too good at that shit\nSee, "
    "I could have me a good girl\nAnd still be addicted to them hoodrats\nAnd "
    "I just blame everything on you\nAt least you know that's what I'm good "
    "at\n\n[Pre-Chorus: Kanye West]\nAnd I always find, yeah, I always "
    "find\nYeah I always find something wrong\nYou been putting up with my "
    "shit just way too long\nI'm so gifted at finding what I don't like the "
    "most\nSo I think it's time for us to have a toast\n\n[Chorus: Kanye "
    "West]\nLet's have a toast for the douchebags\nLet's have a toast for the "
    "assholes\nLet's have a toast for the scumbags\nEvery one of them that I "
    "know\nLet's have a toast for the jerk-offs\nThat'll never take work "
    "off\nBaby, I got a plan\nRun away fast as you can\n\n[Bridge: Kanye West "
    "&Rick James]\nRun away from me, baby, ah, run away\nRun away from me, "
    "baby\n(Look at ya, look at ya, look at ya)\nRun away\nWhen it starts to "
    "get crazy\n(Look at ya, look at ya, look at ya)\nThen, run away\nBabe, "
    "I got a plan, run away as fast as you can\nRun away from me, baby, "
    "run away\nRun away from me, baby\n(Look at-look at-look at-look at-look "
    "at-look at-look at ya)\nRun away\nWhen it starts to get crazy\n(Look at "
    "ya, look at ya, look at ya, look at ya)\nWhy can't she just, "
    "run away?\nBaby, I got a plan, run away as fast as you can\n\n[Verse 2: "
    "Pusha T]\n24/7, 365, pussy stays on my mind\nI-I-I-I did it, alright, "
    "alright, I admit it\nNow pick your next move, you could leave or live "
    "wit' it\nIchabod Crane with that motherfucking top off\nSplit and go "
    "where? Back to wearing knockoffs, haha\nKnock it off, Neiman's, shop it "
    "off\nLet's talk over mai tais, waitress, top it off\nHoes like vultures, "
    "wanna fly in your Freddy loafers\nYou can't blame 'em, they ain't never "
    "seen Versace sofas\nEvery bag, every blouse, every bracelet\nComes with "
    "a price tag, baby, face it\nYou should leave if you can't accept the "
    "basics\nPlenty hoes in the balla-nigga matrix\nInvisibly set, the Rolex "
    "is faceless\nI'm just young, rich, and tasteless, P!\n\n[Verse 3: Kanye "
    "West]\nNever was much of a romantic\nI could never take the "
    "intimacy\nAnd I know I did damage\nCause the look in your eyes is "
    "killing me\nI guess you are at an advantage\nCause you can blame me for "
    "everything\nAnd I don't know how I'ma manage\nIf one day you just up and "
    "leave\n\n[Pre-Chorus: Kanye West]\nAnd I always find, yeah, I always "
    "find something wrong\nYou been putting up with my shit just way too "
    "long\nI'm so gifted at finding what I don't like the most\nSo I think "
    "it's time for us to have a toast\n\n[Chorus: Kanye West]\nLet's have a "
    "toast for the douchebags\nLet's have a toast for the assholes\nLet's "
    "have a toast for the scumbags\nEvery one of them that I know\nLet's have "
    "a toast for the jerk-offs\nThat'll never take work off\nBaby, I got a "
    "plan\nRun away fast as you can\n\n[Outro: Kanye West]\n[Non-Lyrical "
    "Vocals]"
)


class TestGenius(unittest.TestCase):
    def test_genius_search(self):
        r = genius.GeniusApi.search_genius("Runaway Kanye West")
        self.assertEqual(r[0].full_title, "Runaway by Kanye West (Ft. Pusha T)")

    def test_genius_search_not_found(self):
        self.assertRaises(
            NoResultsFound,
            functools.partial(
                genius.GeniusApi.search_genius,
                "AsjOJDoajds8hhcinckjslsfd..dsafdsf32io39043",
            ),
        )

    def test_genius_extraction(self):
        lyrics = genius.GeniusApi.search_genius("Runaway Kanye West")[
            0
        ].to_lyrics(load_annotations=True)

        self.assertEqual(lyrics.lyrics_str, KANYE_WEST_RUNAWAY_LYRICS)

    def test_genius_extraction_async(self):
        lyrics = asyncio.run(
            asyncio.run(
                genius.GeniusApiAsync.search_genius("Kanye West Runaway")
            )[0].to_lyrics_async()
        )

        self.assertEqual(lyrics.lyrics_str, KANYE_WEST_RUNAWAY_LYRICS)


if __name__ == "__main__":
    unittest.main()
