#!/usr/bin/env python3

# Colin Burgin

# Main for interacting with the ROBDD
# Libraries:
#   -pyeda, a python EDA library. It provides a lot of functionality, I am only
#   using its expression conversion functionality so that I don't have to roll my
#   own using lex, flex, etc.

import argparse
import re
from pyeda.boolalg.expr import expr

from robdd import Robdd
from robdd_apply import Robdd_apply
from robdd_restrict import Robdd_restrict
from robdd_sat import Robdd_sat

def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='ROBDD')
    parser.add_argument('-b', '--boolean_expr', dest='expr_1', metavar='B',
                        type=str, nargs='?',help='Provide a boolean expression')
    parser.add_argument('-b2', '--boolean_expr2', dest='expr_2', metavar='B2',
                        type=str, nargs='?',help='Provide a boolean expression')
    parser.add_argument('-a', '--apply', dest='apply_expr', metavar='A',
                        type=str, nargs='?', help='Provide the operation to apply (And, Or, Equal, Implies)')
    parser.add_argument('-r', '--restrict', dest='restrict_expr', metavar='R',
                        type=str, nargs='?', help='Provide the restriction "var,val"')
    parser.add_argument('-s', '--sat', dest='sat', action='store_true',
                        help='Return SAT on ROBDD')


    # Parse the input arguments
    args = parser.parse_args()

    if args.expr_1 is not None:
        expression1 = str(expr(args.expr_1))
        print("Expression1: " + expression1)
        r1 = Robdd(find_large_var(expression1))
        r1.build(expression1)
        r1.print_graph("r1")

    if args.expr_2 is not None:
        expression2 = str(expr(args.expr_2))
        print("Expression2: " + expression2)
        r2 = Robdd(find_large_var(expression2))
        r2.build(expression2)
        r2.print_graph("r2")

    if args.apply_expr is not None:
        r3 = Robdd_apply(max(find_large_var(expression1), find_large_var(expression2)))
        r3.apply(convert_apply(args.apply_expr), r1, r2)
        r3.print_graph("r3_apply")

    if args.restrict_expr is not None:
        r4 = Robdd_restrict(r1)
        r4.restrict(int(args.restrict_expr.split(',')[0]), int(args.restrict_expr.split(',')[1]))
        r4.print_graph('r4_restrict')

    if args.sat:
        r4 = Robdd_sat(r1)
        r4.print_SAT()

    # Convert input expression into a form I can evaluate
def convert_apply(expr):
    # Replace all of the operators with my class operators
    expr = expr.replace("And", "and")
    expr = expr.replace("Or", "or")
    expr = expr.replace("Implies", "**")
    expr = expr.replace("Equal", "==")
    return expr

def find_large_var(expression):
    result = [e for e in re.split("[^0-9]", expression) if e != '']
    # list 'result' elements are strings: ['3', '17', '14'], so we use map(int, list) to get integers
    return max(map(int, result))

if __name__ =='__main__':
    main()
