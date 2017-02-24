#!/usr/bin/env python3

# Main for interacting with the ROBDD
# Libraries:
#   -pyeda, a python EDA library. It provides a lot of functionality, I am only
#   using its expression conversion functionality so that I don't have to roll my
#   own using lex, flex, etc.

import argparse
import re
from pyeda.boolalg.expr import exprvar, expr
import sys

from robdd import Robdd
from robdd_apply import Robdd_apply

#sys.setrecursionlimit(100000)

def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='ROBDD')
    parser.add_argument('-b', '--boolean_expr', dest='input_expr', metavar='B',
                        type=str, nargs='?',help='Provide a boolean expression')
    parser.add_argument('-b2', '--boolean_expr2', dest='input_expr2', metavar='B2',
                        type=str, nargs='?',help='Provide a boolean expression')

    # Parse the input arguments
    args = parser.parse_args()

    expression1 = str(expr(args.input_expr))
    expression2 = str(expr(args.input_expr2))

    r1 = Robdd(find_large_var(expression1))
    r1.build(expression1)
    r1.print_graph()

    # r2 = Robdd(find_large_var(expression2))
    # r2.build(expression2)
    #
    # r3 = Robdd_apply(5)
    # r3.apply("**", r1, r2)
    # r3.print_graph()

def find_large_var(expression):
    result = [e for e in re.split("[^0-9]", expression) if e != '']
    # list 'result' elements are strings: ['3', '17', '14'], so we use map(int, list) to get integers
    return max(map(int, result))

if __name__ =='__main__':
    main()
