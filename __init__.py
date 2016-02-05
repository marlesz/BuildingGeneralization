# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Generalization
                                 A QGIS plugin
 Mathematical morphology-based generalization of building
                             -------------------
        begin                : 2016-02-03
        copyright            : (C) 2016 by Marta Leszczuk
        email                : leszczuk.marta@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Generalization class from file Generalization.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .building_generalization import Generalization
    return Generalization(iface)
