from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial
import Qt
import logging

if Qt.__binding__ = 'PySide':
    from shiboken import wrapInstance
    from QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    from sip import wrapinstance
    from QtCore import pytqSignal as Signal
else:
    from shiboken2 import wrapInstance
    from QtCore import Signal

class LightManager(QtWidgets.QDialog):

    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight = True),
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight = True)
    }

    def __init__(self):
        super(LightManager, self).__init__()
        self.setWindowTitle('Lighting Manager')
        self.buildUI()
        self.populate()

    def populate(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widet()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()
        for light in pm.ls(type = ["areaLight", "spotLight", "directionalLight", "pointLight", "volumeLight"]):
            self.addLight(light)

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            self. lightTypeCB.addItem(lightType)
        layout.addWidget(self.lightTypeCB, 0, 0)

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 1)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 2)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        layout.addWidget(refreshBtn, 2, 1)


    def createLight(self):
        lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]

        light = func()
        self.addLight(light)

    def addLight(self, light):
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        lightWidgets = self.findChildren(LightWidget)
        print lightWidgets
        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)

class LightWidget(QtWidgets.QWidget):

    onSolo = Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()
        if isinstance(light, basestring):
            light = pm.PyNode(light)
        
        self.light = light
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val : self.light.visibility.set(val))
        layout.addWidget(self.name, 0, 0)

        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val : self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0, 1)

        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)

        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1)
        intensity.setMaximum(1000)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val : self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)

        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

    def setButtonColor(self, color = None):
        if not color:
            color = self.light.color.get()
        
        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]
        
        self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0)' % (r, g, b))

    def setColor(self):
        lightColor = self.light.color.get()
        color = pm.colorEditor(rgbValue = lightColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)

        self.light.color.set(color)
        self.setButtonColor(color)

    def disableLight(self, value):
        self.name.setChecked(not value)

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.light.getTransform())


def showUI():
    ui = LightManager()
    ui.show()

    return ui