import lyricsgenius
import os 
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
genius = lyricsgenius.Genius(token)

