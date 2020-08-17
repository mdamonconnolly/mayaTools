import maya.cmds as cmds


def renameChain(root, stopAtFork = True):
    pass

def getHierarchy(root, includeEnd = True):

    listedJoints = cmds.listRelatives(root, type='joint', ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()

    jointList = listedJoints[:]

    if not includeEnd:
        jointList = [j for j in listedJoints if cmds.listRelatives(j, c = 1, type = 'joint')]

    return jointList
