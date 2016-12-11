# This file has the implementation of the algorithm described in
# "The Tree-to-Tree Correction Problem" by Kuo-Chung Tai published
# at the Journal of the ACM , 26(3):422-433, July 1979.
#
# We follow the naming of the variables and functions from the paper
# even though sometimes it may be against some Python conventions.
# The algorithm is at section 5 in the paper. There is one
# missing piece in the algorithm provided in the paper which is
# MIN_M(i, 1) and MIN_M(1, j) values. We added the computation
# of these in the implementation below.

INFINITE = float("inf")

# Constant used for describing insertions or deletions
ALPHA = 'alpha'

# Returns the cost of transforming a to b
#
# @parameter a the label of the source node
# @parameter b the label of the target node
# @returns integer
def r(a, b):
  if (a != ALPHA and
      b != ALPHA  and
      a.label() == b.label()): # No change
    return 0
  else:  # Insert, Delete, Change.
    return 1

def keyForE(s, u, i, t, v, j):
  return '%d:%d:%d, %d:%d:%d' % (s, u, i, t, v, j)

# Returns the E mapping. Check the paper to understand what
# the mapping mean.
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns (dict, dict)
#        The first dict is in the format {'i:j:k, p:q:r' => cost} where 
#        i, j, k, p, q, r are integers. The second dict is in the format
#        {'i:j:k, p:q:r' => mapping} where mapping is a list of
#         (x, y) pairs showing which node at the preorder position x
#         in the source tree is mapped to which node at the preorder
#         position y in the target tree. If x is ALPHA, then it shows
#         the node at the preorder position y in the target tree is
#         inserted. If y is ALPHA, then it shows the node at the preorder
#         position x in the souce tree is deleted.
def computeE(sourceTree, targetTree):
  E = {}
  mappingForE = {}
  for i in range(1, sourceTree.size() + 1):
    for j in range(1, targetTree.size() + 1):
      for u in sourceTree.ancestor_iterator(i):
        for s in sourceTree.ancestor_iterator(u):
          for v in targetTree.ancestor_iterator(j):
            for t in targetTree.ancestor_iterator(v):
              key = keyForE(s, u, i, t, v, j)
              if (s == u and u == i) and (t == v and v == j):
                E[key] = r(sourceTree.node_at(i), targetTree.node_at(j))
                mappingForE[key] = [(i,j)]
              elif (s == u and u == i) or (t < v and v == j):
                f_j = targetTree.father_of(j).preorder_position()
                dependentKey = keyForE(s, u, i, t, f_j, j - 1)
                E[key] = E[dependentKey] + r(ALPHA, targetTree.node_at(j))
                mappingForE[key] = mappingForE[dependentKey] + [(ALPHA, j)]
              elif (s < u and u == i) or (t == v and v == j):
                f_i = sourceTree.father_of(i).preorder_position()
                dependentKey = keyForE(s, f_i, i - 1, t, v, j)
                E[key] = E[dependentKey] + r(sourceTree.node_at(i), ALPHA)
                mappingForE[key] = mappingForE[dependentKey] + [(i, ALPHA)]
              else:
                xNode = sourceTree.child_on_path_from_descendant(u, i)
                x = xNode.preorder_position()
                yNode = targetTree.child_on_path_from_descendant(v, j)
                y = yNode.preorder_position()
                dependentKey1 = keyForE(s, x, i, t, v, j)
                dependentKey2 = keyForE(s, u, i, t, y, j)
                dependentKey3 = keyForE(s, u, x - 1, t, v, y - 1)
                dependentKey4 = keyForE(x, x, i, y, y, j)
                E[key] = min(
                    E[dependentKey1],
                    E[dependentKey2],
                    E[dependentKey3] + E[dependentKey4])
                # Remember the mapping.
                if E[key] == E[dependentKey1]:
                  mappingForE[key] = mappingForE[dependentKey1]
                elif E[key] == E[dependentKey2]:
                  mappingForE[key] = mappingForE[dependentKey2]
                else:
                  mappingForE[key] = (
                      mappingForE[dependentKey3] + 
                      mappingForE[dependentKey4])

  return E, mappingForE

# Returns the key for MIN_M map
def keyForMIN_M(s, t):
  return '%d:%d' % (s, t)

# Returns the MIN_M mapping. Check out the article to see
# what the mapping mean
#
# @parameter E computed by computeE (dict)
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns (dict, dict)
#        The first dict is the MIN_M map (key to cost). The second
#        dict is (key to list of integer pairs) the transformation mapping
#        where a pair (x, y) shows which node at the preorder position x
#         in the source tree is mapped to which node at the preorder
#         position y in the target tree. If x is ALPHA, then it shows
#         the node at the preorder position y in the target tree is
#         inserted. If y is ALPHA, then it shows the node at the preorder
#         position x in the souce tree is deleted.
def computeMIN_M(E, mappingForE, sourceTree, targetTree):
  MIN_M = {keyForMIN_M(1, 1) : 0}
  mappingForMinM = {keyForMIN_M(1, 1) : [(1, 1)]}
  
  # This part is missing in the paper
  for j in range(2, targetTree.size()):
    MIN_M[keyForMIN_M(1, j)] = (
        MIN_M[keyForMIN_M(1, j - 1)] +
        r(ALPHA, targetTree.node_at(j)))
    mappingForMinM[keyForMIN_M(1, j)] = (
        mappingForMinM[keyForMIN_M(1, j - 1)] + [(ALPHA, j)])

  # This part is missing in the paper
  for i in range(2, sourceTree.size()):
    MIN_M[keyForMIN_M(i, 1)] = (
        MIN_M[keyForMIN_M(i - 1, 1)] +
        r(sourceTree.node_at(i), ALPHA))
    mappingForMinM[keyForMIN_M(i, 1)] = (
        mappingForMinM[keyForMIN_M(i - 1, 1)] + [(i, ALPHA)])
  
  for i in range(2, sourceTree.size() + 1):
    for j in range(2, targetTree.size() + 1):
      keyForMIN_M_i_j= keyForMIN_M(i, j)
      MIN_M[keyForMIN_M_i_j] = INFINITE
      f_i = sourceTree.father_of(i).preorder_position()
      f_j = targetTree.father_of(j).preorder_position()

      for s in sourceTree.ancestor_iterator(f_i):
        for t in targetTree.ancestor_iterator(f_j):
          dependentKeyForE = keyForE(s, f_i, i - 1, t, f_j, j - 1)
          dependentKeyForM = keyForMIN_M(s, t)
          temp = (MIN_M[dependentKeyForM] +
                       E[dependentKeyForE] -
                       r(sourceTree.node_at(s), targetTree.node_at(t)))
          MIN_M[keyForMIN_M_i_j] = min(temp, MIN_M[keyForMIN_M_i_j])
          if temp == MIN_M[keyForMIN_M_i_j]:
            mappingForMinM[keyForMIN_M_i_j] = list(set(
                mappingForMinM[dependentKeyForM] +
                mappingForE[dependentKeyForE]))
          
      MIN_M[keyForMIN_M_i_j]  = (
          MIN_M[keyForMIN_M_i_j]  +
          r(sourceTree.node_at(i), targetTree.node_at(j)))
      mappingForMinM[keyForMIN_M_i_j].append((i, j))

  return MIN_M, mappingForMinM

# Returns the key for D map
def keyForD(i, j):
  return '%d, %d' % (i, j)

# Returns the D mapping. Check out the article to see
# what the mapping mean
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @parameter MIN_M the MIN_M map (dict)
# @parameter mappingForM the transformation details for MIN_M
# @returns (dict, dict)
#        The first dict is the D mapping (key to cost).
#        The second dict is (key to list of integer pairs) the transformation mapping
#        where a pair (x, y) shows which node at the preorder position x
#         in the source tree is mapped to which node at the preorder
#         position y in the target tree. If x is ALPHA, then it shows
#         the node at the preorder position y in the target tree is
#         inserted. If y is ALPHA, then it shows the node at the preorder
#         position x in the souce tree is deleted.
def computeD(sourceTree, targetTree, MIN_M, mappingForMinM):
  D = {keyForD(1, 1) : 0}
  mappingForD = {keyForD(1, 1) : [(1, 1)]}

  for i in range(2, sourceTree.size() + 1):
    D[keyForD(i, 1)] = D[keyForD(i - 1, 1)] + r(sourceTree.node_at(i), ALPHA)
    mappingForD[keyForD(i, 1)] = (
        mappingForD[keyForD(i - 1, 1)] + [(i, ALPHA)])

  for j in range(2, targetTree.size() + 1):
    D[keyForD(1, j)] = D[keyForD(1, j - 1)] + r(ALPHA, targetTree.node_at(j))
    mappingForD[keyForD(1, j)] = (
        mappingForD[keyForD(1, j - 1)] + [(ALPHA, j)])

  for i in range(2, sourceTree.size() + 1):
    for j in range(2, targetTree.size() + 1):
      option1 = D[keyForD(i, j - 1)] + r(ALPHA, targetTree.node_at(j))
      option2 = D[keyForD(i - 1, j)] + r(sourceTree.node_at(i), ALPHA),
      option3 = MIN_M[keyForMIN_M(i, j)]
      D[keyForD(i, j)] = min(option1, option2, option3)

      if D[keyForD(i, j)] == option1:
        mappingForD[keyForD(i,  j)] = (
            mappingForD[keyForD(i, j - 1)] + [(ALPHA, j)])
      elif D[keyForD(i, j)] == option2:
        mappingForD[keyForD(i,  j)] = (
            mappingForD[keyForD(i - 1, j)] + [(i, ALPHA)])
      else:
        mappingForD[keyForD(i,  j)] = mappingForMinM[keyForMIN_M(i, j)]
  return D, mappingForD

# Produces a list of humand friendly descriptions for mapping
# between two trees
# Example:
#   ['No change for A (@1)', 'Change from B (@2) to C (@3)',
#    'No change for D (@3)', 'Insert B (@2)']
#
# @returns list of strings
def produceHumanFriendlyMapping(mapping, sourceTree, targetTree):
  humandFriendlyMapping = []
  for i, j in mapping:
    if i == ALPHA:
      targetNode = targetTree.node_at(j)
      humandFriendlyMapping.append(
          'Insert %s (@%d)' % (
              targetNode.label(), targetNode.preorder_position()))
    elif j == ALPHA:
      sourceNode = sourceTree.node_at(i)
      humandFriendlyMapping.append(
          'Delete %s (@%d)' % (
              sourceNode.label(), sourceNode.preorder_position()))
    else:
      sourceNode = sourceTree.node_at(i)
      targetNode = targetTree.node_at(j)
      if sourceNode.label() == targetNode.label():
        humandFriendlyMapping.append(
            'No change for %s (@%d and @%d)' % (
                sourceNode.label(), sourceNode.preorder_position(),
                targetNode.preorder_position()))
      else:
        humandFriendlyMapping.append(
            'Change from %s (@%d) to %s (@%d)' % (
                sourceNode.label(), sourceNode.preorder_position(),
                targetNode.label(), targetNode.preorder_position()))
  return humandFriendlyMapping

# Returns the distance between the given trees and the list of pairs
# where each pair (x, y) shows which node at the preorder position x
# in the source tree is mapped to which node at the preorder
# position y in the target tree. If x is ALPHA, then it shows
# the node at the preorder position y in the target tree is
# inserted. If y is ALPHA, then it shows the node at the preorder
# position x in the souce tree is deleted.
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns (int, [(int, int)])
def computeDiff(sourceTree, targetTree):
  E, mappingForE = computeE(sourceTree, targetTree)
  MIN_M, mappingForMinM = computeMIN_M(
      E, mappingForE, sourceTree, targetTree)
  D, mappingForD = computeD(
      sourceTree, targetTree, MIN_M, mappingForMinM)
  mapping = mappingForD[keyForD(sourceTree.size(), targetTree.size())]
  mapping.sort()
  return (D[keyForD(sourceTree.size(), targetTree.size())], mapping)
