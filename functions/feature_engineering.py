# import libraries
import pandas as pd


def read_data(audio_path: str, artists_path: str, playlists_path: str):
    """
    read in raw spotify api json data from local files.

    Args:
        audio_path (str): path to audio features json
        artists_path (str): path to artists json
        playlists_path (str): path to playlists json

    Returns:
        audio_features (pd.DataFrame): audio features
        artists (pd.DataFrame): artists
        playlists (pd.DataFrame): playlists
    """
    # audio features
    with open(audio_path) as f:
        audio_features = pd.read_json(f)

    # artists
    with open(artists_path) as f:
        artists = pd.read_json(f)

    # playlists
    with open(playlists_path) as f:
        playlists = pd.read_json(f)

    # return list
    return audio_features, artists, playlists
