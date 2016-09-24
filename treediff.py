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

# Cost maps to be computed
E = {}
MIN_M = {}
D = {}

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
# the mapping mean
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns dict (in the format {'i:j:k, p:q:r' => cost} where 
#                        i, j, k, p, q, r are integers)
def computeE(sourceTree, targetTree):
  E = {}
  for i in range(1, sourceTree.size() + 1):
    for j in range(1, targetTree.size() + 1):
      for u in sourceTree.ancestorIterator(i):
        for s in sourceTree.ancestorIterator(u):
          for v in targetTree.ancestorIterator(j):
            for t in targetTree.ancestorIterator(v):
              key = keyForE(s, u, i, t, v, j)
              if (s == u and u == i) and (t == v and v == j):
                E[key] = r(sourceTree.nodeAt(i), targetTree.nodeAt(j))
              elif (s == u and u == i) or (t < v and v == j):
                f_j = targetTree.fatherOf(j).preorderPosition()
                dependentKey = keyForE(s, u, i, t, f_j, j - 1)
                E[key] = E[dependentKey] + r(ALPHA, targetTree.nodeAt(j))
              elif (s < u and u == i) or (t == v and v == j):
                f_i = sourceTree.fatherOf(i).preorderPosition()
                dependentKey = keyForE(s, f_i, i - 1, t, v, j)
                E[key] = E[dependentKey] + r(sourceTree.nodeAt(i), ALPHA)
              else:
                xNode = sourceTree.childNodeOnPathFromDescendant(u, i)
                x = xNode.preorderPosition()
                yNode = targetTree.childNodeOnPathFromDescendant(v, j)
                y = yNode.preorderPosition()
                dependentKey1 = keyForE(s, x, i, t, v, j)
                dependentKey2 = keyForE(s, u, i, t, y, j)
                dependentKey3 = keyForE(s, u, x - 1, t, v, y - 1)
                dependentKey4 = keyForE(x, x, i, y, y, j)
                E[key] = min(
                    E[dependentKey1],
                    E[dependentKey2],
                    E[dependentKey3] + E[dependentKey4])

  return E

# Returns the key for MIN_M map
def keyForMIN_M(s, t):
  return '%d:%d' % (s, t)

# Returns the MIN_M mapping. Check out the article to see
# what the mapping mean
#
# @parameter E computed by computeE (dict)
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns dict
def computeMIN_M(E, sourceTree, targetTree):
  MIN_M = {keyForMIN_M(1, 1) : 0}
  
  # This part is missing in the paper
  for j in range(2, targetTree.size()):
    MIN_M[keyForMIN_M(1, j)] = (
        MIN_M[keyForMIN_M(1, j - 1)] +
        r(ALPHA, targetTree.nodeAt(j)))

  # This part is missing in the paper
  for i in range(2, sourceTree.size()):
    MIN_M[keyForMIN_M(i, 1)] = (
        MIN_M[keyForMIN_M(i - 1, 1)] +
        r(sourceTree.nodeAt(i), ALPHA))
  
  for i in range(2, sourceTree.size() + 1):
    for j in range(2, targetTree.size() + 1):
      keyForMIN_M_i_j= keyForMIN_M(i, j)
      MIN_M[keyForMIN_M_i_j] = INFINITE
      f_i = sourceTree.fatherOf(i).preorderPosition()
      f_j = targetTree.fatherOf(j).preorderPosition()

      for s in sourceTree.ancestorIterator(f_i):
        for t in targetTree.ancestorIterator(f_j):
          dependentKeyForE = keyForE(s, f_i, i - 1, t, f_j, j - 1)
          dependentKeyForM = keyForMIN_M(s, t)
          temp = (MIN_M[dependentKeyForM] +
                       E[dependentKeyForE] -
                       r(sourceTree.nodeAt(s), targetTree.nodeAt(t)))
          MIN_M[keyForMIN_M_i_j] = min(temp, MIN_M[keyForMIN_M_i_j])
          
      MIN_M[keyForMIN_M_i_j]  = (
          MIN_M[keyForMIN_M_i_j]  +
          r(sourceTree.nodeAt(i), targetTree.nodeAt(j)))

  return MIN_M

# Returns the key for D map
def keyForD(i, j):
  return '%d, %d' % (i, j)

# Returns the D mapping. Check out the article to see
# what the mapping mean
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @parameter MIN_M the MIN_M map (dict)
# @returns dict
def computeD(sourceTree, targetTree, MIN_M):
  D = {keyForD(1, 1) : 0}
  for i in range(2, sourceTree.size() + 1):
    D[keyForD(i, 1)] = D[keyForD(i - 1, 1)] + r(sourceTree.nodeAt(i), ALPHA)
  for j in range(2, targetTree.size() + 1):
    D[keyForD(1, j)] = D[keyForD(1, j - 1)] + r(ALPHA, targetTree.nodeAt(j))
  for i in range(2, sourceTree.size() + 1):
    for j in range(2, targetTree.size() + 1):
      D[keyForD(i, j)] = min(
        D[keyForD(i, j - 1)] + r(ALPHA, targetTree.nodeAt(j)),
        D[keyForD(i - 1, j)] + r(sourceTree.nodeAt(i), ALPHA),
        MIN_M[keyForMIN_M(i, j)])
  return D

# Returns the distance between the given trees
#
# @parameter sourceTree the source tree (Tree)
# @parameter targetTree the target tree (Tree)
# @returns int
def computeMinDiff(sourceTree, targetTree):
  E = computeE(sourceTree, targetTree)
  MIN_M = computeMIN_M(E, sourceTree, targetTree)
  D = computeD(sourceTree, targetTree, MIN_M)
  return D[keyForD(sourceTree.size(), targetTree.size())]