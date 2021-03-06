# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Generalization
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
import os.path
from qgis.utils import *
from PyQt4.QtCore import QVariant

from PyQt4.QtCore import QSettings, QTranslator, qVersion
from PyQt4.QtGui import QAction, QIcon

# Initialize Qt resources from file resources.py
# Import the code for the dialog
#from building_generalization_dialog import GeneralizationDialog
import os.path
from selekcja50k import *
from WarstwaOperacje import *
from morfologia import *
from RDP import *
#from piedziesiat import *
import processing
from simplification import *
from Morphology import *
from roadsSimplification import *
from buildingSimplification import *
from buildingsAreaSimplification import *
from dissolveWiithFields import *
class Generalization:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Generalization_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GeneralizationDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Building Generalization')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Generalization')
        self.toolbar.setObjectName(u'Generalization')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Generalization', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Generalization/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'BuildingGeneralization'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.BuildingsAreaButton.clicked.connect(self.buildingsAreaClicked)
        self.dlg.RoadsButton.clicked.connect(self.roadsClicked)
        self.dlg.BuildingButton.clicked.connect(self.buildingClicked)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Building Generalization'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            #Do something useful here - delete the line containing pass and
            # substitute with your code.

            pass


    def buildingsAreaClicked (self):
        buildArea = BuildingsAreaSimplification()
        buildArea.simplify()




    def roadsClicked(self):
        roads  = RoadSimplification()
        roads.simplify()

    def buildingClicked(self):
        build = BuildingSimplification()
        build.simplify()








