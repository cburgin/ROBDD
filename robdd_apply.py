#!/usr/bin/env python3

# Colin Burgin

# Perform an operation on two ROBDD's.  Inherits from base ROBDD class

from robdd import Robdd

class Robdd_apply(Robdd):
    """ROBDD apply implementation using python 3.5"""

    def __init__(self, num_vars):

        # Create data structures and vars for ROBDD
        self.num_vars = num_vars
        self.num_nodes = 0

        # Init T, H, and G
        self.init_T()
        self.init_H()
        self.G = {}
        self.op = None

    # Apply the given operation on the two ROBDD's
    def apply(self, op, u1, u2):

        self.op = op
        self.t1 = u1.get_T()
        self.t2 = u2.get_T()

        # Make sure the operation is valid
        if (u1 == None) or not isinstance(u1, Robdd):
            print("Expression 1 is not an ROBDD object")
            return 0
        elif (u2 == None) or not isinstance(u2, Robdd):
            print("Expression 2 is not an ROBDD object")
            return 0
        elif op not in ["and", "or", "**", "=="]:
            print("Operation is not valid")
            return 0

        self.app(u1.get_num_nodes()-1, u2.get_num_nodes()-1)


    # REcursive function which performs the apply
    def app(self, a_idx, b_idx):

        # Check for duplicate
        if(a_idx, b_idx) in self.G:
            return self.G[(a_idx, b_idx)]

        # Get the node values
        a_i, a_l, a_h = self.t1[a_idx]
        b_i, b_l, b_h = self.t2[b_idx]

        # Check to see if they are both leaf nodes else do the algorithm
        if(self.t1[a_idx][1] < 0) and (self.t2[b_idx][1] < 0):
            z = int(eval(str(b_idx) +" "+ str(self.op) +" "+ str(a_idx)))
        elif a_i == b_i:
            z = self.mk(a_i, self.app(a_l, b_l), self.app(a_h, b_h))
        elif a_i < b_i:
            z = self.mk(a_i, self.app(a_l, b_idx), self.app(a_h, b_idx))
        else:
            z = self.mk(b_i, self.app(a_idx, b_l), self.app(a_idx, b_h))

        self.G[(a_idx, b_idx)] = z
        return z
