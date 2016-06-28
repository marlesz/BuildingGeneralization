# -*- coding: utf-8 -*-

from qgis.utils import *

from PyQt4.QtCore import QSettings, QTranslator, qVersion
from PyQt4.QtGui import QAction, QIcon

# Initialize Qt resources from file resources.py
# Import the code for the dialog
from matplotlib.backends.qt4_editor.formlayout import QColor

from building_generalization_dialog import GeneralizationDialog
import os.path
from selekcja50k import *
from WarstwaOperacje import *
import processing
from PyQt4.QtCore import QVariant
from math import degrees, atan2
from qgis.core import QGis, QgsField, QgsPoint, QgsGeometry, QgsFeature
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.tools import dataobjects, vector


class OrientedMinimumBoundingBox(GeoAlgorithm):
        def featureOmbb2(self, layer, newlayerName, type):
            provider = layer.dataProvider()
            fields = provider.fields()
            outputLayer = QgsVectorLayer(type + "?crs=EPSG:2180", newlayerName, "memory")
            outputLayer.startEditing()
            for field in fields:
                outputLayer.addAttribute(field)
            outputLayer.updateFields()
            outputLayer.commitChanges()
            outputLayer.startEditing()
            features = vector.features(layer)
            outFeat = QgsFeature()
            ids = []
            for current, inFeat in enumerate(features):
                geometry, area, perim, angle, width, height = self.OMBBox(inFeat.geometry())
                outFeat.setAttributes(inFeat.attributes())
                outFeat.setGeometry(geometry)
                outputLayer.addFeature(outFeat)
            outputLayer.commitChanges()
            return outputLayer

        def featureOmbb(self, layer, minwidth, minheight):
            features = vector.features(layer)
            outFeat = QgsFeature()
            ids = []
            for current, inFeat in enumerate(features):
                geometry, area, perim, angle, width, height = self.OMBBox(inFeat.geometry())
                if width<= minwidth or height <= minheight:
                    ids.append(inFeat.id())
            QgsMessageLog.logMessage("zbyt małe obszary" +str(len(ids)))
            return ids

        def GetAngleOfLineBetweenTwoPoints(self, p1, p2, angle_unit="degrees"):
            xDiff = p2.x() - p1.x()
            yDiff = p2.y() - p1.y()
            if angle_unit == "radians":
                return atan2(yDiff, xDiff)
            else:
                return degrees(atan2(yDiff, xDiff))

        def OMBBox(self, geom):
            g = geom.convexHull()
            if g.type() != QGis.Polygon:
                return None, None, None, None, None, None
            r = g.asPolygon()[0]
            p0 = QgsPoint(r[0][0], r[0][1])
            i = 0
            l = len(r)
            OMBBox = QgsGeometry()
            gBBox = g.boundingBox()
            OMBBox_area = gBBox.height() * gBBox.width()
            OMBBox_angle = 0
            OMBBox_width = 0
            OMBBox_heigth = 0
            OMBBox_perim = 0
            while i < l - 1:
                x = QgsGeometry(g)
                angle = self.GetAngleOfLineBetweenTwoPoints(r[i], r[i + 1])
                x.rotate(angle, p0)
                bbox = x.boundingBox()
                bb = QgsGeometry.fromWkt(bbox.asWktPolygon())
                bb.rotate(-angle, p0)

                areabb = bb.area()
                if areabb <= OMBBox_area:
                    OMBBox = QgsGeometry(bb)
                    OMBBox_area = areabb
                    OMBBox_angle = angle
                    OMBBox_width = bbox.width()
                    OMBBox_heigth = bbox.height()
                    OMBBox_perim = 2 * OMBBox_width + 2 * OMBBox_heigth
                i += 1
            return OMBBox, OMBBox_area, OMBBox_perim, OMBBox_angle, OMBBox_width, OMBBox_heigth

class Simplification(OrientedMinimumBoundingBox):
        def fillHoles(self, layer, minWidth, minHeight, layerName):
            provider = layer.dataProvider()
            fields = provider.fields()
            writer = QgsVectorLayer("Polygon?crs=EPSG:2180", layerName, "memory")
            writer.startEditing()
            layer.startEditing()
            for feat in layer.getFeatures():
                geometry = feat.geometry()
                if geometry.isMultipart():
                    multi_polygon = geometry.asMultiPolygon()
                    for polygon in multi_polygon:
                        for ring in polygon[1:]:
                            geometry, area, perim, angle, width, height = self.OMBBox(QgsGeometry.fromPolygon([ring]))
                            if width <= minWidth or height <= minHeight or area <=minWidth*minHeight:
                                polygon.remove(ring)
                    geometry = QgsGeometry.fromMultiPolygon(multi_polygon)
                else:
                    polygon = geometry.asPolygon()
                    for ring in polygon[1:]:
                        geometry, area, perim, angle, width, height = self.OMBBox(QgsGeometry.fromPolygon([ring]))
                        if width <= minWidth or height <= minHeight or area <= minWidth * minHeight:
                            polygon.remove(ring)
                    geometry = QgsGeometry.fromPolygon(polygon)

                outFeat = QgsFeature()
                outFeat.setGeometry(geometry)
                writer.addFeature(feat)
            writer.commitChanges()
            layer.commitChanges()
            return writer