from client import Client
import argparse


def parse_filter(args):
    pass


def main(args):
    pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-du", "--duration", default=[0, 15], nargs="2", help="expects two arguments")
    parser.add_argument("-t", "--tags", nargs="*", help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--format", default="wav", help="the audio files will have the defined format")
    parser.add_argument("-sr", "--sample-rate", type=int, default=44100, help="the audio files will only have the samplerates specified")
    parser.add_argument("-qu", "--query", default="*", help="the query used for searching")
    parser.add_argument("-ch", "--channel", type=int, default=1, help="define the amount of channels")
    parser.add_argument("-dp", "--download-path", default="./", help="define the path where files are downloaded")
    parser.add_argument("-n", "--amount", type=int, default=15, help="amount of sound files you want to have");
    parser.add_argument("-p", "--pack", type=int, help="enter the id of the pack you want to have")
    args = parser.parser_args()

    main(args)
