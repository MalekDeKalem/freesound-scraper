from client import Client
from oauthcallbackhandler import OAuthCallbackHandler, OAuthServer
import argparse
import os
from dotenv import load_dotenv    
from settings import DEFAULT_TAGS
from textual.app import App

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

    if args.pack:
        samples_data = client.get_packsounds(pack_id=args.pack, page_size=args.amount)

        if args.processes > 1:
            success = client.multi_process_download_samples(samples=samples_data, target_directory=args.download_path)
        else:
            success = client.download_samples(samples=samples_data, target_directory=args.download_path)

    else:
        samples_data = client.get_sounds(page_size=args.amount, query=args.query, tags=args.tags, duration=args.duration, sr=args.sample_rate, form=args.format, channels=args.channels)

        if args.processes > 1:
            success = client.multi_process_download_samples(samples=samples_data, target_directory=args.download_path)
        else:
            success = client.download_samples(samples=samples_data, target_directory=args.download_path)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, nargs=2, help="Duration of the file you want in the FORMAT: begin,end")
    parser.add_argument("-t", "--tags", nargs="*", required=True, help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--format", type=str, help="the audio files will have the defined format")
    parser.add_argument("-sr", "--sample-rate", type=int, help="the audio files will only have the samplerates specified")
    parser.add_argument("-qu", "--query",type=str, help="the query used for searching")
    parser.add_argument("-ch", "--channels", type=int, help="define the amount of channels")
    parser.add_argument("-dp", "--download-path", type=str, default="./", help="define the path where files are downloaded")
    parser.add_argument("-n", "--amount", type=int, default=15, help="amount of sound files you want to have")
    parser.add_argument("-p", "--pack", type=int, help="enter the id of the pack you want to have")
    parser.add_argument("-proc", "--processes", type=int, default=1, help="enter the number of threads that need to be used while downloading")
    args = parser.parse_args()

    main(args)
