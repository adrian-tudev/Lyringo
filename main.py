import re
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

    # Fetch lyrics and metadata (get_song_lyrics now returns a dict with
    # keys 'formatted' and 'language'). We prefer the language reported by
    # the provider instead of doing automatic detection.
    lyrics_info = genius_client.get_song_lyrics(track, primary_artist)
    formatted_lyrics = None
    lyrics_language = None
    if isinstance(lyrics_info, dict):
        formatted_lyrics = lyrics_info.get("formatted")
        lyrics_language = lyrics_info.get("language")
    else:
        # fallback for older return shape
        formatted_lyrics = lyrics_info

    if lyrics_language:
        # convert returned code/name to a friendly display name
        display = translate_client.code_to_display_name(lyrics_language)
        print(f"The song is in {display}")
    else:
        print("Song language not provided by lyrics metadata.")

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

    # Start the translation game: for each non-empty line in the lyrics body,
    # ask the user to type the translation into the chosen language. After the
    # user answers, show the correct translation and keep score.
    header, body = translate_client._extract_header(formatted_lyrics or "")
    lines = [line for line in body.splitlines()]

    def _normalize(s: str) -> str:
        # Lowercase, remove punctuation and collapse whitespace for comparison.
        if s is None:
            return ""
        s = s.lower()
        s = re.sub(r"[^a-z0-9\s]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    total = 0
    score = 0

    print("Starting the translation game. Translate each displayed line into your chosen language.")
    print("Leave blank to skip a line. Press Ctrl+C to quit early.")

    for orig in lines:
        orig_strip = orig.strip()
        if not orig_strip:
            # keep paragraph breaks but don't quiz blank lines
            continue

        total += 1
        print(f"\nOriginal: {orig_strip}")
        answer = input("Your translation: ").strip()

        # Get the expected translation from the translate client.
        try:
            expected_full = translate_client.translate_song(orig_strip, code)
        except Exception:
            expected_full = orig_strip

        # extract body in case the translator wrapped headers
        _, expected_body = translate_client._extract_header(expected_full)

        if not answer:
            print(f"Skipped. Correct: {expected_body}")
        else:
            if _normalize(answer) == _normalize(expected_body):
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. Correct: {expected_body}")

    print(f"\nGame over — score: {score}/{total} ({(score/total*100) if total else 0:.1f}%)")

if __name__ == "__main__":
    main()