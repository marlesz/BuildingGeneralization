# -*- coding: utf-8 -*-
from shapely.geometry import Point, MultiLineString, Polygon, LineString
from shapely.ops import polygonize
from shapely.ops import unary_union
import qgis
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.analysis import *
from WarstwaOperacje import *
from RDP import*
class Morphology(Warstwa):
    def buffering(self, ring, bufferSize, segments):
        outFeat = QgsFeature()
        value = bufferSize
        inGeom = QgsGeometry(ring)
        outGeom = inGeom.buffer(float(value), segments)
        outFeat.setGeometry(outGeom)
        return outFeat
        del outFeat

    def getOuterRing(self, inFeat):
        geom = inFeat.geometry()
        ring = QgsGeometry.fromPolyline(geom.asPolygon()[0])
        return ring
        del ring

    def getInnerRing(self, inFeat, n):
        #if n = 0, get all inner rings
        geom = inFeat.geometry()
        if self.countInnerRing(inFeat)>0:
            if n == 0:
                ringsList = []
                numInnerRings = self.countInnerRing(inFeat)
                for num in range(1, numInnerRings + 1):
                    ring = QgsGeometry.fromPolyline(geom.asPolygon()[num])
                    ringsList.append(QgsGeometry(ring))
                return ringsList
            else:
                ring = QgsGeometry.fromPolyline(geom.asPolygon()[n])
                return ring

    def countInnerRing(self, inFeat):
        geom = inFeat.geometry()
        countInner = len(geom.asPolygon())-1
        return countInner

    def dillation(self,inFeat, bufferSize, segments):
        outerRing = self.getOuterRing(inFeat)
        innerRings = self.getInnerRing(inFeat, 0)
        bufferr = self.buffering(outerRing, bufferSize, segments)
        outerBufferRing = self.getOuterRing(bufferr)
        if self.countInnerRing(inFeat)>0:
            poly = []
            poly.append(outerBufferRing.asPolyline())
            for inner in innerRings:
                poly.append(inner.asPolyline())
            polygon = QgsGeometry.fromPolygon(poly)
        else:
            polygon = QgsGeometry.fromPolygon([outerBufferRing.asPolyline()])
        outFeat = QgsFeature()
        outFeat.setGeometry(polygon)
        return outFeat


    def dillationWithInnerRings(self, inFeat, bufferSize, segments):
            outerRing = self.getOuterRing(inFeat)
            innerRings = self.getInnerRing(inFeat, 0)
            bufferOuter = self.buffering(outerRing, bufferSize, segments)
            outerBufferRing = self.getOuterRing(bufferOuter)
            #if outer ring is dillated, inner ring is eroded
            if innerRings:
                poly = []
                poly.append(outerBufferRing.asPolyline())
                for inner in innerRings:
                    bufferInner = self.buffering(inner, bufferSize, segments)
                    outerBufferInnerRing = self.getOuterRing(bufferInner)
                    poly.append(outerBufferInnerRing.asPolyline())
                    polygon = QgsGeometry.fromPolygon(poly)
            else:
                polygon = QgsGeometry.fromPolygon([outerBufferRing.asPolyline()])
            outFeat = QgsFeature()
            outFeat.setGeometry(polygon)
            return outFeat



    def erosion(self, inFeat, bufferSize, segments):
        outerRing = self.getOuterRing(inFeat)
        innerRings = self.getInnerRing(inFeat, 0)
        bufferr = self.buffering(outerRing, bufferSize, segments)
        #QgsMessageLog.logMessage(str(bufferr.geometry().type()))
        innerBufferRings = self.getInnerRing(bufferr, 0)
        if innerBufferRings:
            poly = []
            if len(innerBufferRings)>1:
                for innerBuffer in innerBufferRings:
                    if QgsGeometry.fromPolygon([outerRing.asPolyline()]).contains(QgsGeometry.fromPolygon([innerBuffer.asPolyline()])):
                        poly.append([innerBuffer.asPolyline()])
                if innerRings:
                    for i, pol in enumerate(poly):
                        for inner in innerRings:
                            if QgsGeometry.fromPolygon(pol).contains(QgsGeometry.fromPolygon([inner.asPolyline()])):
                                pol.append(inner.asPolyline())
                    polygon = QgsGeometry.fromMultiPolygon(poly)
                else:
                    polygon = QgsGeometry.fromMultiPolygon(poly)
            else:
                for innerBuffer in innerBufferRings:
                    if QgsGeometry.fromPolygon([outerRing.asPolyline()]).contains(QgsGeometry.fromPolygon([innerBuffer.asPolyline()])):
                        poly.append(innerBuffer.asPolyline())
                if innerRings:
                    for inner in innerRings:
                        if QgsGeometry.fromPolygon([poly[0]]).contains(QgsGeometry.fromPolygon([inner.asPolyline()])):
                            poly.append(inner.asPolyline())
                    polygon = QgsGeometry.fromPolygon(poly)
                else:
                    polygon = QgsGeometry.fromPolygon(poly)
            outFeat = QgsFeature()
            outFeat.setGeometry(polygon)
            # else:
            #    outFeat = inFeat
            return outFeat

    def erosionWithInnerRings(self, inFeat, bufferSize, segments):
        outerRing = self.getOuterRing(inFeat)
        innerRings = self.getInnerRing(inFeat, 0)
        bufferr = self.buffering(outerRing, bufferSize, segments)
        # QgsMessageLog.logMessage(str(bufferr.geometry().type()))
        innerBufferRings = self.getInnerRing(bufferr, 0)
        if innerBufferRings:
            poly = []
            if len(innerBufferRings)>1:
                for innerBuffer in innerBufferRings:
                    if QgsGeometry.fromPolygon([outerRing.asPolyline()]).contains(QgsGeometry.fromPolygon([innerBuffer.asPolyline()])):
                        poly.append([innerBuffer.asPolyline()])
                if innerRings:
                    for i, pol in enumerate(poly):
                        for inner in innerRings:
                            if QgsGeometry.fromPolygon(pol).contains(QgsGeometry.fromPolygon([inner.asPolyline()])):
                                bufferInner = self.buffering(inner, bufferSize, segments)
                                innerBufferInnerRing = self.getInnerRing(bufferInner, 0)
                                if innerBufferInnerRing:
                                    for allin in innerBufferInnerRing:
                                        if QgsGeometry.fromPolygon([inner.asPolyline()]).contains(QgsGeometry.fromPolygon([allin.asPolyline()])):
                                            pol.append(allin.asPolyline())
                    polygon = QgsGeometry.fromMultiPolygon(poly)
                else:
                    polygon = QgsGeometry.fromMultiPolygon(poly)
            else:
                for innerBuffer in innerBufferRings:
                    if QgsGeometry.fromPolygon([outerRing.asPolyline()]).contains(QgsGeometry.fromPolygon([innerBuffer.asPolyline()])):
                        poly.append(innerBuffer.asPolyline())
                if innerRings:
                    for inner in innerRings:
                        if QgsGeometry.fromPolygon([poly[0]]).contains(QgsGeometry.fromPolygon([inner.asPolyline()])):
                            bufferInner = self.buffering(inner, bufferSize, segments)
                            innerBufferInnerRing = self.getInnerRing(bufferInner, 0)
                            if innerBufferInnerRing:
                                for allin in innerBufferInnerRing:
                                    if QgsGeometry.fromPolygon([inner.asPolyline()]).contains(
                                            QgsGeometry.fromPolygon([allin.asPolyline()])):
                                        poly.append(allin.asPolyline())
                    polygon = QgsGeometry.fromPolygon(poly)
                else:
                    polygon = QgsGeometry.fromPolygon(poly)
            outFeat = QgsFeature()
            outFeat.setGeometry(polygon)
            # else:
            #    outFeat = inFeat
            return outFeat

    def dillateErode(self, layer, bufferSize, segments, DPtolerance, layerName):
        #dillation
        simp = self.multiToSingle(layer)
        vl = QgsVectorLayer("Polygon?crs=EPSG:2180", "dillate1", "memory")
        vl.startEditing()
        tempGeom = QgsGeometry()
        first = True
        for feature in simp.getFeatures():
            QgsMessageLog.logMessage(str(feature.geometry().asPolygon()))
            poly = self.dillation(feature, bufferSize, segments)
            if poly is not None:
                if first:
                    tempGeom = QgsGeometry(poly.geometry())
                    first = False
                else:
                    tempGeom = tempGeom.combine(poly.geometry())

        outFeat = QgsFeature()
        outFeat.setGeometry(tempGeom)
        vl.addFeature(outFeat)
        vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)

        #erosion
        self.multiToSingle(vl)
        polygons = []
        vl2 = QgsVectorLayer("Polygon?crs=EPSG:2180", "erode1", "memory")
        vl2.startEditing()
        for feature in vl.getFeatures():
            poly = self.erosion(feature, bufferSize, segments)
            if poly is not None:
                polygons.append(QgsFeature(poly))
        vl2.addFeatures(polygons, False)
        vl2.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl2)
        rdp = SimplifyGeometries()
        simplify = rdp.processAlgorithm(vl2, DPtolerance, layerName)

        return simplify

    def erodeDillate(self, layer, bufferSize, segments, DPtolerance, layerName):
        # erosion
        self.multiToSingle(layer)
        polygons = []
        vl3 = QgsVectorLayer("Polygon?crs=EPSG:2180", "erode2", "memory")
        vl3.startEditing()
        tempGeom = QgsGeometry()

        for feature in layer.getFeatures():
            poly = self.erosionWithInnerRings(feature, bufferSize, segments)
            if poly is not None:
                polygons.append(QgsFeature(poly))
        vl3.addFeatures(polygons, False)
        vl3.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl3)

        rdp = SimplifyGeometries()
        simplify = rdp.processAlgorithm(vl3, DPtolerance, "simply2")
        QgsMapLayerRegistry.instance().addMapLayer(simplify)

        # dillation
        self.multiToSingle(simplify)
        polygons = []
        vl4 = QgsVectorLayer("Polygon?crs=EPSG:2180", layerName, "memory")
        vl4.startEditing()
        first = True
        for feature in simplify.getFeatures():
            poly = self.dillationWithInnerRings(feature, bufferSize, segments)
            if poly is not None:
                if first:
                    tempGeom = QgsGeometry(poly.geometry())
                    first = False
                else:
                    tempGeom = tempGeom.combine(poly.geometry())
                    #polygons.append(QgsFeature(poly))
        outFeat = QgsFeature()
        outFeat.setGeometry(tempGeom)
        vl4.addFeature(outFeat)
        self.multiToSingle(vl4)
        #vl.addFeatures(polygons, False)
        vl4.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl4)
        return vl4

    def multiToSingle(self, layer):
        layer.startEditing()
        remove_list = []
        for feature in layer.getFeatures():
            geom = feature.geometry()
            # check if feature geometry is multipart
            if geom.isMultipart():
                remove_list.append(feature.id())
                QgsMessageLog.logMessage(str(remove_list))
                new_features = []
                temp_feature = QgsFeature(feature)
                # create a new feature using the geometry of each part
                for part in geom.asGeometryCollection():
                    temp_feature.setGeometry(part)
                    new_features.append(QgsFeature(temp_feature))
                # add new features to layer
                layer.addFeatures(new_features, False)
        # remove the original (multipart) features from layer
        if len(remove_list) > 0:
            for id in remove_list:
                layer.deleteFeature(id)
        layer.commitChanges()
        iface.mapCanvas().refresh()
        return layer

    def morph(self, layer, bufferSize, segments, DPtolerance, layerName):
        # dillation
        simp = self.multiToSingle(layer)
        vl = QgsVectorLayer("Polygon?crs=EPSG:2180", "dillate1", "memory")
        vl.startEditing()
        tempGeom = QgsGeometry()
        first = True
        for feature in simp.getFeatures():
            poly = feature.geometry().buffer(bufferSize, segments)
            if poly is not None:
                if first:
                    tempGeom = QgsGeometry(poly)
                    first = False
                else:
                    tempGeom = tempGeom.combine(poly)
        outFeat = QgsFeature()
        outFeat.setGeometry(tempGeom)
        vl.addFeature(outFeat)
        vl.commitChanges()
        #QgsMapLayerRegistry.instance().addMapLayer(vl)
        # erosion
        self.multiToSingle(vl)
        polygons = []
        outFeat = QgsFeature()

        vl2 = QgsVectorLayer("Polygon?crs=EPSG:2180", "erode1", "memory")
        vl2.startEditing()
        for feature in vl.getFeatures():
            poly = feature.geometry().buffer(-bufferSize, segments)
            outFeat.setGeometry(poly)
            vl2.addFeature(outFeat)
        vl2.commitChanges()
        rdp = SimplifyGeometries()
        simplify = rdp.processAlgorithm(vl2, DPtolerance, layerName)
        return simplify


