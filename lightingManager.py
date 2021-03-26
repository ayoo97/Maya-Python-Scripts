from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial

class LightManager(QtWidgets.QDialog):

    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight = True)
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight = True)
    }

    def __init__(self):
        super(LightManager, self).__init__()
        self.setWindowTitle('Lighting Manager')
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in self.lightTypes:
            self.lightTypeCB.addItem(lightType)
        layout.addWidget(self.lightTypeCB, 0, 0)

        createBtn = QtWidgets.QPushButton('Create')
        layout.addWidget(createBtn, 0, 1)

def showUI():
    ui = LightManager()
    ui.show()

    return uif