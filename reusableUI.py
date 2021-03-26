import tweenerUI
import Gear

reload(tweenerUI)
reload(Gear)

from tweenerUI import tween
from Gear import Gear
from maya import cmds

class BaseWindow:

    windowName = "BaseWindow"

    def show(self):

        if cmds.window(self.windowName, query = True, exists = True):
            cmds.deleteUI(self.windowName)
        cmds.window(self.windowName, wh = (200, 80))
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)

class TweenerUI(BaseWindow):

    windowName = "TweenerWindow"

    def buildUI(self):
        column = cmds.columnLayout()

        cmds.text(label = "Use the slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns = 2)

        self.slider = cmds.floatSlider(min = 0, max = 100, value = 50, step = 1, changeCommand = tween)

        cmds.button(label = "Reset", command = self.reset)

        cmds.setParent(column)
        cmds.button(label = "Close", command = self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit = True, value = 50)

class GearUI(BaseWindow):

    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):

        column = cmds.columnLayout()
        cmds.text(label = "Use the sliders to modify the gear")

        cmds.rowLayout(numberOfColumns = 4)
        cmds.text(label = "Teeth   ")
        self.teethSlider = cmds.intSlider(min = 5, max = 30, value = 10, step = 1, dragCommand = self.modifyTeeth)
        self.teethSliderLabel = cmds.text(label = "10")
        cmds.button(label = "Reset", command = self.resetTeeth)
        cmds.setParent(column)

        cmds.rowLayout(numberOfColumns = 4)
        cmds.text(label = "Length ")
        self.lengthSlider = cmds.floatSlider(min = 0.1, max = 1.0, value = 0.3, step = 0.1, dragCommand = self.modifyLength)
        self.lengthSliderLabel = cmds.text(label = "0.3")
        cmds.button(label = "Reset", command = self.resetLength)
        cmds.setParent(column)

        cmds.rowLayout(numberOfColumns = 2)
        cmds.button(label = "Make Gear", command = self.makeGear)
        cmds.button(label = "Close", command = self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.teethSlider, query = True, value = True)
        length = cmds.floatSlider(self.lengthSlider, query = True, value = True)
        self.gear = Gear(teeth = teeth, length = length)

    def modifyTeeth(self, teeth = 10):
        if self.gear:
            self.gear.changeTeeth(teeth = teeth, length = self.gear.length)

        cmds.text(self.teethSliderLabel, edit = True, label = teeth)
    
    def modifyLength(self, length = 0.3):
        if self.gear:
            self.gear.changeTeeth(teeth = self.gear.teeth, length = length)
        
        cmds.text(self.lengthSliderLabel, edit = True, label = "%0.1f" % length)

    def resetTeeth(self, *args):
        cmds.intSlider(self.teethSlider, edit = True, value = 10)
        cmds.text(self.teethSliderLabel, edit = True, label = "10")
        self.gear.changeTeeth(length = self.gear.length)
    
    def resetLength(self, *args):
        cmds.floatSlider(self.lengthSlider, edit = True, value = 0.3)
        cmds.text(self.lengthSliderLabel, edit = True, label = "0.3")
        self.gear.changeTeeth(teeth = self.gear.teeth)