#!/usr/bin/env python3

# Main for interacting with the ROBDD
# Libraries:
#   -pyeda, a python EDA library. It provides a lot of functionality, I am only
#   using its expression conversion functionality so that I don't have to roll my
#   own using lex, flex, etc.

import argparse
from pyeda.boolalg.expr import exprvar, expr

def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='ROBDD')
    parser.add_argument('-b', '--boolean_expr', dest='input_expr', metavar='B',
                        type=str, nargs='?',help='Provide a boolean expression')

    # Parse the input arguments
    args = parser.parse_args()

    print(expr(args.input_expr))

if __name__ =='__main__':
    main()
