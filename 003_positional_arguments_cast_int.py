import argparse

parser = argparse.ArgumentParser()
# argparse treats the options we give it as strings, unless we tell it otherwise
parser.add_argument('square', help="display a square of a given number", type=int)
args = parser.parse_args()
print(args.square**2)
