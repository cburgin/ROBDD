#!/usr/bin/env python3

# Perform an operation on two ROBDD's

from robdd import Robdd

class Robdd_restrict(Robdd):
    """Robdd Restrict implementation in Python 3.5"""

    def __init__(self, robdd_in):
        # Create data structures and vars for ROBDD
        self.num_vars = robdd_in.get_num_vars()
        self.num_nodes = 0

        # Restrict vars
        self.j = None
        self.b = None
        self.r_nodes = 0

        # Init Restrict
        self.curr_T = robdd_in.get_T()
        self.r_nodes = robdd_in.get_num_nodes()
        self.r = self.r_nodes * [False]

        # Init T, H, and G
        self.init_T()
        self.init_H()

    def restrict(self, j, b):
        self.j = j
        self.b = b

        self.res(self.r_nodes-1)

    def res(self, u):
        a_i, a_l, a_h = self.curr_T[u]
        # Make sure the node is not already restricted
        if self.r[u]:
            return u

        # Implement algorithm
        if self.curr_T[u][0] > self.j:
            self.buildR(u)
            self.r[u] = True
            return u
        elif self.curr_T[u][0] < self.j:
            self.r[u] = True
            return self.mk(a_i, self.res(a_l), self.res(a_h))
        else:
            if self.b == 0:
                self.r[u] = True
                return self.res(a_l)
            else:
                self.r[u] = True
                return self.res(a_h)

    def buildR(self, u):
        if (u is 1) or (u is 0):
            return 0
        a_i, a_l, a_h = self.curr_T[u]
        self.buildR(a_l)
        self.buildR(a_h)
        self.mk(a_i, a_l, a_h)
