# import packages
import random
import time
import requests
import base64


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_headers = self.get_auth_headers()

    def call_api(self, endpoint: str) -> dict:
        """call spotify api

        Args:
            endpoint (str): api endpoint
        Returns:
            dict: response json
        """
        # construct url
        url = "https://api.spotify.com/v1/" + endpoint

        # call api
        return requests.get(url, headers=self.auth_headers).json()

    def get_auth_headers(self) -> dict:
        """get authorization headers from Spotify API"""
        # client auth
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")

        # headers
        headers = {"Authorization": f"Basic {auth_header}"}

        # data
        data = {"grant_type": "client_credentials"}

        # call api
        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

        # check response
        if response.status_code == 200:
            token = response.json()["access_token"]
        else:
            raise Exception("could not retrieve access token")
        return {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

    @staticmethod
    def random_sleep():
        """sleep for a random amount of time"""
        time.sleep(random.uniform(1, 2))

    @staticmethod
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

    def request_playlist(self, playlist_id: str) -> dict:
        """request playlist from spotify api

        Args:
            playlist_id (str): playlist id
            auth_headers (dict): authorization headers
        Returns:
            dict: playlist json
        """
        # call api
        playlist_res = self.call_api("playlists/" + playlist_id)
        return playlist_res if "id" in playlist_res.keys() else {"playlist_id": playlist_id}

    def request_artist(self, artist_id: str, silent: bool = False) -> dict:
        """retrieve artist data from spotify api

        Args:
            artist_id (str): artist id
            auth_headers (dict): authorization headers

        Returns:
            dict: artist data json
        """
        # call api
        artist_res = self.call_api("artists/" + artist_id)

        if "id" in artist_res.keys():
            # followers
            followers = artist_res["followers"]["total"]

            # genres
            genres = artist_res["genres"]

            # popularity
            popularity = artist_res["popularity"]

            # name
            artist_name = artist_res["name"]

            if not silent:
                print("-- retrieved artist: " + artist_name, "--")

            # random sleep
            self.random_sleep()

            # append to list
            return {
                "artist_id": artist_id,
                "artist_name": artist_name,
                "followers": followers,
                "genres": genres,
                "popularity": popularity,
            }

    def request_audio_features(self, track_id: str, silent: bool = False) -> dict:
        """request audio features from spotify api

        Args:
            track_id (str): track id
            auth_headers (dict): authorization headers
        Returns:
            dict: audio features json
        """
        # call api
        track_res = self.call_api("audio-features/" + track_id)

        # random sleep
        self.random_sleep()

        if "id" in track_res.keys():
            if not silent:
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
