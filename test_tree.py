# File containings unit tests for testing Tree and TreeNode classes.
# Run the test by executing "python test_tree.py -v" at the command
# line.
import unittest
from tree import *

# Tests the functionality of Tree and TreeNode
# classes.
class TestTree(unittest.TestCase):

  def setUp(self):
    a = TreeNode('A')
    b = TreeNode('B')
    a.addChild(b)
    c = TreeNode('C')
    b.addChild(c)
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

  def test_preorderTraversal(self):
    class Visitor:
      def __init__(self):
        self.traversal = []

      def visit(self, node):
        self.traversal.append(node.debugString())
  
    visitor = Visitor()
    self.treeOne.performPreorderTraversal(visitor)
    expected = [
        "label: A, preorderPosition: 1",
        "label: B, preorderPosition: 2",
        "label: C, preorderPosition: 3"]
    self.assertEqual(expected, visitor.traversal)

  def test_preorderTraversalSecondTree(self):
    class Visitor:
      def __init__(self):
        self.traversal = []

      def visit(self, node):
        self.traversal.append(node.debugString())
  
    visitor = Visitor()
    self.treeTwo.performPreorderTraversal(visitor)
    expected = [
        "label: A, preorderPosition: 1",
        "label: B, preorderPosition: 2",
        "label: C, preorderPosition: 3",
        "label: D, preorderPosition: 4",]
    self.assertEqual(expected, visitor.traversal)

  # Testing getting a node from the tree by its preorder position
  def test_nodeAt(self):
    # Tree 1
    self.assertEqual('A', self.treeOne.nodeAt(1).label())
    self.assertEqual('B', self.treeOne.nodeAt(2).label())
    self.assertEqual('C', self.treeOne.nodeAt(3).label())
    self.assertIsNone(self.treeOne.nodeAt(4))

    # Tree 2
    self.assertEqual('A', self.treeTwo.nodeAt(1).label())
    self.assertEqual('B', self.treeTwo.nodeAt(2).label())
    self.assertEqual('C', self.treeTwo.nodeAt(3).label())
    self.assertEqual('D', self.treeTwo.nodeAt(4).label())
    self.assertIsNone(self.treeTwo.nodeAt(5))

  def test_fatherOfRaisesErrorWhenNoSuchNode(self):
    with self.assertRaises(ValueError):
      self.treeTwo.fatherOf(5)

  def test_fatherOfWhenNodeHasFather(self):
    self.assertEqual(3, self.treeTwo.fatherOf(4).preorderPosition())
    self.assertEqual(1, self.treeTwo.fatherOf(3).preorderPosition())
    self.assertEqual(1, self.treeTwo.fatherOf(2).preorderPosition())

  def test_fatherOfRoot(self):
    self.assertIsNone(self.treeTwo.fatherOf(1))

  def test_ancestorIterator(self):
    ancestorPreorderPositions = []
    for i in self.treeTwo.ancestorIterator(4):
      ancestorPreorderPositions.append(i)
    self.assertEquals([4, 3, 1], ancestorPreorderPositions)

    ancestorPreorderPositions = []
    for i in self.treeTwo.ancestorIterator(2):
      ancestorPreorderPositions.append(i)
    self.assertEquals([2, 1], ancestorPreorderPositions)

  def test_ancestorIteratorFromTheRoot(self):
    ancestorPreorderPositions = []
    for i in self.treeTwo.ancestorIterator(1):
      ancestorPreorderPositions.append(i)
    self.assertEquals([1], ancestorPreorderPositions)
    
  def test_ancestorIteratorFromNotExistingPosition(self):
    with self.assertRaises(ValueError):
      for i in self.treeTwo.ancestorIterator(100):
        self.fail("Should not yield even once")

  def test_childNodeOnPathFromDescendant(self):
    node = self.treeTwo.childNodeOnPathFromDescendant(1, 4)
    self.assertEquals('C', node.label())
    self.assertEquals(3, node.preorderPosition())

    node = self.treeThree.childNodeOnPathFromDescendant(1, 5)
    self.assertEquals('C', node.label())
    self.assertEquals(3, node.preorderPosition())
    
    node = self.treeThree.childNodeOnPathFromDescendant(3, 5)
    self.assertEquals('D', node.label())
    self.assertEquals(4, node.preorderPosition())

  def test_childNodeOnPathFromDescendantWhenNoSuchNode(self):
    with self.assertRaises(ValueError):
      node = self.treeTwo.childNodeOnPathFromDescendant(1, 1)

if __name__ == '__main__':
    unittest.main()