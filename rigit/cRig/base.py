import maya.cmds as cmds
from ..utils import controller


class cRig():

    def __init__(self,
                prefix = 'new_',
                name = 'rig',
                suffix = '_01',
                scale = 1.0
                ):

        self.topGrp = cmds.group(n = name + '_rig_grp' + suffix, em = 1)
        self.rigGrp = cmds.group(n = 'rig_grp' + suffix, em = 1, p = self.topGrp)
        self.meshGrp = cmds.group(n = 'mesh_grp' + suffix, em = 1, p = self.topGrp)

        #Create global controller
        globalCtrl = controller.controlObject(
                                            name = 'global',
                                            scale = scale * 10,
                                            parent = self.rigGrp,
                                            lockChannels = ['v']
                                            )

        subGlobalCtrl = controller.controlObject(
                                            name = 'subGlobal',
                                            scale = scale * 9,
                                            parent = globalCtrl.ctrl,
                                            lockChannels = ['s', 'v']
                                            )

        globalCtrl.rotate_controller(['z'], 90)
        subGlobalCtrl.rotate_controller(['z'], 90)

        for axis in ['y', 'z']:
            cmds.connectAttr(globalCtrl.ctrl + '.sx', globalCtrl.ctrl + '.s' + axis)
            cmds.setAttr(globalCtrl.ctrl + '.s' + axis, k = 0)

        self.jointsGrp = cmds.group(n = 'joints_grp' + suffix, em = 1, p = subGlobalCtrl.ctrl)
        self.modulesGrp = cmds.group(n = 'modules_grp' + suffix, em = 1, p = subGlobalCtrl.ctrl)

        self.partGrp = cmds.group(n = 'part_grp' + suffix, em = 1, p = self.rigGrp)
        cmds.setAttr(self.partGrp + '.it', 0, l=1)



class cModule():

    def __init__(
                self,
                prefix = 'new_',
                name = 'module',
                suffix = '_01',
                scale = 1.0,
                base = None,
                type = ''
                ):

        self.topGrp = cmds.group(n = name + '_module_grp' + suffix, em = 1)

        self.controlsGrp = cmds.group(n = prefix + name + '_ctrlGrp' + suffix, em = 1, p = self.topGrp)
        self.jointsGrp = cmds.group(n = prefix + name + '_jntGrp' + suffix, em = 1, p = self.topGrp)
        self.partsGrp = cmds.group(n = prefix + name + '_prtGrp' + suffix, em = 1, p = self.topGrp)

        self.partsGrpLocked = cmds.group(n = prefix + name + '_prtGrp_Locked' + suffix, em = 1, p = self.topGrp)
        cmds.setAttr(self.partsGrpLocked + '.it', 0, l = 1)

        if base:
            cmds.parent(self.topGrp, base.modulesGrp)
