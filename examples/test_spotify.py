from joi_skill_utils.spotify import Spotify
from joi_skill_utils.enviro import get_setting
import pandas as pd
import random

sp = Spotify()
playlists = sp.get_playlists()

playlist_id = '2LjLbyEEw9aRqMZo5qpK4O'
tracks = sp.get_playlist_tracks(playlist_id)
print(len(tracks))

for track in tracks:
    features = sp.get_audio_features(track.id)
    track.energy = features.energy

# sort the list in place
list.sort(tracks,key=lambda o: o.energy)

for track in tracks:
    print(f"{track.name}, {track.energy}")

# split list by slow and fast songs
# choose a few slow and fast songs
slow_songs = random.sample(tracks[:len(tracks)//2],3)
fast_songs = random.sample(tracks[len(tracks)//2:],3)

sorted_list = sorted(slow_songs + fast_songs, key=lambda o: o.energy)

def build_pyramid(sorted_list):
    even = sorted_list[::2]
    odd = sorted_list[1::2]
    return even + list(reversed(odd))

print("-----")
for track in build_pyramid(sorted_list):
    print(f"{track.energy}")

