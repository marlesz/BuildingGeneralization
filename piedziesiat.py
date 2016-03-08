from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
import sys
from PyQt4 import QtCore, QtGui
import os.path
import glob
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from building_generalization_dialog import GeneralizationDialog
import os.path
import osgeo.ogr as ogr

class Warstwa:
    #def __init__(self, nazwaWarstwy):
        #self.nazwaWarstwy = nazwaWarstwy

    def wyborWarstwy(self, nazwaWarstwy):
        rejestr = QgsMapLayerRegistry.instance()
        try:
            warstwa = rejestr.mapLayersByName(nazwaWarstwy)[0]
            iface.setActiveLayer(warstwa)
        except IndexError:
            iface.messageBar().pushMessage("Error", "Wczytaj warstwe " + nazwaWarstwy, level=QgsMessageBar.CRITICAL)
        return warstwa

    def utworzNowaWartswe(self, nazwaWarstwy, typ, obiekty, nowaNazwaWarstwy):
        warstwa = self.wyborWarstwy(nazwaWarstwy)
        provider = warstwa.dataProvider()
        fields = provider.fields()
        outputLayer = QgsVectorLayer(typ+"?crs=EPSG:2180", nowaNazwaWarstwy, "memory")
        outputLayer.startEditing()
        for field in fields:
            outputLayer.addAttribute(field)
        outputLayer.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)
        outFeat = QgsFeature()
        for feature in obiekty:
            outFeat.setGeometry(feature.geometry())
            outFeat.setAttributes(feature.attributes())
            outputLayer.dataProvider().addFeatures([outFeat])
            outputLayer.updateExtents()
            outputLayer.updateFields()
        return outputLayer
        """warstwa = self.wyborWarstwy()
        fields = warstwa.pendingFields()
        outputLayer = QgsVectorLayer(typ+"?crs=EPSG:2180", nowaNazwaWarstwy, "memory")
        provider = outputLayer.dataProvider()
        for field in fields:
            provider.addAttributes([field])
            outputLayer.updateFields()
            feats1 = warstwa.getFeatures()
            for feature in feats1:
                provider.addFeatures([feature])
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)
        outputLayer.updateExtents()
        return outputLayer"""

#class LaczenieWarstw:
    """def polaczWarstwy(self,typ, nowaNazwaWarstwy, *nazwyWarstw):
        rejestr = QgsMapLayerRegistry.instance()

        outputLayer = QgsVectorLayer(typ+"?crs=EPSG:2180", nowaNazwaWarstwy, "memory")
        provider = outputLayer.dataProvider()


        for nazwaWarstwy in nazwyWarstw:
            QgsMessageLog.logMessage(str(nazwaWarstwy))
            warstwa = rejestr.mapLayersByName(nazwaWarstwy)[0]
            fields = warstwa.pendingFields()
            for field in fields:
                provider.addAttributes([field])
            outputLayer.updateFields()

            feats1 = warstwa.getFeatures()
            for feature in feats1:
                provider.addFeatures([feature])
                #outputLayer.updateExtents()
                outputLayer.updateFields()
            self.usunWarstwe(nazwaWarstwy)
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)
        outputLayer.updateExtents()"""
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
                #outputLayer.updateExtents()
                outputLayer.updateFields()
            self.usunWarstwe(warstwa)
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)
        outputLayer.updateExtents()

    def usunWarstwe(self, warstwa):
        #warstwa = self.wyborWarstwy(nazwaWarstwy)
        QgsMapLayerRegistry.instance().removeMapLayers([warstwa.id()])

class BUBD_A:
    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_BUBD_A')
    def budynekMieszkalnySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #self.warstwa.setSelectedFeatures( ids )
        #return obiekty
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "budynekMieszkalnySkala")

    def budynekUzytecznosciPublicznejSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os','1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni <> 'Zns' AND  geometria1 >=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "budynekUzytecznosciPublicznejSkala")

    def budynekPrzemyslowySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekGospodarczySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "budynekGospodarczySkala")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego='1271.Sz' AND x_katIstni<>'Zns' AND geometria1>=2500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "szklarniaSkala")

    def budynekMieszkalnySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND geometria1<500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "budynekMieszkalnySymbol")

    def budynekUzytecznosciPublicznejSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os', '1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>=200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "budynekUzytecznosciPublicznejSymbol")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "budynekPrzemyslowySymbol")

    def budynekGospodarczySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "budynekGospodarczySymbol")

    def ruinaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(x_katIstni='Zns' AND geometria1>=600) OR (x_katIstni='Zns' AND zabytek = 1)")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(),"Polygon",obiekty, "ruinaSymbol")

    def swiatyniaChrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.Ck', '1272.Ks') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "swiatyniaChrzescijanskaSymbol")

    def swiatyniaNiechrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.IR', '1272.Mc', '1272.Sn') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "swiatyniaNiechrzescijanskaSymbol")

    def kaplicaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego ='1272.Kp' AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "kaplicaSymbol")

class OIOR_A:
    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_OIOR_A')
    def ruinaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Rzb' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "ruinaSymbol")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Skl' AND geometria1>=2500 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "szklarniaSkala")

class BUWT_A:
    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_BUWT_A')

    def budynekPrzemyslowySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Ckm' AND x_katIstni<>'Zns' AND geometria1>=500 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Ckm' AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "budynekPrzemyslowySymbol")

class PTZB_A:

    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_PTZB_A')

    def zabudowaWielorodzinnaZwarta(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Wld' AND charakter='Zwr' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "zabudowaWielorodzinnaZwarta")

    def zabudowaWielorodzinnaGesta(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Wld' AND charakter='Gst' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "zabudowaWielorodzinnaGesta")

    def zabudowaJednorodzinna(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Jrd' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa.name(), "Polygon",obiekty, "zabudowaJednorodzinna")


class CentroidPoligonu:

    def centroidPoligonu(self, nazwaWarstwy):
        rejestr = QgsMapLayerRegistry.instance()
        warstwa = rejestr.mapLayersByName(nazwaWarstwy)[0]
        iface.setActiveLayer(warstwa)

        provider = warstwa.dataProvider()
        fields = provider.fields()
        outputLayer = QgsVectorLayer("Point?crs=EPSG:2180", "Punkt" + nazwaWarstwy, "memory")
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

            #writer = QgsVectorFileWriter(outputFilename, "CP1250", fields, provider.geometryType(), provider.crs(), "ESRI Shapefile")


