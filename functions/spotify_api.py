# import packages
import random
import time
import requests
import base64


def random_sleep():
    """sleep for a random amount of time"""
    time.sleep(random.uniform(1.5, 3))


def parse_playlist_track(track: dict, playlist_id: str, playlist_name: str) -> dict:
    """parses a track object from a playlist object

    Args:
        track (dict): track object
        playlist_id (str): playlist id
        playlist_name (str): playlist name
    Returns:
        (dict): parsed track object
    """
    # go down one level
    track = track["track"]

    # track id
    track_id = track["id"]

    # track name
    track_name = track["name"]

    # album object
    track_album = track["album"]
    album_type = track_album["album_type"]
    album_id = track_album["id"]

    # artists object
    artist_ids = [{"id": artist["id"]} for artist in track["artists"]]

    # avail markets
    avail_markets = track["available_markets"]

    # explicit
    explicit = track["explicit"]

    # popularity
    popularity = track["popularity"]

    # convert into one json
    return {
        "track_id": track_id,
        "track_name": track_name,
        "playlist_id": playlist_id,
        "playlist_name": playlist_name,
        "album_type": album_type,
        "album_id": album_id,
        "artist_ids": artist_ids,
        "explicit": explicit,
        "popularity": popularity,
        "available_markets": avail_markets,
    }


def request_playlist(playlist_id: str, auth_headers: dict) -> dict:
    """request playlist from spotify api

    Args:
        playlist_id (str): playlist id
        auth_headers (dict): authorization headers
    Returns:
        dict: playlist json
    """
    # call api
    playlist_res = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id, headers=auth_headers).json()

    if "id" in playlist_res.keys():
        return playlist_res
    else:
        return {"playlist_id": playlist_id}


def request_artist(artist_id: str, auth_headers: dict) -> dict:
    """retrieve artist data from spotify api

    Args:
        artist_id (str): artist id
        auth_headers (dict): authorization headers

    Returns:
        dict: artist data json
    """
    # call api
    artist_res = requests.get("https://api.spotify.com/v1/artists/" + artist_id, headers=auth_headers).json()

    if "id" in artist_res.keys():
        # followers
        followers = artist_res["followers"]["total"]

        # genres
        genres = artist_res["genres"]

        # popularity
        popularity = artist_res["popularity"]

        # name
        artist_name = artist_res["name"]

        print("-- retrieved artist: " + artist_name, "--")

        # random sleep
        random_sleep()

        # append to list
        return {
            "artist_id": artist_id,
            "artist_name": artist_name,
            "followers": followers,
            "genres": genres,
            "popularity": popularity,
        }


def request_audio_features(track_id: str, auth_headers: dict) -> dict:
    """request audio features from spotify api

    Args:
        track_id (str): track id
        auth_headers (dict): authorization headers
    Returns:
        dict: audio features json
    """

    track_res = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=auth_headers).json()

    # random sleep
    random_sleep()

    if "id" in track_res.keys():
        print("-- retrieved audio features: " + track_id, "--")
        return {
            "track_id": track_id,
            "danceability": track_res["danceability"],
            "energy": track_res["energy"],
            "key": track_res["key"],
            "loudness": track_res["loudness"],
            "mode": track_res["mode"],
            "speechiness": track_res["speechiness"],
            "acousticness": track_res["acousticness"],
            "instrumentalness": track_res["instrumentalness"],
            "liveness": track_res["liveness"],
            "valence": track_res["valence"],
            "tempo": track_res["tempo"],
            "duration_ms": track_res["duration_ms"],
            "time_signature": track_res["time_signature"],
        }
    else:
        if track_res["error"]["status"] == 429:
            raise Exception("rate limit exceeded")
        print("audio features error")
        return {"track_id": track_id}


def get_auth_headers(client_id: str, client_secret: str) -> dict:
    """
    get access token from Spotify API

    Args:
        client_id (str): client id
        client_secret (str): client secret
    Returns:
        (dict): authorization headers
    """

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {auth_header}"}

    data = {"grant_type": "client_credentials"}

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code == 200:
        token = response.json()["access_token"]
    else:
        raise Exception("could not retrieve access token")

    auth_headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

    return auth_headers
