def parse_playlist_track(track: dict, playlist_id: str, playlist_name: str) -> dict:
    """parses a track object from a playlist object

    Args:
        track (dict): track object
        playlist_id (str): playlist id
        playlist_name (str): playlist name
    Returns:
        track_json (dict): parsed track object
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
    track_json = {
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

    return track_json
