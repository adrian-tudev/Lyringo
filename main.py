import spotify_client
import genius_client

def main():
    print(genius_client.get_song_lyrics("PUNTO G", "Quevedo"))

if __name__ == "__main__":
    main()