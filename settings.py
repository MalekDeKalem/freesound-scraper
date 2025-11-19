import os
from dotenv import load_dotenv    


TAGS_TO_IGNORE = ["Blowjob-Sound", "Asmr", "Female-Licking-Sound", "climax", "hentai", "loli", "anime", "moan", "porn", "lewd", "Erotic", "DDLC", "Audio-Porn", "Anime-Girl", "sex", "blowjob", "audio-porn", "blowjob-with-moaning", "Hentai-Audio", "Female-Moan", "female-moan", "erotic", "Female-Laughing", "Female-Giggle", "Cute-Female-Moan", "blowjob-with-moaning", "blowjob-sound-effect", "Cute-Sexy", "Cute-Lewd"]
MAX_DURATION = 3
BASE_URL = "https://freesound.org/apiv2"
SOUNDS = "sounds/"
DOWNLOAD = "download/"
TOKEN_PARAM = "&token=" + os.getenv('API_TOKEN')
ACCESS_TOKEN = "/oauth2/access_token/"
AUTHORIZE = "/oauth2/authorize/"
