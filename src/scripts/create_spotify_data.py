# import libraries
import os
import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

# load functions
from functions.spotify_api import parse_playlist_track

# read in secrets
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# authenticate
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:3000",
        scope="user-library-read",
    )
)

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

# extract playlist ids from hrefs
playlist_ids = [href.split("/")[-1] for href in playlist_hrefs]

# init list to store all data
top_50_playlists = []

# call api for each playlist
for playlist_id in playlist_ids[:4]:
    playlist_res = sp.playlist(playlist_id=playlist_id)
    # keep playlist name
    playlist_name = playlist_res["name"]
    print("-- processing playlist: " + playlist_name, "--")
    # extract tracks
    playlist_tracks = playlist_res["tracks"]["items"]
    # loop through tracks
    for track in playlist_tracks:
        # parse track
        track_json = parse_playlist_track(track=track, playlist_id=playlist_id, playlist_name=playlist_name)
        # append to list
        top_50_playlists.append(track_json)

# -- Data Write -- #
# top 50 playlists
with open("data/spotify_top_50_playlists.json", "w") as outfile:
    json.dump(top_50_playlists, outfile)
