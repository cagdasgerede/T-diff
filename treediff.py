#from treediff import *


class TreeNode:	
	# Label of the current node
	_label = None
	
	# List of TreeNode instances
	_children = None

	# The father node of the current node
	_father = None
	
	# The cached position of the current node in the preorder
	# traversal of the tree.
	_preOrderPosition = None
	
	# Initializer
	#
	# @parameter label the label of the node (String)
	def __init__(this, label):
		this._label = label
		this._children = []
	
	# Sets the label of this node
	#
	# @parameter label the new label (String)
	def setLabel(this, label):
		this.l_abel = label
		
	# Returns the label of this node
	#
	# @return the label of the node (String)
	def label(this):
		return this._label
	
	# Sets the father of the node
	#
	# @parameter the node to become the father of this node
	def setFather(this, node):
		this._father = node
	
	# Returns the father node of the node (TreeNode)
	def father(this):
		return this._father
		
	# Adds a new child to the node.
	#
	# @parameter node the node to be added as a new child
	def addChild(this, node):
		print 'inside addChild ' + this._label
		print 'adding ndoe ' + node._label
		this._children.append(node)
		node.setFather(this)
		
	# Yields an iteration over the children (TreeNode)
	def children(this):
		for child in this._children:
			yield child
	
	# Sets the preorder traversal position
	#
	# @parameter i the new position of the node
	def setPreOrderPosition(this, i):
		this._preOrderPosition = i
	
	# Returns the position of the node in the preorder traversal
	def preOrderPosition(this):
		return this._preOrderPosition
		
	# Does a preorder traversal of the subtree rooted at this node
	def preOrderTraversal(this, visitor):
		visitor.visit(this)
		for child in this._children:
			child.preOrderTraversal(visitor)
			
	# Provides a string representation for this node for debugging
	# purposes
	def debugString(this):
		return ('label: %s, preOrderPosition: %d' %
			     (this._label, this._preOrderPosition))


class Tree:
	_root = None

	def __init__(this, root):
		this._root = root

	def setRoot(this, root):
		this._root = root

	# Does a preorder traversal and updates the node preorder
	# traversal caches.
	def updatePreorderTraversal(this):
		class Visitor:
			_position = 1
			
			def visit(this, node):
				node.setPreOrderPosition(this._position)
				this._position += 1
		
		visitor = Visitor()
		this._root.preOrderTraversal(visitor)
		
	# Does a preorder traversal and prints the node labels
	def printPreOrderTraversal(this, useCached=False):
		if not useCached:
			this.updatePreorderTraversal()

		class Visitor:
			def visit(this, node):
				print node.debugString()
		
		visitor = Visitor()
		this._root.preOrderTraversal(visitor)

def test():
	treeOne = None
	a = TreeNode('A')
	b = TreeNode('B')
	a.addChild(b)
	c = TreeNode('C')
	b.addChild(c)
	treeOne = Tree(a)
	treeOne.printPreOrderTraversal()

	
	a = TreeNode('A')
	b = TreeNode('B')
	c = TreeNode('C')
	d = TreeNode('D')
	a.addChild(b)
	a.addChild(c)
	c.addChild(d)
	treeTwo = Tree(a)
	treeTwo.printPreOrderTraversal()
	


treeOne = { 1:'A1', 2:'B2', 3:'C3'}
treeOneFatherRelationship = {3:2, 2:1, 1:1}

treeTwo = {1:'A1', 2:'B2', 3:'C3', 4:'D4'}
treeTwoFatherRelationship = {4:3, 3:1, 2:1, 1:1}

# Constant used for describing insertions or deletions.
ALPHA = 'alpha'

# Cost maps to be computed.
E = {}
MIN_M = {}
D = {}

# Cost function where a becomes b.
#
# @param a the label of the source node
# @param b the label of the target node
# @returns integer the cost of the transformation
def r(a, b):
	if a == b:  # No change
		return 0
	else:  # Insert, Delete, Change.
		return 1		


# Auxilary function to return the range of the preorderings numbers of
# the nodes along the path starting from the given node to the root.
#
# @param i the preordering number of the starting node
# @param tree the tree being traversed
def fatherIter(i, tree):
	yield i
	while (True):
		if i == 1:
			return
		i = tree[i]
		yield i
		
#def testFatherIteration(startingNode, tree):
#	for i in fatherIter(startingNode, tree):
#		print i

#def test():
#	startingNode = 4
#	tree = treeTwo
#	testFatherIteration(startingNode, tree)

#def father(i, tree):
#	return tree[i]	

#def computeE(tree1, tree2):
#	for i in range(1, len(tree1)):
#		for j in range(1, len(tree2)):
#			u = tree1[i] 
#			s = tree1[u]