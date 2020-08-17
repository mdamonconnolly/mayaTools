import maya.cmds as cmds

def makeOffsetGroup(object, orient=False):

    offsetGrp = cmds.group(n = 'grpOffset_' + object, em=1)
    objParents = cmds.listRelatives(object, p = 1)

    if objectParents:
        cmds.parent(offsetGrp, objParents[0])

    cmds.delete(cmds.parentConstraint(object, offsetGrp))
    cmds.delete(cmds.scaleConstraint(object, offsetGrp))

    if orient:
        cmds.delete(cmds.orientConstraint(object, offsetGrp))

    return offsetGrp
