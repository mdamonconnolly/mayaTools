import maya.cmds as cmds

class controlObject():

    """
    This is the control object used for curve controllers for the rig.
    The controller will pick the shape from a shapes.json file.
    """

    def __init__(
                self,
                prefix = 'ctrl_',
                name = '',
                suffix = '01',
                shape = '',
                color = '',
                translate = 0.0,
                rotate = 0.0,
                scale = 1.0,
                parent = '',
                createAt = '',
                orientTo = '',
                lockChannels = ['s', 'v']
                ):

        if shape != '':

            ctrl = cmds.curve(
                n = prefix + name + suffix,
                d = shapes[shape][0],
                p = shapes[shape][1],
                k = shapes[shape][2]
            )
        else:
            ctrl = cmds.circle(n = prefix + name + suffix, ch = False, normal = [1, 0, 0], radius = scale)[0] 


        ctrlShp = cmds.listRelatives(ctrl, s=1)[0]

        ctrlGrp = cmds.group(n = prefix + 'grp_' + name, em=1)
        cmds.parent(ctrl, ctrlGrp)


        #Handle positions
        if cmds.objExists(createAt):
            cmds.delete(cmds.pointConstraint(createAt, ctrlGrp))
        if cmds.objExists(orientTo):
            cmds.delete(cmds.orientConstraint(orientTo, ctrlGrp))
        if cmds.objExists(parent):
            cmds.parent(ctrlGrp, parent)

        lockList = []
        #Handle Channel Locking
        for channel in lockChannels:
            if channel in ['t', 'r', 's']:
                for axis in ['x', 'y', 'z']:                    
                    at = channel + axis
                    lockList.append(at)
            else:
                lockList.append(channel)

        for attr in lockList:
            cmds.setAttr(ctrl + '.' + attr, l = 1, k = 0)

        cmds.setAttr(ctrlShp + '.ove', 1)

        if '_l_' in name:
            cmds.setAttr(ctrlShp + '.ovc', 6)
        elif '_r_' in name:
            cmds.setAttr(ctrlShp + '.ovc', 13)
        else:
            cmds.setAttr(ctrlShp + '.ovc', 22)

        self.ctrl = ctrl
        self.ctrlGrp = ctrlGrp

    def rotate_controller(self, channels = ['x', 'y', 'z'], value=0):
        """
        This will take an input object and rotate its shape node by the value (in degrees) on the axis provided
        """

        ctrlShapes = cmds.listRelatives(self.ctrl, s=1, type = 'nurbsCurve')
        cluster = cmds.cluster(ctrlShapes)[1]

        for axis in channels:
            cmds.setAttr(cluster + '.r' + axis, value)
        cmds.delete(ctrlShapes, ch = 1)


#TODO: Temporary globals. Move into local file.
shapes = {
    "softArrow" : [
        3,
        [(0, 0, 2), (-1, 0 , 2), (-2, 0 , 2), (-2, 0, 1), (-2, 0, 0), (-1, 0, -2), (0, 0, -3), (1, 0 , -2), (2, 0, 0), (2, 0, 1), (2, 0, 2), (1, 0, 2), (0, 0, 2)],
        [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10]
    ]
}
