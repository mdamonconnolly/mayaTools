"""
mesh @ utils

This module will supply tools for getting mesh related data.
"""

import maya.cmds as cmds

def getBound(meshObjects, boundCenter=False, locatorsAtBounds=False):
    """
    This function returns the bounding box information.
    """

    meshObjects = cmds.ls(selection=True)

    lowerBounds = []
    upperBounds = []

    for obj in meshObjects:

        lowerBounds.append(cmds.exactWorldBoundingBox(obj)[:3])
        upperBounds.append(cmds.exactWorldBoundingBox(obj)[3:])
            
    finalBounds = list(map(min, *lowerBounds)) + list(map(max, *upperBounds))

    if locatorsAtBounds:
        locGrp = cmds.group(n = 'locGrp', em = 1)

        for itt, coord in enumerate(finalBounds):
            if itt == 0 or itt == 3:
                locX = cmds.spaceLocator(p=(coord, 0, 0))
                cmds.parent(locX, locGrp)
            if itt == 1 or itt == 4:
                locY = cmds.spaceLocator(p=(0, coord, 0))
                cmds.parent(locY, locGrp)
            if itt == 2 or itt == 5:
                locZ = cmds.spaceLocator(p=(0, 0, coord))
                cmds.parent(locZ, locGrp)

    return finalBounds
