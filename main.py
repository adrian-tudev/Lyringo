import spotify_client
import genius_client
import translate_client

def main():
    token = spotify_client.get_token()
    
    #print(genius_client.get_song_lyrics("PUNTO G", "Quevedo"))
    #print(spotify_client.search_for_artist(token, "nfeiwjfhwejlfowef"))
    random_song = spotify_client.get_random_song_from_playlist(token, "https://open.spotify.com/playlist/6dhcLtSj6VxpVrXjzfpTV0?si=56ef23f5b7f94d51")

    track = random_song.get("track_name")
    artists = random_song.get("artist_names", [])
    primary_artist = artists[0]

    lyrics = genius_client.get_song_lyrics(track, primary_artist)
    formatted_lyrics = genius_client.clean_lyrics(lyrics)
    
    target_language = "en"
    translated_formatted = translate_client.translate_song(formatted_lyrics, target_language)
    
    print(translated_formatted)

if __name__ == "__main__":
    main()