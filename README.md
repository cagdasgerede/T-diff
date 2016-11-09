[![Build Status](https://travis-ci.org/cagdasgerede/T-diff.svg?branch=master)](https://travis-ci.org/cagdasgerede/T-diff)

# T-diff

This repository contains the implementation of an algorithm computing the distance between two trees. The algorithm was published in an aricle titled "The Tree-to-Tree Correction Problem" by Kuo-Chung Tai at the Journal of the ACM, 26(3):422-433, in July 1979.

The time complexity of the algorithm is O(V * V' * L^2 * L'^2) where V, V' are the number of nodes and L, L' are the the maximum depths of the source and target trees respectively.

During the implementation, we came across some minor issues in the reported algorithm. The implementation contains the fixes for these issues.

At the moment, the trees are assumed to be instances of Tree class in the tree module contained in the implementation. An example run is below
```python
from util.tree import *
from treediff import *

# Source Tree
a = TreeNode('A')
b = TreeNode('B')
a.add_child(b)
d = TreeNode('D')
b.add_child(d)
treeOne = Tree(a)
treeOne.build_caches()

# Target Tree
a = TreeNode('A')
b = TreeNode('B')
c = TreeNode('C')
d = TreeNode('D')
a.add_child(b)
a.add_child(c)
c.add_child(d)
treeTwo = Tree(a)
treeTwo.build_caches()

# Diff Computation
distance, mapping = computeDiff(treeOne, treeTwo) 
print distance # Prints 2
print mapping # [(1, 1), (2, 3), (3, 4), ('alpha', 2)]
print produceHumanFriendlyMapping(mapping, treeOne, treeTwo) # ['No change for A (@1 and @1)', 'Change from B (@2) to C (@3)', 'No change for D (@3 and @4)', 'Insert B (@2)']
```

The last line shows how to produce the mapping between the source and the target describing how a sequence of edit operations transforms the source tree to the target, ignoring the order in which edit operations are applied.

Project site: https://cagdasgerede.github.io/T-diff/


Dependencies:
- Graphviz (sudo apt-get install graphviz)
- pip install requirements.txt


