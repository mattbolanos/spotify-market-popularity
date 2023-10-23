# import libraries
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

# load functions
from functions.spotify_api import SpotifyAPI

# SET LIMIT - this whole script takes a while to run and may end up in rate limiting
# This script is for demonstration purposes, albeit functional, and is not intended to be run in full
scrape_lim = 3

# read in secrets
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# init api
spotify = SpotifyAPI(client_id=client_id, client_secret=client_secret)

# -- Webdriver -- #

print("-- opening webdriver --")

# scrape playlists
browser = webdriver.Chrome()
browser.get("https://open.spotify.com/genre/section0JQ5DAzQHECxDlYNI6xD1h")

## USER NOTE - scroll to bottom of page to load all playlists
time.sleep(3)

# Find all "a" tags with title containing "Top Songs"
anchor_elements = browser.find_elements(By.XPATH, '//a[contains(@title, "Top Songs")]')

# Extract hrefs from the anchor elements
playlist_hrefs = [elem.get_attribute("href") for elem in anchor_elements]

# Close browser
browser.close()

# -- Playlists -- #
print("")
print("-- scraping playlists --")

# extract playlist ids from hrefs
playlist_ids = [href.split("/")[-1] for href in playlist_hrefs]

# init list to store all data
top_50_playlists = []

# call api for each playlist
for playlist_id in playlist_ids[:scrape_lim]:
    playlist_res = spotify.request_playlist(playlist_id=playlist_id)
    # keep playlist name
    playlist_name = playlist_res["name"]
    print("-- processing playlist: " + playlist_name, "--")
    # extract tracks
    playlist_tracks = playlist_res["tracks"]["items"]
    # loop through tracks
    for track in playlist_tracks:
        # parse track
        track_json = spotify.parse_playlist_track(track=track, playlist_id=playlist_id, playlist_name=playlist_name)
        # append to list
        top_50_playlists.append(track_json)

# -- Artists -- #
print("")
print("-- scraping artists --")

# get artist ids
artist_ids = list(set([artist["id"] for playlist in top_50_playlists for artist in playlist["artist_ids"]]))

# init list to store all data
artists = []

for artist_id in artist_ids[:scrape_lim]:
    artists.append(spotify.request_artist(artist_id=artist_id))

# -- Audio Features -- #
print("")
print("-- scraping audio features --")

# get track ids
track_ids = list(set([track["track_id"] for track in top_50_playlists]))

# init list to store all data
audio_features = []

for track_id in track_ids[:scrape_lim]:
    # retrieve audio features
    audio_features.append(spotify.request_audio_features(track_id=track_id))

# -- Data Write -- #
# top 50 playlists
# with open("path_to_data/spotify_top_50_playlists.json", "w") as outfile:
#     json.dump(top_50_playlists, outfile)
# artists
# with open("path_to_data/spotify_artists.json", "w") as outfile:
#     json.dump(artists, outfile)
# audio features
# with open("path_to_data/spotify_audio_features.json", "w") as outfile:
#     json.dump(all_audio_features, outfile)
