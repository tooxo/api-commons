import asyncio
import functools
import unittest
import api_commons.genius as genius
from api_commons.common.error import NoResultsFound

KANYE_WEST_RUNAWAY_LYRICS = (
    """[Produced by Kanye West, co-produced by Emile, Jeff Bhasker, & Mike Dean]

[Intro: Rick James & James Brown]
Look at ya, look at ya, look at ya, look at ya
Look at ya, look at ya, look at ya, look at ya
Look at ya, look at ya, look at ya, look at ya
Look at ya, look at ya, look at ya, look at ya (Ladies and gentlemen, ladies, ladies and gentlemen)

[Pre-Chorus: Kanye West]
And I always find, yeah, I always find something wrong
You been puttin' up with my shit just way too long
I'm so gifted at finding what I don't like the most
So I think it's time for us to have a toast

[Chorus: Kanye West]
Let's have a toast for the douchebags
Let's have a toast for the assholes
Let's have a toast for the scumbags
Every one of them that I know
Let's have a toast for the jerk-offs
That'll never take work off
Baby, I got a plan
Run away fast as you can

[Verse 1: Kanye West]
She find pictures in my email
I sent this bitch a picture of my dick
I don't know what it is with females
But I'm not too good at that shit
See, I could have me a good girl
And still be addicted to them hoodrats
And I just blame everything on you
At least you know that's what I'm good at

[Pre-Chorus: Kanye West]
And I always find, yeah, I always find
Yeah, I always find something wrong
You been puttin' up with my shit just way too long
I'm so gifted at finding what I don't like the most
So I think it's time for us to have a toast

[Chorus: Kanye West]
Let's have a toast for the douchebags
Let's have a toast for the assholes
Let's have a toast for the scumbags
Every one of them that I know
Let's have a toast for the jerk-offs
That'll never take work off
Baby, I got a plan
Run away fast as you can

[Bridge: Kanye West & Rick James]
Run away from me, baby
Ah, run away
Run away from me, baby (Look at ya, look at ya, look at ya)
Run away
When it starts to get crazy (Look at ya, look at ya, look at ya)
Then run away
Babe, I got a plan, run away as fast as you can
Run away from me, baby
Run away
Run away from me, baby (Look at, look at, look at, look at, look at, look at, look at ya)
Run away
When it starts to get crazy (Look at ya, look at ya, look at ya, look at ya)
Why can't she just run away?
Baby, I got a plan
Run away as fast as you can (Look at ya, look at ya, look at ya)

[Verse 2: Pusha T]
Twenty-four seven, three sixty-five, pussy stays on my mind
I-I-I-I did it, alright, alright, I admit it
Now pick your next move, you could leave or live with it
Ichabod Crane with that motherfuckin' top off
Split and go where? Back to wearing knockoffs?
Haha, knock it off, Neimans, shop it off
Let's talk over mai tais, waitress, top it off
Hoes like vultures, wanna fly in your Freddy loafers
You can't blame 'em, they ain't never seen Versace sofas
Every bag, every blouse, every bracelet
Comes with a price tag, baby, face it
You should leave if you can't accept the basics
Plenty hoes in the baller-nigga matrix
Invisibly set, the Rolex is faceless
I'm just young, rich, and tasteless, P

[Verse 3: Kanye West]
Never was much of a romantic
I could never take the intimacy
And I know I did damage
'Cause the look in your eyes is killing me
I guess you knew of that advantage
'Cause you could blame me for everything
And I don't know how I'ma manage
If one day, you just up and leave

[Pre-Chorus: Kanye West]
And I always find, yeah, I always find something wrong
You been puttin' up with my shit just way too long
I'm so gifted at finding what I don't like the most
So I think it's time for us to have a toast

[Chorus: Kanye West]
Let's have a toast for the douchebags
Let's have a toast for the assholes
Let's have a toast for the scumbags
Every one of them that I know
Let's have a toast for the jerk-offs
That'll never take work off
Baby, I got a plan
Run away fast as you can

[Outro: Kanye West]
[Non-Lyrical Vocals]"""
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
