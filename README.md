# emo-music
background music for videos based on the emotions of the people in it

## Resources:
[Documentation for Azure Face API](https://docs.microsoft.com/en-us/azure/cognitive-services/Face/QuickStarts/Python)

>>> import spotipy (pip3 install spotipy)
>>> scc = SpotifyClientCredentials(client_id = 'b03077619b9748a5b8926a13ffa20e5d', client_secret = 'bf61d28f68ba48e7a9f3515a1070d4df')
>>> scc
<spotipy.oauth2.SpotifyClientCredentials object at 0x101a85e48>
>>> sp = spotipy.Spotify(client_credentials_manager = scc)
>>> results = sp.artist_top_tracks('spotify:artist:36QJpDe2go2KgaRleHCDTp')
