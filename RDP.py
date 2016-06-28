# -*- coding: utf-8 -*-

"""
***************************************************************************
    SimplifyGeometries.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QGis, QgsFeature, QgsGeometry
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.ProcessingLog import ProcessingLog
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterNumber
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector


class SimplifyGeometries(GeoAlgorithm):
    def processAlgorithm(self, layer, tolerance, layerName):
        writer = QgsVectorLayer("Polygon?crs=EPSG:2180", layerName, "memory")
        writer.startEditing()
        pointsBefore = 0
        pointsAfter = 0

        features = vector.features(layer)
        for current, f in enumerate(features):
            featGeometry = QgsGeometry(f.geometry())
            pointsBefore += self.geomVertexCount(featGeometry)
            newGeometry = featGeometry.simplify(tolerance)
            pointsAfter += self.geomVertexCount(newGeometry)
            feature = QgsFeature()
            feature.setGeometry(newGeometry)
            writer.addFeature(feature)
        writer.commitChanges()
        return writer
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO,
                               self.tr('Simplify: Input geometries have been simplified from %s to %s points' % (pointsBefore, pointsAfter)))

    def geomVertexCount(self, geometry):
        geomType = geometry.type()
        if geomType == QGis.Line:
            if geometry.isMultipart():
                pointsList = geometry.asMultiPolyline()
                points = sum(pointsList, [])
            else:
                points = geometry.asPolyline()
            return len(points)
        elif geomType == QGis.Polygon:
            if geometry.isMultipart():
                polylinesList = geometry.asMultiPolygon()
                polylines = sum(polylinesList, [])
            else:
                polylines = geometry.asPolygon()
            points = []
            for l in polylines:
                points.extend(l)
            return len(points)
        else:
            return None