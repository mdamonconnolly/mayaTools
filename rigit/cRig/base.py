import maya.cmds as cmds
from ..utils import controller


class cRig():

    def __init__(self,
                name = 'new',
                scale = 1.0
                ):

        self.topGrp = cmds.group(n = name + '_rig_grp', em = 1)
        self.rigGrp = cmds.group(n = 'rig_grp', em = 1, p = self.topGrp)
        self.meshGrp = cmds.group(n = 'mesh_grp', em = 1, p = self.topGrp)

        #Create global controller
        globalCtrl = controller.controlObject(
                                            name = 'global',
                                            scale = scale * 10,
                                            parent = self.rigGrp,
                                            lockChannels = ['v']
                                            )

        globalCtrl2 = controller.controlObject(
                                            name = 'global2',
                                            scale = scale * 9,
                                            parent = globalCtrl.ctrl,
                                            lockChannels = ['s', 'v']
                                            )

        globalCtrl.rotate_controller(['z'], 90)

        for axis in ['y', 'z']:
            cmds.connectAttr(globalCtrl.ctrl + '.sx', globalCtrl.ctrl + '.s' + axis)
            cmds.setAttr(globalCtrl.ctrl + '.s' + axis, k = 0)

        self.jointsGrp = cmds.group(n = 'joints_grp', em = 1, p = globalCtrl2.ctrl)
        self.modulesGrp = cmds.group(n = 'modules_grp', em = 1, p = globalCtrl2.ctrl)

        self.partGrp = cmds.group(n = 'part_grp', em = 1, p = self.rigGrp)
        cmds.setAttr(self.partGrp + '.it', 0, l=1)
