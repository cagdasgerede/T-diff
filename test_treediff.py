# File containings unit tests for testing min cost tree diff computation.
# Run the test by executing "python test_treediff.py -v" at the command
# line.
import unittest
from util.tree import *
from treediff import *

class TestTreeDiff(unittest.TestCase):
  def setUp(self):
    a = TreeNode('A')
    b = TreeNode('B')
    a.add_child(b)
    d = TreeNode('D')
    b.add_child(d)
    self.treeOne = Tree(a)
    self.treeOne.build_caches()

    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('C')
    d = TreeNode('D')
    a.add_child(b)
    a.add_child(c)
    c.add_child(d)
    self.treeTwo = Tree(a)
    self.treeTwo.build_caches()

    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('C')
    d = TreeNode('D')
    e = TreeNode('E')
    a.add_child(b)
    a.add_child(c)
    c.add_child(d)
    d.add_child(e)
    self.treeThree = Tree(a)
    self.treeThree.build_caches()
    
    a = TreeNode('A')
    b = TreeNode('B')
    c = TreeNode('CC')
    d = TreeNode('D')
    e = TreeNode('E')
    a.add_child(b)
    a.add_child(c)
    c.add_child(d)
    d.add_child(e)
    self.treeFour = Tree(a)
    self.treeFour.build_caches()

  def test_distance(self):
    self.assertEqual(2, computeDiff(self.treeOne, self.treeTwo)[0])
    self.assertEqual(3, computeDiff(self.treeOne, self.treeThree)[0])
    self.assertEqual(1, computeDiff(self.treeTwo, self.treeThree)[0])
    self.assertEqual(1, computeDiff(self.treeThree, self.treeFour)[0])
    self.assertEqual(0, computeDiff(self.treeTwo, self.treeTwo)[0])

  def test_mapping(self):
    _, mapping = computeDiff(self.treeOne, self.treeTwo)
    expectedMapping = [(1, 1), (2, 3), (3, 4), ('alpha', 2)]
    self.assertTrue(expectedMapping, mapping)

    _, mapping = computeDiff(self.treeOne, self.treeThree)
    expectedMapping = [(1, 1), (2, 3), (3, 4), ('alpha', 2), ('alpha', 5)]
    self.assertEqual(expectedMapping, mapping)

    _, mapping = computeDiff(self.treeTwo, self.treeThree)
    expectedMapping = [(1, 1), (2, 2), (3, 3), (4, 4), ('alpha', 5)]
    self.assertEqual(expectedMapping, mapping)

    _, mapping = computeDiff(self.treeThree, self.treeFour)
    expectedMapping = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    self.assertEqual(expectedMapping, mapping)

    _, mapping = computeDiff(self.treeTwo, self.treeTwo)
    expectedMapping = [(1, 1), (2, 2), (3, 3), (4, 4)]
    self.assertEqual(expectedMapping, mapping)

  def test_produceHumanFriendlyMapping(self):
    _, mapping = computeDiff(self.treeOne, self.treeTwo)
    description = produceHumanFriendlyMapping(
        mapping, self.treeOne, self.treeTwo)
    self.assertEqual([
        'No change for A (@1 and @1)',
        'Change from B (@2) to C (@3)',
        'No change for D (@3 and @4)', 'Insert B (@2)'],
        description)

    _, mapping = computeDiff(self.treeOne, self.treeThree)
    description = produceHumanFriendlyMapping(
        mapping, self.treeOne, self.treeThree)
    self.assertEqual([
        'No change for A (@1 and @1)',
        'Change from B (@2) to C (@3)',
        'No change for D (@3 and @4)',
       'Insert B (@2)', 'Insert E (@5)'],
        description)

    _, mapping = computeDiff(self.treeTwo, self.treeThree)
    description = produceHumanFriendlyMapping(
        mapping, self.treeTwo, self.treeThree)
    self.assertEqual([
        'No change for A (@1 and @1)', 'No change for B (@2 and @2)',
        'No change for C (@3 and @3)', 'No change for D (@4 and @4)',
        'Insert E (@5)'],
        description)

    _, mapping = computeDiff(self.treeThree, self.treeFour)
    description = produceHumanFriendlyMapping(
        mapping, self.treeThree, self.treeFour)
    self.assertEqual([
        'No change for A (@1 and @1)', 'No change for B (@2 and @2)',
        'Change from C (@3) to CC (@3)', 'No change for D (@4 and @4)',
        'No change for E (@5 and @5)'],
        description)

    _, mapping = computeDiff(self.treeTwo, self.treeTwo)
    description = produceHumanFriendlyMapping(
        mapping, self.treeTwo, self.treeTwo)
    self.assertEqual([
        'No change for A (@1 and @1)', 'No change for B (@2 and @2)',
        'No change for C (@3 and @3)', 'No change for D (@4 and @4)'],
        description)

if __name__ == '__main__':
    unittest.main()