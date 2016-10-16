""" File contains unit tests for testing Tree and TreeNode classes.

Run the test by executing "python test_tree.py -v" or "nosetests" at the
command line.
"""

import unittest
from tree import Tree
from tree import TreeNode

# Pylint does not ignore the methods in the parent class when considering the
# number of max 20 methods in a class. We suppress this check for test classes
# below.
# pylint: disable=too-many-public-methods


class Visitor(object):  # pylint: disable=too-few-public-methods
    """Builds an array of node labels it visits"""
    def __init__(self):
        self.traversal = []

    def visit(self, node):
        """Records the label of the node visited"""
        self.traversal.append(node.debug_string())


class TestTree(unittest.TestCase):
    """Tests the functionality of Tree """

    def setUp(self):
        a_node = TreeNode('A')
        b_node = TreeNode('B')
        a_node.add_child(b_node)
        c_node = TreeNode('C')
        b_node.add_child(c_node)
        self.tree_one = Tree(a_node)
        self.tree_one.build_caches()

        a_node = TreeNode('A')
        b_node = TreeNode('B')
        c_node = TreeNode('C')
        d_node = TreeNode('D')
        a_node.add_child(b_node)
        a_node.add_child(c_node)
        c_node.add_child(d_node)
        self.tree_two = Tree(a_node)
        self.tree_two.build_caches()

        a_node = TreeNode('A')
        b_node = TreeNode('B')
        c_node = TreeNode('C')
        d_node = TreeNode('D')
        e_node = TreeNode('E')
        a_node.add_child(b_node)
        a_node.add_child(c_node)
        c_node.add_child(d_node)
        d_node.add_child(e_node)
        self.tree_three = Tree(a_node)
        self.tree_three.build_caches()


class TestPreorderTraversal(TestTree):
    """Tests perform_preorder_traversal method of Tree class"""

    def test_success(self):
        """Successfully produce the list of visited node labels"""
        visitor = Visitor()
        self.tree_one.perform_preorder_traversal(visitor)
        expected = [
            "label: A, preorder_position: 1",
            "label: B, preorder_position: 2",
            "label: C, preorder_position: 3"]
        self.assertEqual(expected, visitor.traversal)

        visitor = Visitor()
        self.tree_two.perform_preorder_traversal(visitor)
        expected = [
            "label: A, preorder_position: 1",
            "label: B, preorder_position: 2",
            "label: C, preorder_position: 3",
            "label: D, preorder_position: 4"]
        self.assertEqual(expected, visitor.traversal)


class TestNodeAt(TestTree):
    """Tests node_at method of Tree class"""

    def test_node_at(self):
        """Testing getting a node from the tree by its preorder position"""
        # Tree 1
        self.assertEqual('A', self.tree_one.node_at(1).label())
        self.assertEqual('B', self.tree_one.node_at(2).label())
        self.assertEqual('C', self.tree_one.node_at(3).label())
        self.assertIsNone(self.tree_one.node_at(4))

        # Tree 2
        self.assertEqual('A', self.tree_two.node_at(1).label())
        self.assertEqual('B', self.tree_two.node_at(2).label())
        self.assertEqual('C', self.tree_two.node_at(3).label())
        self.assertEqual('D', self.tree_two.node_at(4).label())
        self.assertIsNone(self.tree_two.node_at(5))


class TestFatherOf(TestTree):
    """Tests father_of method of Tree class"""

    def test_success(self):
        """Usual case when father exists"""
        self.assertEqual(3, self.tree_two.father_of(4).preorder_position())
        self.assertEqual(1, self.tree_two.father_of(3).preorder_position())
        self.assertEqual(1, self.tree_two.father_of(2).preorder_position())

    def test_root(self):
        """Father of root should be None"""
        self.assertIsNone(self.tree_two.father_of(1))

    def test_when_no_such_node(self):
        """Raise error when father of a non-existing node requested"""
        with self.assertRaises(ValueError):
            self.tree_two.father_of(5)


class TestAncestorIterator(TestTree):
    """Tests ancestor_iterator method of Tree class"""

    def test_success(self):
        """Iterate from intermediate or leaf nodes upwards"""
        ancestor_preorder_positions = []
        for i in self.tree_two.ancestor_iterator(4):
            ancestor_preorder_positions.append(i)
        self.assertEquals([4, 3, 1], ancestor_preorder_positions)

        ancestor_preorder_positions = []
        for i in self.tree_two.ancestor_iterator(2):
            ancestor_preorder_positions.append(i)
        self.assertEquals([2, 1], ancestor_preorder_positions)

    def test_from_the_root(self):
        """Iterating from the root upwards"""
        ancestor_preorder_positions = []
        for i in self.tree_two.ancestor_iterator(1):
            ancestor_preorder_positions.append(i)
        self.assertEquals([1], ancestor_preorder_positions)

    def test_from_non_existing_position(self):
        """Trying to iterate from non-existing node is erroneous"""
        with self.assertRaises(ValueError):
            for dummy_i in self.tree_two.ancestor_iterator(100):
                self.fail("Should not yield even once")


class TestChildOnPathFromDescendant(TestTree):
    """Tests child_on_path_from_descendant method of Tree class"""

    def test_success(self):
        """When there is a node between ancestor and descendant"""
        node = self.tree_two.child_on_path_from_descendant(1, 4)
        self.assertEquals('C', node.label())
        self.assertEquals(3, node.preorder_position())

        node = self.tree_three.child_on_path_from_descendant(1, 5)
        self.assertEquals('C', node.label())
        self.assertEquals(3, node.preorder_position())

        node = self.tree_three.child_on_path_from_descendant(3, 5)
        self.assertEquals('D', node.label())
        self.assertEquals(4, node.preorder_position())

    def test_when_no_such_node(self):
        """No node between ancestor and descendant"""
        with self.assertRaises(ValueError):
            self.tree_two.child_on_path_from_descendant(1, 1)

if __name__ == '__main__':
    unittest.main()
