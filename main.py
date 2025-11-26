from client import Client
import argparse
import os
from dotenv import load_dotenv    



def main(args):
    
    client = Client(os.getenv('CLIENT_ID'), os.getenv('API_TOKEN'))
    download_path = args.download_path

    if (args.pack):
        samples_data = client.get_packsounds(pack_id=args.pack, page_size=args.amount)  
        success = client.download_samples(samples=samples_data, target_directory=args.download_path)  
    else:
        filter_string = client.filter_string(tags=args.tags, duration=args.duration, sr=args.sample_rate, format=args.format, channels=args.channels)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-du", "--duration", default=[0, 15], nargs="2", help="expects two arguments")
    parser.add_argument("-t", "--tags", nargs="*", default=DEFAULT_TAGS, help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--format", default="wav", type=str, help="the audio files will have the defined format")
    parser.add_argument("-sr", "--sample-rate", type=int, default=44100, help="the audio files will only have the samplerates specified")
    parser.add_argument("-qu", "--query", default="*",type=str, help="the query used for searching")
    parser.add_argument("-ch", "--channel", type=int, default=1, help="define the amount of channels")
    parser.add_argument("-dp", "--download-path", type=str, default="./", help="define the path where files are downloaded")
    parser.add_argument("-n", "--amount", type=int, default=15, help="amount of sound files you want to have");
    parser.add_argument("-p", "--pack", type=int, help="enter the id of the pack you want to have")
    args = parser.parser_args()

    main(args)
