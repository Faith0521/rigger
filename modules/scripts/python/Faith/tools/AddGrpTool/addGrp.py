# Embedded file name: E:\JunCmds\tool\AddGrpTool\addGrp.py
import maya.cmds as cmds
import maya.mel as mel

class AddGrp:

    def __init__(self):
        pass

    def AttrSet(self, ObjattrDatadic):
        """
        attrDatadic = {obj.Attr:data,obj.Attr:data}
        """
        for objattr in ObjattrDatadic:
            Data = ObjattrDatadic.get(objattr)
            cmds.setAttr(objattr, Data)

    def GrpAdd(self, Obj, GrpNames, addgrpRelativeTier):
        objParent = cmds.listRelatives(Obj, p=True, f=True)
        GrpNames = GrpNames[::-1]
        Grps = []
        for grp in GrpNames:
            if cmds.objExists(grp) == True:
                cmds.warning(grp + '------ is exists')
            if grp == GrpNames[0]:
                grp = cmds.group(em=True)
                Grps.append(grp)
            else:
                grp = cmds.group()
                Grps.append(grp)

        Grps = Grps[::-1]
        topGrp = Grps[0]
        EndGrp = Grps[-1]
        cmds.parent(topGrp, Obj)
        self.AttrSet({topGrp + '.rx': 0,
         topGrp + '.ry': 0,
         topGrp + '.rz': 0,
         topGrp + '.tx': 0,
         topGrp + '.ty': 0,
         topGrp + '.tz': 0,
         topGrp + '.sx': 1,
         topGrp + '.sy': 1,
         topGrp + '.sz': 1})
        if addgrpRelativeTier == 'Up':
            cmds.parent(topGrp, w=True)
            if objParent != None:
                cmds.parent(topGrp, objParent)
            cmds.parent(Obj, EndGrp)
        elif addgrpRelativeTier == 'Dn':
            pass
        Grps = Grps[::-1]
        cmds.select(Grps, add=True)
        for i in range(len(Grps)):
            cmds.rename(Grps[i], GrpNames[i])

        reGrps = cmds.ls(sl=True)[::-1]
        print(reGrps)
        return (reGrps, topGrp, EndGrp)