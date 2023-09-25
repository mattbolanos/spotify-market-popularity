# import packages
from spotipy import Spotify


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

    # append to list
    return {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "followers": followers,
        "genres": genres,
        "popularity": popularity,
    }
