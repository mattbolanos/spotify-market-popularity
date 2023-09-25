# import packages
from spotipy import Spotify
import random
import time


def random_sleep():
    """sleep for a random amount of time between .5 and 1.5 seconds"""
    time.sleep(random.uniform(0.5, 1.5))


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


def retrieve_artist(artist_id: str, sp: Spotify) -> dict:
    """retrieve artist data from spotify api

    Args:
        artist_id (str): artist id

    Returns:
        dict: artist data json
    """
    # call api
    artist_res = sp.artist(artist_id=artist_id)

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


def retrieve_audio_features(track_id: str, sp: Spotify) -> dict:
    """retrieve audio features from spotify api

    Args:
        track_id (str): track id
        sp (Spotify): spotify api object

    Returns:
        dict: audio features json
    """
    # call api
    track_res = sp.audio_features(tracks=track_id)[0]

    # random sleep
    random_sleep()

    if track_res:
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
        return None
