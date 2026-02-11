import os
from importlib import reload
import maya.cmds as mc
import maya.mel as mel
import snap
reload(snap)

if 'rxRIGHT_MENU' not in os.environ.keys():
    os.environ['rxRIGHT_MENU'] = 'False'

def toggle():
    if os.environ['rxRIGHT_MENU'] == 'False':
        os.environ['rxRIGHT_MENU'] = 'True'
        mc.inViewMessage( amg='RX Custom Right-Button is <hl>Enabled</hl>.', pos='midCenter', fade=True )

    else:
        os.environ['rxRIGHT_MENU'] = 'False'
        mc.inViewMessage( amg='RX Custom Right-Button is <hl>Disabled</hl>.', pos='midCenter', fade=True )

# over write and recreate custom menu
def createMenu(parentName):
    if os.environ['rxRIGHT_MENU'] == 'False':
        return

    ctrls = mc.ls(sl=1)
    if not ctrls:
        return   

    ctrl = ctrls[-1]
    if not mc.nodeType(ctrl) == 'transform'and not mc.nodeType(ctrl) == 'joint':
        return 
    if not mc.objExists(ctrl+'.controlID'):
        return

    mc.popupMenu(parentName, e=1, dai=1)
    mc.menuItem(l='* '+ctrl+' *')

    # ik fk snap
    if mc.objExists(ctrl+'.tagIkFkSnap'):
        mc.menuItem(d=1)
        mc.menuItem(l='Noflip Fk / Ik', c='import snap; snap.limb()')

    # spaces snap
    if mc.objExists(ctrl+'.space'):
        mc.menuItem(d=1)
        spaces = mc.addAttr(ctrl+'.space',q=1,en=1).split(':')
        for space in spaces:
            mc.menuItem(l='Noflip Space: '+space ,c='import snap; snap.space("'+space+'")')

    # pivot snap
    if mc.objExists(ctrl+'.footPivot'):
        mc.menuItem(d=1)
        mc.menuItem(l='Toe Pivot', c='import snap; snap.footPivot("toe")')
        mc.menuItem(l='Ball Pivot', c='import snap; snap.footPivot("ball")')
        mc.menuItem(l='Ankle Pivot', c='import snap; snap.footPivot("ankle")')
        mc.menuItem(l='Heel Pivot', c='import snap; snap.footPivot("heel")')
        mc.menuItem(l='Inner Pivot', c='import snap; snap.footPivot("inner")')
        mc.menuItem(l='Outter Pivot', c='import snap; snap.footPivot("outter")')
        mc.menuItem(l='Movable Pivot', c='import snap; snap.footPivot("movable")')

    #mc.menuItem(d=1)


arg2022 = r"""
global proc buildObjectMenuItemsNow( string $parentName)
{
    if (`exists DRUseModelingToolkitMM` && DRUseModelingToolkitMM($parentName)) {
        return;
    }

    global int $gIsMarkingMenuOn;

    if (`popupMenu -e -exists $parentName`) {
        popupMenu -e -deleteAllItems $parentName;   
        if (`popupMenu -q -mm $parentName` != $gIsMarkingMenuOn) {
            popupMenu -e -mm $gIsMarkingMenuOn $parentName;
        }

        int $editMode = 0;
        string $currentContext = `currentCtx`; 
        if (`contextInfo -exists $currentContext`) {
            string $ctx = `contextInfo -c $currentContext`; 
            if ($ctx == "manipMove") { 
                $editMode = `manipMoveContext -q -editPivotMode Move`;
            } else if ($ctx == "manipScale") { 
                $editMode = `manipScaleContext -q -editPivotMode Scale`;
            } else if ($ctx == "manipRotate") { 
                $editMode = `manipRotateContext -q -editPivotMode Rotate`;
            } else if ($ctx == "sculptMeshCache") {
                setParent -menu $parentName;
                sculptMeshCacheOptionsPopup();
                return;
            }
        }

        if ($editMode) {
            setParent -menu $parentName;

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kPinComponentPivot"))
                -checkBox `manipPivot -q -pin`
                -radialPosition "N"
                -command ("setTRSPinPivot #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivot"))
                -radialPosition "S"
                -command ("manipPivotReset true true");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kSnapPivotOrientation"))
                -checkBox `manipPivot -q -snapOri`
                -radialPosition "NW"
                -command ("setTRSSnapPivotOri #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kSnapPivotPosition"))
                -checkBox `manipPivot -q -snapPos`
                -radialPosition "NE"
                -command ("setTRSSnapPivotPos #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivotOrientation"))
                -radialPosition "SW"
                -command ("manipPivotReset false true");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivotPosition"))
                -radialPosition "SE"
                -command ("manipPivotReset true false");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kExitPivotMode"))
                -radialPosition "E"
                -command ("ctxEditMode");

            setParent ..;
        } else {
            if (!`dagObjectHit -mn $parentName`) {
                // Nothing was hit - check selection/hilight list...
                string $leadObject[] = `ls -sl -tail 1 -typ transform -typ shape`;
                if (size($leadObject) == 0) {
                    $leadObject = `ls -hl -tail 1 -typ transform -typ shape`;
                }               
                if (size($leadObject) > 0) {
                    dagMenuProc($parentName, $leadObject[0]);
                } else {
                    if (`modelingTookitActive` && (`nexCtx -rmbComplete -q`) ) {
                        ctxCompletion;
                        return;
                    }
                    setParent -menu $parentName;

                    menuItem
                        -version "2014"
                        -label (uiRes("m_buildObjectMenuItemsNow.kSelectAll"))
                        -radialPosition "S"
                        -command ("SelectAll");

                    menuItem
                        -label (uiRes("m_buildObjectMenuItemsNow.kCompleteTool"))
                        -radialPosition "N"
                        -command ("CompleteCurrentTool");

                    setParent ..;
                }
            }
        }
    } else {
        warning (uiRes("m_buildObjectMenuItemsNow.kParentWarn"));
    }
    string $arg = "import rightClickMenu; rightClickMenu.createMenu(\""+$parentName+"\")";
    catch (`python ($arg)`);
}"""


arg2025 = r"""
global proc buildObjectMenuItemsNow( string $parentName)
{
    if (`exists DRUseModelingToolkitMM` && DRUseModelingToolkitMM($parentName)) {
        return;
    }

    global int $gIsMarkingMenuOn;

    if (`popupMenu -e -exists $parentName`) {
        popupMenu -e -deleteAllItems $parentName;   
        if (`popupMenu -q -mm $parentName` != $gIsMarkingMenuOn) {
            popupMenu -e -mm $gIsMarkingMenuOn $parentName;
        }

        int $editMode = 0;
        string $currentContext = `currentCtx`; 
        if (`contextInfo -exists $currentContext`) {
            string $ctx = `contextInfo -c $currentContext`; 
            if ($ctx == "manipMove") { 
                $editMode = `manipMoveContext -q -editPivotMode Move`;
            } else if ($ctx == "manipScale") { 
                $editMode = `manipScaleContext -q -editPivotMode Scale`;
            } else if ($ctx == "manipRotate") { 
                $editMode = `manipRotateContext -q -editPivotMode Rotate`;
            } else if ($ctx == "sculptMeshCache") {
                setParent -menu $parentName;
                sculptMeshCacheOptionsPopup();
                return;
            }
        }

        if ($editMode) {
            setParent -menu $parentName;

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kPinComponentPivot"))
                -checkBox `manipPivot -q -pin`
                -radialPosition "N"
                -command ("setTRSPinPivot #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivot"))
                -radialPosition "S"
                -command ("manipPivotReset true true");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kSnapPivotOrientation"))
                -checkBox `manipPivot -q -snapOri`
                -radialPosition "NW"
                -command ("setTRSSnapPivotOri #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kSnapPivotPosition"))
                -checkBox `manipPivot -q -snapPos`
                -radialPosition "NE"
                -command ("setTRSSnapPivotPos #1");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivotOrientation"))
                -radialPosition "SW"
                -command ("manipPivotReset false true");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kResetPivotPosition"))
                -radialPosition "SE"
                -command ("manipPivotReset true false");

            menuItem
                -label (uiRes("m_buildObjectMenuItemsNow.kExitPivotMode"))
                -radialPosition "E"
                -command ("ctxEditMode");

            setParent ..;
        } else {
            if (!`dagObjectHit -mn $parentName`) {
                // Nothing was hit - check selection/hilight list...
                string $leadObject[] = `ls -sl -tail 1 -typ transform -typ shape`;
                if (size($leadObject) == 0) {
                    $leadObject = `ls -hl -tail 1 -typ transform -typ shape`;
                }               
                if (size($leadObject) > 0) {
                    dagMenuProc($parentName, $leadObject[0]);
                } else {
                    if (`modelingTookitActive` && (`nexCtx -rmbComplete -q`) ) {
                        ctxCompletion;
                        return;
                    }
                    setParent -menu $parentName;

                    menuItem
                        -version "2025"
                        -label (uiRes("m_buildObjectMenuItemsNow.kSelectAll"))
                        -radialPosition "S"
                        -command ("SelectAll");

                    menuItem
                        -label (uiRes("m_buildObjectMenuItemsNow.kCompleteTool"))
                        -radialPosition "N"
                        -command ("CompleteCurrentTool");

                    setParent ..;
                }
            }
        }
    } else {
        warning (uiRes("m_buildObjectMenuItemsNow.kParentWarn"));
    }
    string $arg = "import rightClickMenu; rightClickMenu.createMenu(\""+$parentName+"\")";
    catch (`python ($arg)`);
}"""

if mc.about(v=1) == '2022':
    mel.eval(arg2022)
elif mc.about(v=1) == '2025':
    mel.eval(arg2025)
else:
    pass