"""Tree and TreeNode classes"""


class Visitor(object):  # pylint: disable=too-few-public-methods
    """A visitor class to apply the visitor pattern for navigating the tree"""
    def visit(self, node):
        """Override this method"""
        pass


class PreOrderMarkingVisitor(Visitor):
    # pylint: disable=too-few-public-methods
    """A visitor to be used in marking preorder positions of each tree node"""
    def __init__(self, tree):
        self._position = 1
        self._tree = tree

    def visit(self, node):
        self._tree.set_node_at(self._position, node)
        self._position += 1


class DebugVisitor(Visitor):  # pylint: disable=too-few-public-methods
    """A visitor to be used in printing each node's debug information"""
    def visit(self, node):  # pylint: disable=no-self-use
        print node.debug_string()


class TreeNode(object):
    """Single node in a tree"""

    def __init__(self, label):
        # Label of the current node
        self._label = label

        # List of TreeNode instances
        self._children = []

        # The father node of the current node
        self._father = None

        # The cached position of the current node in the preorder
        # traversal of the tree.
        self._preorder_position = None

    def set_label(self, label):
        """Sets the label (str) of this node"""
        self._label = label

    def label(self):
        """Returns the label (str) of this node"""
        return self._label

    def set_father(self, node):
        """Sets the father of the node (TreeNode)"""
        self._father = node

    def father(self):
        """Returns the father node (TreeNode) of the node"""
        return self._father

    def add_child(self, node):
        """Adds a new child (TreeNode) to the node"""
        self._children.append(node)
        node.set_father(self)

    def children(self):
        """Yields an iteration over the children (TreeNode)"""
        for child in self._children:
            yield child

    def set_preorder_position(self, new_position):
        """Sets the preorder traversal position (int)"""
        self._preorder_position = new_position

    def preorder_position(self):
        """Returns the position (int) of the node in the preorder traversal"""
        return self._preorder_position

    def preorder_traversal(self, visitor):
        """Does a preorder traversal of the subtree rooted at this node

        The parameter visitor should have a visit method accepting a TreeNode.
        """
        visitor.visit(self)
        for child in self._children:
            child.preorder_traversal(visitor)

    def debug_string(self):
        """Returns a representation (str) for this node for debugging"""
        return ('label: %s, preorder_position: %d' %
                (self._label, self._preorder_position))


class Tree(object):
    """Defines a tree structure of TreeNode elements"""
    def __init__(self, root):
        self._root = root
        self._preorder_position_to_node = {}

    def size(self):
        """Returns the number of nodes in the tree"""
        return len(self._preorder_position_to_node)

    def build_caches(self):
        """Builds the cached preorder positions of the nodes in the tree.

        Call this method after the tree structure is finalized    .
        """
        visitor = PreOrderMarkingVisitor(self)
        self.perform_preorder_traversal(visitor)

    def perform_preorder_traversal(self, visitor):
        """Performs a preorder traversal on the tree

        The visitor is used for taking an action on the visited node (
        the visitor must have a visit method)
        """
        self._root.preorder_traversal(visitor)

    def print_preorder_traversal(self):
        """Does a preorder traversal and prints the node labels"""
        visitor = DebugVisitor()
        self.perform_preorder_traversal(visitor)

    def node_at(self, preorder_position):
        """Returns the node (TreeNode) at the given preorder position"""
        return self._preorder_position_to_node.get(preorder_position)

    def set_node_at(self, preorder_position, node):
        """Marks the node to be in the given preorder position in the tree"""
        self._preorder_position_to_node[preorder_position] = node
        node.set_preorder_position(preorder_position)

    def father_of(self, preorder_position):
        """Returns the father of the node at the given preorder position"""
        node = self._preorder_position_to_node.get(preorder_position)
        if node:
            return node.father()

        raise ValueError('No node at the given position', preorder_position)

    def ancestor_iterator(self, starting_preorder_position):
        """Produces iteration towards the root starting from the given position

        Yields preorder positions of the nodes along the path from
        the node at the given position to the root
        """
        if starting_preorder_position > len(self._preorder_position_to_node):
            raise ValueError('No node at the given position',
                             starting_preorder_position)

        yield starting_preorder_position
        while True:
            node = self.father_of(starting_preorder_position)
            if node:
                starting_preorder_position = node.preorder_position()
                yield starting_preorder_position
            else:
                break

    def child_on_path_from_descendant(
            self, parent_position, descendant_position):
        """Finds a child node between the parent and the descendant.

        Returns the child of a node which is on the path from a
        descendant of the node to the node (there can only be one such child).
        Returns None if no such node.
        """
        current_child_node = self.node_at(descendant_position)
        father_node = current_child_node.father()
        if father_node is None:
            raise ValueError(
                'No father node for the given descendant position',
                descendant_position)

        while father_node.preorder_position() != parent_position:
            current_child_node = father_node
            father_node = current_child_node .father()
            if father_node is None:
                return None

        return current_child_node
