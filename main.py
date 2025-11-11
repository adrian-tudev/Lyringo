import spotify_client
import genius_client
import translate_client

def main():
    token = spotify_client.get_token()
    print("Welcome to Lyringo!")
    print("Insert a Spotify playlist link: ")
    link = input()
    print("Choosing a random song from your playlist...")
    random_song = spotify_client.get_random_song_from_playlist(token, link)
    track = random_song.get("track_name")
    artists = random_song.get("artist_names", [])
    primary_artist = artists[0]

    lyrics = genius_client.get_song_lyrics(track, primary_artist)
    formatted_lyrics = genius_client.clean_lyrics(lyrics)

    detected = translate_client.announce_song_language(track, primary_artist, formatted_lyrics)

    print("What language do you want to translate to? ")
    user_lang = input().strip()

    # convert language name like "english" -> "en" using translate_client helper
    # convert language name like "english" -> "en" using translate_client helper
    code = translate_client.language_name_to_code(user_lang)
    if not code:
        # accept two-letter codes directly
        if len(user_lang) == 2 and user_lang.isalpha():
            code = user_lang.lower()
        else:
            print(f"Unknown language '{user_lang}', defaulting to English ('en').")
            code = "en"
    print("Setting things up...")

    # make sure a song was actually chosen
    if not random_song:
        print("No song selected. Exiting.")
        return

    translated_formatted = translate_client.translate_song(formatted_lyrics, code)
    print(lyrics)
    print(translated_formatted)

if __name__ == "__main__":
    main()