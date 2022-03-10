from pprint import pprint
from joi_skill_utils.google_photo import GooglePhoto

# test
client = GooglePhoto()

albums = client.get_albums()
for album in albums:
    print(f"{album.title}, {album.id}")

album_id = ''

mediaItems = client.get_media_items(album_id=album.id)
print('===Getting Media Items=============')
print(len(mediaItems))
pprint(mediaItems[0])
