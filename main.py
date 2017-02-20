#!/usr/bin/env python3

# Main for interacting with the ROBDD

import argparse

def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='ROBDD')
    parser.add_argument('-b', '--boolean_expr', dest='input_expr', metavar='B',
                        type=str, nargs='?',help='Provide a boolean expression')

    args = parser.parse_args()
    print(args)

if __name__ =='__main__':
    main()
