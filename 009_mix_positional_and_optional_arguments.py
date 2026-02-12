import argparse

parser = argparse.ArgumentParser()
parser.add_argument('x',
                    type=int,
                    help='the base')
parser.add_argument('y',
                    type=int,
                    help='the exponent')

parser.add_argument('-v', '--verbose',
                    type=int,
                    default=0,
                    help='increase output verbosity, given a number between 0 and 2')
args = parser.parse_args()
answer = args.x ** args.y
if args.verbose >= 2:
    print(f'{args.x} to the power of {args.y} is equal to {answer}.')
elif args.verbose >= 1:
    print(f'{args.x}^{args.y} == {answer}')
else:
    print(answer)
