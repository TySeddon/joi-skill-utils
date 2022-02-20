from pprint import pprint
from joi_skill_utils.spotify import Spotify

sp = Spotify()
track_id = '6gdLoMygLsgktydTQ71b15'

features = sp.get_audio_features(track_id)
pprint(features)

