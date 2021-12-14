import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import time

import requests


class convert:
    def __init__(self, keys: list[list[str, str]], s: bool = None, am: bool = None):
        if not am and not s:
            raise ValueError("Either Spotify or Apple Music are required")
        self.type = "spotify" if s else "am"
        self.spotify = self._spotify(keys)
        self.am = self._am(keys)

    def convert_playlist(self, playlist_id: str, link: bool = False):
        if self.type == "spotify":
            self.spotify.get_spotify(playlist_id, link)
        else:
            self.am.get_am(playlist_id)
        print("Done!")

    class _spotify:
        def __init__(self, keys: list[list[str, str]]):
            super().__init__()
            self.keys = keys
            self.spotify_key = keys[0]
            self.converted = []
            self.manager = spotipy.Spotify

        def get_spotify(self, id, links):
            try:
                auth_manager = SpotifyClientCredentials(client_id=self.spotify_key[0],
                                                        client_secret=self.spotify_key[1])
            except spotipy.oauth2.SpotifyOauthError:
                raise ValueError("Keys cannot be None!")
            self.manager = self.manager(auth_manager=auth_manager)
            tracks = self.spotify_tracks(id)
            track_info = []
            print("Gathering Track Info...")
            for track in tracks:
                info = self.spotify_info(track)
                try:
                    track_info.append([info["name"], info["album"]["name"], info["album"]["artists"][0]["name"]])
                    time.sleep(.1)
                except TypeError:
                    pass
            self.to_am(track_info)
            with open("tracks.txt", "w") as file:
                for i, url in enumerate(self.converted):
                    if links:
                        file.write(f"{url}\n")
                    else:
                        file.write(f"{track_info[i][0]} By {track_info[i][2]} On {track_info[i][1]} - {url}\n")

        def spotify_tracks(self, id: str):
            track_ids = []
            playlist = self.manager.playlist(id)
            for item in playlist['tracks']["items"]:
                track = item["track"]
                track_ids.append(track["id"])
            return track_ids

        def spotify_info(self, id):
            try:
                return self.manager.track(id)
            except AttributeError:
                return print("Cannot parse Local Files\n")

        def to_am(self, tracks):
            print("Searching Itunes...")
            for track in tracks:
                for i, _ in enumerate(iter(bool, True)):

                    name = f"{track[0]} - {track[2]}"
                    url = f"https://itunes.apple.com/search?term={name.replace(' ', '+')}&limit={i + 1}"
                    try:
                        response = requests.get(url).json()["results"][0]
                    except Exception as e:
                        print(e)
                        break
                    if response["artistName"] != track[2]:
                        print(f'Warning: Track "{name}" Could not be found')
                        break
                    else:
                        print(f"Found {name}")
                    self.converted.append(response["collectionViewUrl"])
                    break

    class _am:
        def __init__(self, keys: list[list[str, str]]):
            self.keys = keys

        def get_am(self):
            pass


class applemusic(convert):
    def __init__(self, keys, s, am):
        super().__init__(keys, s, am)

    def get_am(self, id):
        pass
