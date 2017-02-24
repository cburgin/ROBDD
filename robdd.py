#!/usr/bin/env python3

# Parse a Boolean Expression

from graphviz import Digraph
from subprocess import check_call

from operators import Operators

class Robdd:
    """ROBDD implementation using python 3.5"""

    def __init__(self, num_vars):

        # Create data structures and vars for ROBDD
        self.num_vars = num_vars
        self.num_nodes = 0

        # Init T and H
        self.init_T()
        self.init_H()

    # Implementation of the init(T) function
    def init_T(self):
        self.T = 2 * [3 * [None]]
        # Initilize the 0 and 1 node
        # They are constructed this way so that they have unique hash values
        self.T[0] = [self.num_vars+1, -1, -1]
        self.T[1] = [self.num_vars+1, -2, -2]
        self.num_nodes = 2

    def init_H(self):
        self.H = 2 * [None]
        self.H[0] = hash(str(self.T[0][0])+str(self.T[0][1])+str(self.T[0][2]))
        self.H[1] = hash(str(self.T[1][0])+str(self.T[1][1])+str(self.T[1][2]))

    # mk checks to see if a node already exists and creates a new one if it doesn't
    def mk(self, i, l, h):
        # Check for redundent case
        if l is h:
            return l
        elif self.member(i, l, h):
            return self.lookup(i, l, h)
        else:
            u = self.add(i, l, h)
            self.insert(i, l, h, u)
            return u

    # Check to see if (i, l, h) is already in H
    def member(self, i, l, h):
        # Check to see if the hash already exists in the list H
        return hash(str(i)+str(l)+str(h)) in self.H

    # Return the node index for (i, l, h)
    def lookup(self, i, l, h):
        return self.H.index(hash(str(i)+str(l)+str(h)))

    # Allocate a new node in T with attributes (i, l, h) and return the new node index
    def add(self, i, l, h):
        self.T.append([i, l, h])
        idx = self.num_nodes
        self.num_nodes += 1
        return idx

    # Insert the new node with attributes (i, l, h, u) into H
    def insert(self, i, l, h, u):
        self.H.append(hash(str(i)+str(l)+str(h)))

    # Constructs an ROBDD from a given function
    def build(self, expr, i=1):
        if i > self.num_vars:
            return int(eval(self.convert_expr(expr)))
        else:
            l = self.build(self.build_sub_expr(expr, i, 0), i+1)
            h = self.build(self.build_sub_expr(expr, i, 1), i+1)
            return self.mk(i, l, h)

    # Does the Shannon Expansion needed for build
    def build_sub_expr(self, expr, var, val):
        expr =  expr.replace("x"+str(var)+",", str(val)+",")
        return expr.replace("x"+str(var)+")", str(val)+")")


    # Convert input expression into a form I can evaluate
    def convert_expr(self, expr):
        # Replace all of the operators with my class operators
        expr = expr.replace("~", "not ")
        expr = expr.replace("And", "Operators.And")
        expr = expr.replace("Or", "Operators.Or")
        expr = expr.replace("Implies", "Operators.Implies")
        expr = expr.replace("Equal", "Operators.Equal")
        return expr

    # Get ROBDD table T
    def get_T(self):
        return self.T

    #Get the number of nodes in the ROBDD
    def get_num_nodes(self):
        return self.num_nodes

    # Prints the current state
    def print_robdd(self):
        print("\nCurrent state of T")
        for i in range(0, self.num_nodes):
            print("\t" + str(i) + "\t" + str(self.T[i][0]) + " "
                                + str(self.T[i][1]) + " "
                                + str(self.T[i][2]))

        print("\nCurrent state of H")
        for i in range(0,len(self.H)):
            print("\t" + str(i) + "\t" + str(self.H[i]))

        print("\n")

    def print_graph(self):
        parts = ["digraph", "robdd", "{"]
        # Create the nodes
        for node in self.T:
            # Check to see what kind of node it is
            if self.id(node) is 0:
                parts += ['n' + str(self.id(node)), '[label=0,shape=box];']
            elif self.id(node) is 1:
                parts += ['n' + str(self.id(node)), '[label=1,shape=box];']
            else:
                parts += ['n' + str(self.id(node)), '[label=x' + str(node[0]) + ',shape=circle];']
        # Create the connections
        for node in self.T:
            # Make sure it isnt a leaf node
            if self.id(node) > 1:
                parts += ["n" + str(self.id(node)), "->", "n" + str(node[1]), "[label=0,style=dashed];"]
                parts += ["n" + str(self.id(node)), "->", "n" + str(node[2]), "[label=1];"]

        # join everything
        parts.append("}")
        file_contents = " ".join(parts)

        # Write to file
        with open("robdd.dot", 'w') as f:
            f.write(file_contents)
        check_call(['dot','-Tpng','robdd.dot','-o','robdd.png'])

    # Returns the node ID
    def id(self, node):
        return self.lookup(node[0], node[1], node[2])
