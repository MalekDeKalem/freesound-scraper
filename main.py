from client import Client
import argparse




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", help="maximum length of the sound file")
    parser.add_argument("--max-length", help="minimum length of the sound file")
    parser.add_argument("-t", "--tags", nargs="*", help="the audio files will have either one of those tags in the defined list")
    parser.add_argument("-f", "--formats", nargs="*", help="the audio files will have either one of those audio format defined in the list")


    args = parser.parser_args()
