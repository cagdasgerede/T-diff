from treediff import ALPHA

DEBUG = False

def generateDot(sourceTree, targetTree, diffMapping):
    sourceTreeRootLabel = sourceTree.node_at(1).label()
    targetTreeRootLabel = targetTree.node_at(1).label()
    sourceTreeLabelPrefix = 'Source'
    targetTreeLabelPrefix = 'Target'
    
    dotGenerator = _DotGenerator(
        sourceTreeLabelPrefix, sourceTreeRootLabel,
        targetTreeLabelPrefix, targetTreeRootLabel)
    sourceTree.perform_preorder_traversal(dotGenerator)
    dotGenerator.switchToTargetTree()
    targetTree.perform_preorder_traversal(dotGenerator)

    # Fake a change operation
    #dotGenerator.addDottedLine('Source', "Z1", 'Target', "Z1")
    #dotGenerator.addDottedLine('Source', "D4", 'Target', "A10")
    # Fake a delete operation
    #dotGenerator.addDeletion('Source' + "C3");
    # Fake an insert operation
    #dotGenerator.addInsertion('Target' + "A10")
    
    _decorateEditOperationsForDot(
        dotGenerator,
        sourceTree, sourceTreeLabelPrefix,
        targetTree, targetTreeLabelPrefix,
        diffMapping)
    
    dot = dotGenerator.finalDotRepresentation()
    if DEBUG:
        print dot
    return dot

def _decorateEditOperationsForDot(
    dotGenerator,
    sourceTree, sourceTreeLabelPrefix,
    targetTree, targetTreeLabelPrefix,
    mapping):
    for s, t in mapping:
        sourceNode = None
        targetNode = None
        if s != ALPHA:
            sourceNode = sourceTree.node_at(s)
        if t != ALPHA:
            targetNode = targetTree.node_at(t)
    
        if s == ALPHA:
            dotGenerator.addInsertion(
                targetTreeLabelPrefix + targetNode.label())
        elif t == ALPHA:
            dotGenerator.addDeletion(
                sourceTreeLabelPrefix + sourceNode.label())
        else:
           dotGenerator.addDottedLine(
            sourceTreeLabelPrefix, sourceNode.label(),
            targetTreeLabelPrefix, targetNode.label())    

class _DotGenerator:
  def __init__(self,
               sourceTreeLabelPrefix,
               sourceTreeRootNodeLabel,
               targetTreeLabelPrefix,
               targetTreeRootNodeLabel):
    self.dotRepresentation = ['digraph G {']
    self.sourceTreeLabelPrefix = sourceTreeLabelPrefix
    self.sourceTreeRootNodeLabel = sourceTreeRootNodeLabel

    self.targetTreeLabelPrefix = targetTreeLabelPrefix
    self.targetTreeRootNodeLabel = targetTreeRootNodeLabel

    # Used to prepend the node labels in both trees so
    # that we can distinguish the node labels between 2 trees
    self.currentTreeLabelPrefix = self.sourceTreeLabelPrefix
    
    # Root nodes of both trees should be in the same level
    # in the drawing
    self.dotRepresentation.append(
        'subgraph { rank = same; %s; %s }' % (
                self.sourceTreeLabelPrefix + self.sourceTreeRootNodeLabel,
                self.targetTreeLabelPrefix + self.targetTreeRootNodeLabel))

  def visit(self, node):
    fatherNode = node.father()
    if fatherNode:
        self.dotRepresentation.append('{}{} -> {}{}'.format(
            self.currentTreeLabelPrefix, fatherNode.label(),
            self.currentTreeLabelPrefix, node.label()))
            
  def switchToTargetTree(self):
    self.currentTreeLabelPrefix = self.targetTreeLabelPrefix

  def finalDotRepresentation(self):
    self.dotRepresentation.append('}')
    return '\n'.join(self.dotRepresentation)
    
  def addDottedLine(self,
                    sourceTreeLabelPrefix, sourceLabel,
                    targetTreeLabelPrefix, targetLabel):
    """Add a dotted line representing a change
    
    Parameters:
    source - name of the source node
    target - name of the target node
    """
    color = "green"
    if sourceLabel != targetLabel:
        color = "gray"
    self.dotRepresentation.append(
            '{} -> {} [style=dotted color="{}" constraint=false]'.
            format(sourceTreeLabelPrefix + sourceLabel, 
                   targetTreeLabelPrefix + targetLabel,
                   color))

  def addDeletion(self, nodeLabel):
    self.dotRepresentation.append(
        '{} [color="red"]'.format(nodeLabel))
    
  def addInsertion(self, nodeLabel):
    self.dotRepresentation.append(
        '{} [color="orange"]'.format(nodeLabel))