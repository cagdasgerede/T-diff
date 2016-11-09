from treediff import *
from diff2Dot import generateDot

DEBUG = False

def treesToDiff(sourceTree, targetTree, outputDotGraph=False):
    distance, mapping = computeDiff(sourceTree, targetTree) 
    humanFriendlyDescription = produceHumanFriendlyMapping(
        mapping, sourceTree, targetTree) 
    if DEBUG:
        print distance
        print mapping
        print humanFriendlyDescription
    
    if outputDotGraph:
        dotRepresentation = generateDot(sourceTree, targetTree, mapping)
        _producePngFromDot(dotRepresentation)
    return distance, mapping, humanFriendlyDescription
    
# Requires: Graphviz
# sudo apt-get install graphviz
def _producePngFromDot(dotRepresentation, outputFileName="diffImage"):
    open('tmp.dot','w').write(dotRepresentation)
    import subprocess
    fullFileName = "{}.png".format(outputFileName)
    subprocess.call([
        "dot", "-Tpng", "tmp.dot", "-o", fullFileName])
    subprocess.call("eog {} &".format(fullFileName), shell=True)
    
