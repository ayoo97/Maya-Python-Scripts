from maya import cmds

import pprint

import controllerLibrary
reload(controllerLibrary)

from Qt import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The  ControllerLibraryUI is a dialog that lets us save and import controllers
    """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')

        # The library variable points to an instace of our controller library
        self.library = controllerLibrary.ControllerLibrary()

        # Every time we create a new instance, we will automaticaly build out UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """
        This method builds out the UI
        """
        layout = QtWidgets.QVBoxLayout(self)

        # This is the child horizontal widget
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # These are the parameters for our thumbnail size
        size = 64
        buffer = 12

        # This will create a grid list widget to display out controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)



    def populate(self):
        """
        This clears the listWidget and then repopulates is with the contents of our library
        """
        self.listWidget.clear()
        self.library.find()
        
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        """
        This loads the currently selected controller
        """
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """
        This saves the controller with the given file name
        """
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')


def showUI():
    """
    Show dialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui