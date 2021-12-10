from convert import convert


def main():
    s_key = ["client key", "secret"]
    am_key = "" # not required if you just want to create a TXT file
    c = convert([s_key, am_key], s=True)
    c.convert_playlist("https://open.spotify.com/playlist/2Kiqv0H8nOGBiQWTopLWTn?si=8dde288f93cf4a87")


if __name__ == "__main__":
    main()
