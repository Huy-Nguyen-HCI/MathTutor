import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from DiffFunctionTree import *
from IntFunctionTree import *

from sympy.integrals.manualintegrate import manualintegrate
from sympy.abc import x

for i in range(1):
    tree = IntFunctionTree.buildTreeWithMaxComplexity( 3, True )
    tree.printTree()
    func =  tree.getOutputFunction()
    integral = func.getIntegral()
    print("The output function is: ")
    print( simplify(parse_expr(func.toString())))
    print("The value of the output function for x = 5 is: ")
    print(Function.evaluate( func.toString(), 5))
    print("Which is approximately: " )
    print(N(Function.evaluate( func.toString(), 5)))
    print("The integral is: ")
    print( simplify(parse_expr(integral.toString())) )
    print("The value of the integral for x = 5 is: ")
    print(Function.evaluate( integral.toString(), 5))
    print("checking")
    wolfram = "(int (" + simplify(parse_expr(func.toString())) + ")) - (" + integral.toString() + ")"
    print( wolfram.replace(' ', ''))


# u = parse_expr("2 * (x + 5**(x-3))")
# for arg in preorder_traversal(u):
#     print( str(arg.func) == "<class 'sympy.core.add.Add'>")
#     print("arg is: ", arg, " and func is: ", str(arg.func))