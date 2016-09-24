# File containings unit tests for testing min cost tree diff computation.
# Run the test by executing "python test_treediff.py -v" at the command
# line.
import unittest
from tree import *
from treediff import *

class TestTreeDiff(unittest.TestCase):

  def setUp(self):
    a = TreeNode('A')
    b = TreeNode('B')
    a.addChild(b)
    d = TreeNode('D')
    b.addChild(d)
    self.treeOne = Tree(a)
    self.treeOne.buildCaches()

    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('C')
    d = TreeNode('D')
    a.addChild(b)
    a.addChild(c)
    c.addChild(d)
    self.treeTwo = Tree(a)
    self.treeTwo.buildCaches()
    
    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('C')
    d = TreeNode('D')
    e = TreeNode('E')
    a.addChild(b)
    a.addChild(c)
    c.addChild(d)
    d.addChild(e)
    self.treeThree = Tree(a)
    self.treeThree.buildCaches()
    
    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('CC')
    d = TreeNode('D')
    e = TreeNode('E')
    a.addChild(b)
    a.addChild(c)
    c.addChild(d)
    d.addChild(e)
    self.treeFour = Tree(a)
    self.treeFour.buildCaches()

  def test_distance(self):
    self.assertEqual(2, computeMinDiff(self.treeOne, self.treeTwo))
    self.assertEqual(3, computeMinDiff(self.treeOne, self.treeThree))
    self.assertEqual(1, computeMinDiff(self.treeTwo, self.treeThree))
    self.assertEqual(1, computeMinDiff(self.treeThree, self.treeFour))
    self.assertEqual(0, computeMinDiff(self.treeTwo, self.treeTwo))

if __name__ == '__main__':
    unittest.main()