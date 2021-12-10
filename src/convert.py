import json.decoder

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import time

import requests

import json


class convert:
    def __init__(self, keys: list[list[str, str], str], s: bool = None, am: bool = None):
        if not am and not s:
            raise ValueError("Either Spotify or Apple Music are required")
        self.spotify_key = keys[0]
        self.am_key = keys[1]
        self.type = "spotify" if s else "am"
        self.converted = []

    def convert_playlist(self, playlist_id: str):
        if self.type == "spotify":
            self.get_spotify(playlist_id)
        else:
            # self.get_am(playlist_id)
            pass
        print("Done!")

    def get_spotify(self, id):
        try:
            auth_manager = SpotifyClientCredentials(client_id=self.spotify_key[0],
                                                    client_secret=self.spotify_key[1])
        except spotipy.oauth2.SpotifyOauthError:
            raise ValueError("Keys cannot be None!")
        sp = spotipy.Spotify(auth_manager=auth_manager)
        tracks = self.spotify_tracks(id, sp)
        track_info = []
        print("Gathering Track Info...")
        for track in tracks:
            info = self.spotify_info(track, sp)
            track_info.append([info["name"], info["album"]["name"], info["album"]["artists"][0]["name"]])
            time.sleep(.3)
        self.to_am(track_info)
        with open("tracks.txt", "w") as file:
            for url in self.converted:
                file.write(f"{url}\n")

    def spotify_tracks(self, id: str, manager: spotipy.Spotify):
        track_ids = []
        playlist = manager.playlist(id)
        for item in playlist['tracks']["items"]:
            track = item["track"]
            track_ids.append(track["id"])
        return track_ids

    def spotify_info(self, id, manager: spotipy.Spotify):
        return manager.track(id)

    def to_am(self, tracks):
        print("Searching Itunes...")
        for track in tracks:
            for i, _ in enumerate(iter(bool, True)):

                name = f"{track[0]} - {track[2]}".replace(" ", "+")
                print(f"Found {name.replace('+', ' ')}")
                url = f"https://itunes.apple.com/search?term={name}&limit={i + 1}"
                try:
                    response = requests.get(url).json()["results"][0]
                except json.decoder.JSONDecodeError:
                    break
                if response["artistName"] != track[2]:
                    print(f"Warning: Track '{track[0]}' Could not be found")
                    break
                self.converted.append(response["collectionViewUrl"])
                break


class applemusic(convert):
    def __init__(self, keys, s, am):
        super().__init__(keys, s, am)

    def get_am(self, id):
        pass
