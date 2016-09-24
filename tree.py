# Single node in a tree.
class TreeNode:	
    # Initializer
    #
    # @parameter label the label of the node (String)
    def __init__(self, label):
        # Label of the current node
        self._label = label

        # List of TreeNode instances
        self._children = []

        # The father node of the current node
        self._father = None

        # The cached position of the current node in the preorder
        # traversal of the tree.
        self._preorderPosition = None
    
    # Sets the label of this node
    #
    # @parameter label the new label (String)
    def setLabel(self, label):
        self._label = label

    # Returns the label of this node
    #
    # @return String
    def label(self):
        return self._label
    
    # Sets the father of the node
    #
    # @parameter the node to become the father of this node
    def setFather(self, node):
        self._father = node
    
    # Returns the father node of the node
    #
    # @return TreeNode
    def father(self):
        return self._father
        
    # Adds a new child to the node.
    #
    # @parameter node the node to be added as a new child
    def addChild(self, node):
        self._children.append(node)
        node.setFather(self)
        
    # Yields an iteration over the children (TreeNode)
    def children(self):
        for child in self._children:
            yield child
    
    # Sets the preorder traversal position
    #
    # @parameter i the new position of the node
    def setPreorderPosition(self, i):
        self._preorderPosition = i
    
    # Returns the position of the node in the preorder traversal
    #
    # @return int
    def preorderPosition(self):
        return self._preorderPosition
        
    # Does a preorder traversal of the subtree rooted at this node
    def preorderTraversal(self, visitor):
        visitor.visit(self)
        for child in self._children:
            child.preorderTraversal(visitor)
            
    # Provides a string representation for this node for debugging
    # purposes
    def debugString(self):
        return ('label: %s, preorderPosition: %d' %
                 (self._label, self._preorderPosition))

# Defines a tree structure of TreeNode elements.
class Tree:
    def __init__(self, root):
      self._root = root
      self._mapFromPreorderPositionToNode = {}

    # Rebuilds the cached date for the tree. For example,
    # preorder positions are updated. Call this method everytime
    # the tree is modified.
    #
    # TODO(cgerede): We should have a better mechanism for
    # automatically updating the cached content as the tree
    # is updated. It would be less error prone if this detail
    # is hidden from the user.
    def buildCaches(self):
      self._buildPreorderPositionCaches()

    # Returns the number of nodes in the tree
    #
    # @return int
    def size(self):
      return len(self._mapFromPreorderPositionToNode)

    # Does a preorder traversal and updates the cached value of
    # the preorder position in the nodes.
    def _buildPreorderPositionCaches(self, visitor=None):
        class Visitor:
            def __init__(self, tree):
                self._position = 1
                self.tree = tree

            def visit(self, node):
                node.setPreorderPosition(self._position)
                self.tree._mapFromPreorderPositionToNode[
                    self._position] = node
                self._position += 1

                if visitor:
                    visitor.visit(node)

        _visitor = Visitor(self)
        self._root.preorderTraversal(_visitor)

    # Performs a preorder traversal on the tree
    #
    # @parameter visitor the visitor to be used for taking an
    #                              action on the visited node (the visitor must
    #                              have a visit method)
    def performPreorderTraversal(self, visitor):
        self._root.preorderTraversal(visitor)

    # Does a preorder traversal and prints the node labels
    def printPreorderTraversal(self):
        class Visitor:
                def visit(self, node):
                    print node.debugString()

        visitor = Visitor()
        self.performPreorderTraversal(visitor)

    # Returns the node at the given preorder position
    #
    # @return TreeNode
    def nodeAt(self, preorderPosition):
      return self._mapFromPreorderPositionToNode.get(preorderPosition)

    # Returns the father of the node at the given preorder position
    #
    # @return TreeNode
    def fatherOf(self, preorderPosition):
      node = self._mapFromPreorderPositionToNode.get(preorderPosition)
      if node:
        return node.father() 

      raise ValueError('No node at the given position', preorderPosition)

    # Yields preorder positions of the nodes along the path from
    # the node at the given position to the root
    #
    # @return int
    def ancestorIterator(self, startingPreorderPosition):
      currentPreorderPosition = startingPreorderPosition
      if currentPreorderPosition > len(self._mapFromPreorderPositionToNode):
        raise ValueError('No node at the given position',
                                  currentPreorderPosition)

      yield currentPreorderPosition 
      while True:
        node = self.fatherOf(currentPreorderPosition)
        if node:
          currentPreorderPosition = node.preorderPosition()
          yield currentPreorderPosition
        else:
          break

    # Returns the child of a node which is on the path from a
    # descendant of the node to the node (there can only be one
    # such child)
    #
    # @parameter parentPosition the position of the node that is the
    #                                          parent of the node we are looking for
    # @paremeter descendantPosition the position of the descendant
    #                                                 node where the path starts
    # @return TreeNode
    def childNodeOnPathFromDescendant(
        self, parentPosition, descendantPosition):
      currentChildNode = self.nodeAt(descendantPosition)
      fatherNode = currentChildNode.father()
      if fatherNode is None:
        raise ValueError('No father node for the given descendant position',
                                  descendantPosition)

      while fatherNode.preorderPosition() != parentPosition:
        currentChildNode = fatherNode
        fatherNode = currentChildNode .father()
        if fatherNode is None:
          return None

      return currentChildNode