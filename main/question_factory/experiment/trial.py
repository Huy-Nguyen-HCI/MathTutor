import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

from sympy.integrals.manualintegrate import manualintegrate
from sympy.abc import x

e = parse_expr("((x**7)) - (((((7*x) + ((x**1)))) + (9*x))) / 3")
print( manualintegrate(e,x) )