import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbosity', '-v', help='increase output verbosity',
                    action='store_true')
# If we want to evaluate 0 as false we have to cast it to int
# parser.add_argument('--verbosity', help='increase output verbosity', type=int)
args = parser.parse_args()
if args.verbosity:
    print('verbosity turned on')
