#!/usr/bin/env python3

# Colin Burgin

# Perform SAT functions on an ROBDD, Inherits from the base ROBDD class

from robdd import Robdd

class Robdd_sat(Robdd):
    """Robdd SAT functions in Python 3.5"""

    def __init__(self, robdd_in):

        # Create data structures and vars for ROBDD
        self.num_vars = 0
        self.num_nodes = 0

        # Init T and H
        self.init_T()
        self.init_H()

        # Create data structures and vars for ROBDD
        self.num_vars = robdd_in.get_num_vars()
        self.num_nodes = robdd_in.get_num_nodes()

        # SAT stuff
        self.T = robdd_in.get_T()
        self.SAT_table = self.num_nodes * [False]
        self.SAT_var_state = self.num_vars * [-1]
        self.satisfy = True


    # Calls the recursive function
    def sat_count(self):
        return self.count(self.num_nodes - 1)

    # Recursive function call that follows the algorithm
    def count(self, u):
        # Check to see if youve already visited this node
        if self.SAT_table[u]:
            return self.SAT_table[u]

        # Check to see if leaf node
        if (u is 1) or (u is 0):
            return u
        else:
            _low = (2**(self.T[self.T[u][1]][0] - self.T[u][0] - 1)) * self.count(self.T[u][1])
            _high = (2**(self.T[self.T[u][2]][0] - self.T[u][0] - 1)) * self.count(self.T[u][2])
            return _low + _high

    # Calls the recursive any sat function.  Does some cleanup after its done
    def any_sat(self):
        self.any_sat_r(self.num_nodes-1)
        if self.satisfy:
            # Replace the dont care vars with x's
            self.SAT_var_state = ['x' if x==-1 else x for x in self.SAT_var_state]
        return self.SAT_var_state

    # Recursive any sat function
    def any_sat_r(self, u):

        # Handle some odd cases in the algorith and then implement algorithm
        if u is 0:
            self.satisfy = False
            return
        elif u is 1:
            return
        elif self.T[u][1] is 0:
            self.SAT_var_state[self.T[u][0]-1] = 1
            self.any_sat_r(self.T[u][2])
            return
        else:
            self.SAT_var_state[self.T[u][0]-1] = 0
            self.any_sat_r(self.T[u][1])
            return

    # Function that prints out the sat count and any sat results
    def print_SAT(self):
        self.any_sat()

        x = []
        for i in range(1,self.num_vars+1):
            x.append("x"+str(i))

        print("SAT count: " + str(self.sat_count()))
        print("\nAny SAT:")
        print(*x, sep='\t')
        print(*self.SAT_var_state, sep="\t")
