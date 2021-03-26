from maya import cmds

class Gear:

    def __init__(self, teeth = 10, length = 0.3):
        """
        Create a gear with the given parameter.

        Args:
            teeth (int, optional): number of teeth to create. Defaults to 10.
            len (float, optional): length of teeth. Defaults to 0.3.

        Returns:
            tuple: a tuple of (transform, constructor, extrude face)
        """
        self.teeth = teeth
        self.length = length
        # teeth are every other face
        spans = teeth * 2
 
        pipeObj = cmds.polyPipe(sa = spans)
        self.transform = pipeObj[0] + "_gear"
        self.constructor = pipeObj[1]
        
        # rename object
        cmds.rename(pipeObj[0], self.transform)

        # this is because the faces we want in Maya are numbered from [spans * 2, spans * 3)
        # *** if you run ls -sl in MEL, Maya gives you all the face names
        sideFaces = range(spans * 2, spans * 3, 2)

        # clear any selection you have
        cmds.select(clear = True)

        # iterate through every other side face
        for face in sideFaces:
            cmds.select("%s.f[%s]" % (self.transform, face), add = True)

        # get the poly extrude face
        self.extrude = cmds.polyExtrudeFacet(ltz = length)[0]

        #clean up and return
        cmds.select(clear = True)
    
    def changeTeeth(self, teeth = 10, length = 0.3):
        self.teeth = teeth
        self.length = length
        spans = teeth * 2
        cmds.polyPipe(self.constructor, edit = True, sa = spans)
        sideFaces = range(spans * 2, spans * 3, 2)
        newSideFaces = []

        for face in sideFaces:
            faceName = "f[%s]" % (face)
            newSideFaces.append(faceName)

        cmds.setAttr("%s.inputComponents" % (self.extrude), len(newSideFaces), *newSideFaces, type = "componentList")
        cmds.polyExtrudeFacet(self.extrude, edit = True, ltz = length)