# requires
# pip install pyyaml
#
# Graphviz
# sudo apt-get install graphviz

#from lib.tree import *
from treediff import computeDiff
from yaml2tree import buildTreesFromYamlInput
from diffRunner import treesToDiff
    
def buildTestTrees():    
    twoTreesAsYaml = """
---
Z1:
  - B2:  
  - C3:
    - D4:
        - F5:
    - E6:
        - G7:
        - H8:
        - J9:
    - A10:
  - A11:
---
Z1:
  - B2:  
  - C3:
    - D4:
        - F5:
    - E6:
        - G7:
        - H8:
        - J9:
    - A10:
  - A11:
"""
    return buildTreesFromYamlInput(treesAsYaml)



def runtest():
    trees = buildTestTrees()
    sourceTree = trees[0]
    targetTree = trees[1]
    dotRepresentation = generateDot(sourceTree, targetTree, None)
    producePng(dotRepresentation)
    
def runtest2():
    trees = buildTestTrees2()
    sourceTree = trees[0]
    targetTree = trees[1]
    treesToDiff(sourceTree, targetTree, outputDotGraph=True)
    
def deneme():

    # Source Tree
    a = TreeNode('A')
    b = TreeNode('B')
    a.addChild(b)
    d = TreeNode('D')
    b.addChild(d)
    z = TreeNode('Z')
    d.addChild(z)
    t = TreeNode('t')
    z.addChild(t)
    treeOne = Tree(a)
    treeOne.buildCaches()

    # Target Tree
    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('C')
    d = TreeNode('D')
    a.addChild(b)
    a.addChild(c)
    c.addChild(d)
    treeTwo = Tree(a)
    treeTwo.buildCaches()
    
    treesToDiff(treeOne, treeTwo, outputDotGraph=True)
    

def buildTestTrees2():    
    twoTreesAsYaml = """
---
A:
  - B:  
    - D:
        - Z:
            - KKK:
---
A:
  - B:  
  - C:
    - D:
"""
    return buildTreesFromYamlInput(twoTreesAsYaml)
    
#runtest()
#deneme()
runtest2()

