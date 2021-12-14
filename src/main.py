from convert import convert


def main():
    s_key = ["key", "key"]
    c = convert([s_key], s=True)
    c.convert_playlist("playlist", link=True)


if __name__ == "__main__":
    main()
