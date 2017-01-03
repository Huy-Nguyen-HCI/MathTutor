import sys

from ProductionRules import *
from DiffProductionRules import *
from IntProductionRules import *
from FunctionTree import *
from DiffFunctionTree import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x
from sympy.integrals.manualintegrate import manualintegrate


class IntFunctionTree(FunctionTree):

    def applyProduction( self, production, complexity ):
        leaf = self.getRandomLeaf()

        # if this leaf's value has already been set, do nothing
        if leaf.getValue() is not None:
            return

        parent = leaf.getParent()

        # replace leaf with a combo of Inner Node, Left Child, Right Child
        newNode = Node( production, complexity )
        # create new leaf
        newLeaf = Node()
        newNode.setLeftChild( leaf )
        newNode.setRightChild( newLeaf )
        self.replaceNode( leaf, newNode, parent )

        # if rule "timesConst", its left child must be a const
        if production == timesConst:
            leaf.setValue( const() )

        # if rule "timesCompose"
        # right child must be an output of diff production rules
        elif production == timesCompose:
            diffTree = DiffFunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
            func = diffTree.getOutputFunction()
            newLeaf.setValue( func )

        # if rule "partialInt"
        elif production == partialInt:
            self.constructFunctionsForPartialInt( leaf, newLeaf )


    def constructFunctionsForPartialInt( self, leftChild, rightChild ):
        while (True):
            # construct h(x) where int h(x) is known
            productTree = IntFunctionTree.buildTreeWithMaxComplexity( 3, False )
            h = productTree.getOutputFunction()

            # construct v where diff v is known
            rightTree = DiffFunctionTree.buildTreeWithMaxComplexity( 3 )
            v = rightTree.getOutputFunction()
            vDerivative = v.getDerivative()
            assert vDerivative is not None

            # construct u = int ( h / v )
            uDerivative = divide( h, v )
            u = manualintegrate( parse_expr( uDerivative.toString() ), x )
            print("generated u: ", u)

            if not Function.isIntegrable( u ) or not Function.meetsComplexityBound( u, 40 ):
                continue

            # save the constructed functions to the corresponding nodes
            leftFunction = Function( str(u) )
            leftFunction.setDerivative( uDerivative )
            leftChild.setValue( leftFunction )
            rightChild.setValue( v )
            break


    # Evaluate the subtree rooted at node to get the output function
    def getFunctionAtSubtree( self, node ):
        if node.isLeaf():
            return node.getValue()
        else:
            production = node.getValue()
            leftFunction = self.getFunctionAtSubtree( node.getLeftChild() )
            rightFunction = self.getFunctionAtSubtree( node.getRightChild() )
            result = production( leftFunction, rightFunction )

            # get the integral
            integral = IntProductionRules.getIntegral( production.__name__, leftFunction, rightFunction )
            result.setIntegral( integral )
            return result


    # Build a function tree with the input complexity bound
    @classmethod
    def buildTreeWithMaxComplexity( cls, complexity, usePartialInt ):
        iteration = 0
        tree = IntFunctionTree( complexity )

        while tree.getComplexity() < complexity and iteration < 20:
            productionRule = IntProductionRules.getRandomProductionRule()
            if ( not usePartialInt and productionRule == partialInt ):
                continue
            productionComp = IntProductionRules.complexityMap[productionRule]
            tree.applyProduction( productionRule, productionComp )
            iteration +=1

        tree.assignFunctionsToLeaves()
        return tree
