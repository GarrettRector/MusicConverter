class convert:
    def __init__(self, keys: list[str, str], spotify: bool = None, am: bool = None):
        if not am and not spotify:
            raise ValueError("Either Spotify or Apple Music are required")
        self.spotify_key = keys[0]
        self.am_key = keys[1]
        if spotify:
            self.get_spotify()
        else:
            self.get_am()

    def get_spotify(self):
        pass

    def get_am(self):
        pass
