# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from processing.tools import vector, dataobjects
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

class Warstwa:
    def wyborWarstwy(self, nazwaWarstwy):
        rejestr = QgsMapLayerRegistry.instance()
        try:
            warstwa = rejestr.mapLayersByName(nazwaWarstwy)[0]
            iface.setActiveLayer(warstwa)
        except IndexError:
            iface.messageBar().pushMessage("Error", "Wczytaj warstwe " + nazwaWarstwy, level=QgsMessageBar.CRITICAL)
        return warstwa

    def selekcjaAtrybutowa(self, warstwa, expr):
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        return obiekty

    def utworzNowaWartswe(self, warstwa, typ, obiekty, nowaNazwaWarstwy):
        provider = warstwa.dataProvider()
        fields = provider.fields()
        outputLayer = QgsVectorLayer(typ+"?crs=EPSG:2180", nowaNazwaWarstwy, "memory")
        outputLayer.startEditing()
        for field in fields:
            outputLayer.addAttribute(field)
        outputLayer.commitChanges()
        outFeat = QgsFeature()
        for feature in obiekty:
            outFeat.setGeometry(feature.geometry())
            outFeat.setAttributes(feature.attributes())
            outputLayer.dataProvider().addFeatures([outFeat])
            outputLayer.updateExtents()
            outputLayer.updateFields()
        return outputLayer

    def polaczWarstwy(self,typ, nowaNazwaWarstwy, *warstwy):
        outputLayer = QgsVectorLayer(typ+"?crs=EPSG:2180", nowaNazwaWarstwy, "memory")
        provider = outputLayer.dataProvider()
        for warstwa in warstwy:
            fields = warstwa.pendingFields()
            for field in fields:
                provider.addAttributes([field])
            outputLayer.updateFields()
            feats1 = warstwa.getFeatures()
            for feature in feats1:
                provider.addFeatures([feature])
                outputLayer.updateFields()
        outputLayer.updateExtents()
        return outputLayer

    def usunWarstwe(self, warstwa):
        QgsMapLayerRegistry.instance().removeMapLayers([warstwa.id()])

class CentroidPoligonu:
    def centroidPoligonu(self, warstwa):
        iface.setActiveLayer(warstwa)

        provider = warstwa.dataProvider()
        fields = provider.fields()
        outputLayer = QgsVectorLayer("Point?crs=EPSG:2180", warstwa.name(), "memory")
        crs = outputLayer.crs()
        crs.createFromId(2180)
        outputLayer.setCrs(crs)

        outputLayer.startEditing()
        for field in fields:
            outputLayer.addAttribute(field)
        outputLayer.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

        outputLayer.updateFields()
        outFeat = QgsFeature()
        for feature in warstwa.getFeatures():
            outFeat.setGeometry(feature.geometry().centroid())
            outFeat.setAttributes(feature.attributes())
            outputLayer.dataProvider().addFeatures([outFeat])
            outputLayer.updateExtents()
            outputLayer.updateFields()
        return outputLayer
