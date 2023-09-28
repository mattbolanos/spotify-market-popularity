# import libraries
import pandas as pd
import re


def get_data(audio_path: str, artists_path: str, playlists_path: str) -> list:
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
    return add_features(audio_features, artists, playlists)


def add_features(audio_features: pd.DataFrame, artists: pd.DataFrame, playlists: pd.DataFrame) -> list:
    """add features to read in spotify data

    Args:
        audio_features (pd.DataFrame): audio features
        artists (pd.DataFrame): artists
        playlists (pd.DataFrame): playlists
    Returns:
        audio_features (pd.DataFrame): audio features w/ added features
        artists (pd.DataFrame): artists w/ added features
        playlists (pd.DataFrame): playlists w/ added features
    """
    # --- playlists --- #
    # add market ID to playlists
    playlists["market_id"] = (
        playlists["playlist_name"]
        .apply(lambda x: re.sub(r"Top Songs - ", "", x))
        .apply(lambda x: re.sub(r"\s+", "_", x).lower())
    )

    # add # of available markets by counting ","
    # it is a list column so we need to make it a string first
    playlists["num_avail_markets"] = playlists["available_markets"].apply(lambda x: len(str(x).split(",")))

    # count # of artists per song
    playlists["num_artists"] = playlists["artist_ids"].apply(lambda x: sum(1 for item in x if "id" in item))

    # create rank variable, which is row number grouped by market_id
    playlists["playlist_rank"] = playlists.groupby("market_id").cumcount() + 1

    # drop some columns
    playlists.drop(columns=["available_markets", "playlist_name"], inplace=True)

    # rename some columns
    playlists.rename(columns={"popularity": "track_popularity"}, inplace=True)

    # create a longer pivot of playlists to get summary statistics of multi-artists
    playlists_w_artists = playlists.copy().explode("artist_ids")
    playlists_w_artists["artist_id"] = playlists_w_artists["artist_ids"].apply(lambda x: x["id"])
    playlists_w_artists = playlists_w_artists[["artist_id", "track_id"]].drop_duplicates()

    # join artists to playlists_w_artists
    playlists_w_artists = playlists_w_artists.merge(artists, left_on="artist_id", right_on="artist_id")

    # group by track_id,
    # sum followers, and take average of popularity
    track_artist_sum_stats = (
        playlists_w_artists.groupby("track_id")
        .agg({"followers": "sum", "popularity": "mean"})
        .reset_index()
        .rename(
            columns={
                "followers": "tot_artist_followers",
                "popularity": "avg_artist_popularity",
            }
        )
    )

    # join back to playlists
    playlists = playlists.merge(track_artist_sum_stats, left_on="track_id", right_on="track_id")

    return audio_features, artists, playlists
