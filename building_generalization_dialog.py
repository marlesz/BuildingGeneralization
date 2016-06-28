# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeneralizationDialog
                                 A QGIS plugin
 Mathematical morphology-based generalization of building
                             -------------------
        begin                : 2016-02-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Marta Leszczuk
        email                : leszczuk.marta@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt4.QtGui import QFileDialog, QMessageBox

from PyQt4 import QtGui, uic
from building_generalization import *
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'building_generalization_dialog_base.ui'))


class GeneralizationDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GeneralizationDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)

    def showBrowserDialog(self):
        """Shows a file browser dialog to enter the output path."""
        fileName = QFileDialog.getSaveFileName(None, 'Save output shapefile','','Shapefiles (*.shp *.SHP)')
        self.outputPath.setText(fileName)


