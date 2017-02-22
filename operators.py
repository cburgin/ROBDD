#!/usr/bin/env python3

# Operators needed for ROBDD

class Operators:
    """Operators needed for ROBDD, using python 3.5"""

    @staticmethod
    def And(*args):
        curr_arg = args[0]
        for arg in args[1:]:
            curr_arg = arg and curr_arg
        return curr_arg

    @staticmethod
    def Or(*args):
        curr_arg = args[0]
        for arg in args[1:]:
            curr_arg = arg or curr_arg
        return curr_arg

    @staticmethod
    def Implies(x, y):
        return int(y ** x)

    @staticmethod
    def Equal(x, y):
        return x == y
