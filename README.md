# T-diff

This repository contains the implementation of an algorithm computing the distance between two trees. The algorithm was published in an aricle titled "The Tree-to-Tree Correction Problem" by Kuo-Chung Tai at the Journal of the ACM, 26(3):422-433, in July 1979.

The time complexity of the algorithm is O(V * V' * L^2 * L'^2) where V, V' are the number of nodes and L, L' are the the maximum depths of the source and target trees respectively.

During the implementation, we came across some minor issues in the reported algorithm. The implementation contains the fixes for these issues.

At the moment, the trees are assumed to be instances of Tree class in the tree module contained in the implementation. An example run is below
```python
from tree import *
from treediff import *

# Source Tree
a = TreeNode('A')
b = TreeNode('B')
a.addChild(b)
d = TreeNode('D')
b.addChild(d)
self.treeOne = Tree(a)
self.treeOne.buildCaches()

# Target Tree
a = TreeNode('A')
b = TreeNode('B')
c = TreeNode('C')
d = TreeNode('D')
a.addChild(b)
a.addChild(c)
c.addChild(d)
self.treeTwo = Tree(a)
self.treeTwo.buildCaches()
    
print computeMinDiff(self.treeOne, self.treeTwo)  # Prints 2
```

We are working on the computation of the mapping between the source and the target describing how a sequence of edit operations transforms the source tree to the target, ignoring the order in which edit operations are applied.
