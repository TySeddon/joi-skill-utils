from joi_skill_utils.google_photo import GooglePhoto

# get list of photo albums and their IDs.
# ID is needed in Memory Box
client = GooglePhoto()
albums = client.get_albums()
for album in albums:
    print(f"{album.title}, {album.id}")
