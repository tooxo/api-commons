[![Coverage Status](https://coveralls.io/repos/github/tooxo/api-commons/badge.svg?branch=master)](https://coveralls.io/github/tooxo/api-commons?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.com/tooxo/api-commons.svg?branch=master)](https://travis-ci.com/tooxo/api-commons)
# tooxo / api-commons

Wrappers for multiple APIs compiled into one Python package.
All parts of the program are usable synchronous as well as asynchronous with the *asyncio* python package. 

The library is also fully usable without any requirements, as long as it is used in synchronous mode only.
### Services included

* Spotify
* Genius
* SoundCloud

## Services one by one
### <img align="left" width="20" height="20" src="https://raw.githubusercontent.com/simple-icons/simple-icons/4b882220efc78dc824c7647a81b47dd1d4fdd3d8/icons/spotify.svg"> Spotify

Currently implemented: 
* Artist, Album, Track and Playlist Extraction by Id and Url
* Spotify Search

### <img align="left" width="20" height="20" src="https://raw.githubusercontent.com/simple-icons/simple-icons/4b882220efc78dc824c7647a81b47dd1d4fdd3d8/icons/soundcloud.svg"> SoundCloud

Currently implemented:
* Track and Playlist Extraction by Id and Url
* SoundCloud Search

### <img align="left" width="20" height="20" src="https://raw.githubusercontent.com/simple-icons/simple-icons/3db785c36a94b3f15587244f9c2dd3d6275a7097/icons/genius.svg">Genius

Currently implemented:
* Track Search
* Lyrics Extraction


