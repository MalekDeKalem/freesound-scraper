from client import Client
from oauthcallbackhandler import OAuthCallbackHandler, OAuthServer
import argparse
import os
from dotenv import load_dotenv    
from settings import DEFAULT_TAGS



def main(args):

    load_dotenv()

    client_id = os.getenv('CLIENT_ID')
    api_token = os.getenv('API_TOKEN')
    
    client = Client(client_id, api_token)
    download_path = args.download_path


    oauth_server = OAuthServer()
    print('Opening Browser for Freesound authorization...')

    client.oauth2_authorize()

    code = oauth_server.get_oauth_code(client_id)
    print("This is your auth code! ", code)

    token_info = client.fetch_access_token(code)
    print("Access token:", token_info["access_token"])

    if (args.pack):
        samples_data = client.get_packsounds(pack_id=args.pack, page_size=args.amount)  
        success = client.download_samples(samples=samples_data, target_directory=args.download_path)  
    else:
        filter_string = client.filter_string(tags=args.tags, duration=(args.min_length, args.max_length), sr=args.sample_rate, format=args.format, channels=args.channels)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", default=15, type=int, help="the maximum length of the sound file")
    parser.add_argument("--min-length", default=0, type=int, help="the minimum length of the sound file")
    parser.add_argument("-t", "--tags", nargs="*", default=DEFAULT_TAGS, help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--format", default="wav", type=str, help="the audio files will have the defined format")
    parser.add_argument("-sr", "--sample-rate", type=int, default=44100, help="the audio files will only have the samplerates specified")
    parser.add_argument("-qu", "--query", default="*",type=str, help="the query used for searching")
    parser.add_argument("-ch", "--channels", type=int, default=1, help="define the amount of channels")
    parser.add_argument("-dp", "--download-path", type=str, default="./", help="define the path where files are downloaded")
    parser.add_argument("-n", "--amount", type=int, default=15, help="amount of sound files you want to have");
    parser.add_argument("-p", "--pack", type=int, help="enter the id of the pack you want to have")
    args = parser.parse_args()

    main(args)
