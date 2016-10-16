# requires
# pip install pyyaml
import yaml
from util.tree import Tree
from util.tree import TreeNode

def buildTreesFromYamlInput(treesAsYaml):
    yamlInput = yaml.safe_load_all(treesAsYaml)
    treesParsed = []
    for t in yamlInput:
        treesParsed.append(t)    
    trees = []
    for treeParsed in treesParsed:
      trees.append(_buildTree(treeParsed))

    return trees

def _buildSubtree(rootLabel, children):
  rootNode = TreeNode(rootLabel)
  if children:
    for childDict in children:
      childLabel, childrenOfChild = childDict.iteritems().next()
      childNode = _buildSubtree(childLabel, childrenOfChild)
      rootNode.add_child(childNode)
  return rootNode

def _buildTree(treeParsed):
    rootLabel, children = treeParsed.iteritems().next()
    rootNode = _buildSubtree(rootLabel, children)
    aTree = Tree(rootNode)
    aTree.build_caches()
    aTree.print_preorder_traversal()
    return aTree

