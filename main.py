from client import Client
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-du", "--duration", nargs="2", help="expects two arguments")
    parser.add_argument("-t", "--tags", nargs="*", help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--format", help="the audio files will have the defined format")
    parser.add_argument("-sr", "--sample-rate", help="the audio files will only have the samplerates specified")
    parser.add_argument("-qu", "--query", default="*", help="the query used for searching")
    parser.add_argument("-bd", "--bit-depth", help="define the bit depth")
    parser.add_argument("-br", "--bit-rate", help="define the bit size")
    parser.add_argument("-ch", "--channel", help="define the amount of channels")
    parser.add_argument("-dp", "--download-path", default="./", help="define the path where files are downloaded")
    args = parser.parser_args()
