from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from joi_skill_utils.enviro import get_setting

SPOTIPY_CLIENT_ID = get_setting('spotipy_client_id')
SPOTIPY_CLIENT_SECRET = get_setting('spotipy_client_secret')
SPOTIPY_REDIRECT_URI = get_setting('spotipy_redirect_uri')
SPOTIPY_SCOPES = get_setting('spotipy_scopes')

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

search_str = 'Muse'
result = sp.search(search_str)
pprint(result)

