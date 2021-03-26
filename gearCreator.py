from maya import cmds

def createGear(teeth = 10, len = 0.3):
    """
    Create a gear with the given parameter.

    Args:
        teeth (int, optional): number of teeth to create. Defaults to 10.
        len (float, optional): length of teeth. Defaults to 0.3.

    Returns:
        tuple: a tuple of (transform, constructor, extrude face)
    """
    # teeth are every other face
    spans = teeth * 2

    # 
    transform, constructor = cmds.polyPipe(sa = spans)

    # this is because the faces we want in Maya are numbered from [spans * 2, spans * 3)
    # *** if you run ls -sl in MEL, Maya gives you all the face names
    sideFaces = range(spans * 2, spans * 3, 2)

    # clear any selection you have
    cmds.select(clear = True)

    # iterate through every other side face
    for face in sideFaces:
        cmds.select("%s.f[%s]" % (transform, face), add = True)

    # get the poly extrude face
    extrude = cmds.polyExtrudeFacet(ltz = len)[0]

    #clean up and return
    cmds.select(clear = True)
    return transform, constructor, extrude

def changeTeeth(constructor, extrude, teeth = 10, length = 0.3):
    spans = teeth * 2

    cmds.polyPipe(constructor, edit = True, sa = spans)
    sideFaces = range(spans * 2, spans * 3, 2)
    newSideFaces = []

    for face in sideFaces:
        faceName = "f[%s]" % (face)
        newSideFaces.append(faceName)

    cmds.setAttr("%s.inputComponents" % (extrude), len(newSideFaces), *newSideFaces, type = "componentList")
    cmds.polyExtrudeFacet(extrude, edit = True, ltz = length)