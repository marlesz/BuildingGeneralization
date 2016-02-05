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


class BUBD_A:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy

    def wyborWarstwy(self):
        rejestr = QgsMapLayerRegistry.instance()
        warstwa = rejestr.mapLayersByName(self.nazwaWarstwy)[0]
        iface.setActiveLayer(warstwa)
        return warstwa

    def budynekMieszkalnySkala(self):
        #rejestr = QgsMapLayerRegistry.instance()
        #warstwa = rejestr.mapLayersByName(nazwaWarstwy)[0]
        #iface.setActiveLayer(warstwa)
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #objects = layer.getFeatures( QgsFeatureRequest( expr ) )
        ids = [i.id() for i in obiekty]
        warstwa.setSelectedFeatures( ids )
        return obiekty

    def budynekUzytecznosciPublicznejSkala(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os','1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni <> 'Zns' AND  geometria1 >=500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        ids = [i.id() for i in obiekty]
        warstwa.setSelectedFeatures( ids )
        return obiekty

    def budynekPrzemyslowySkala(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression(" funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        return obiekty


    def budynekGospodarczySkala(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def szklarniaSkala(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("funSzczego='1271.Sz' AND x_katIstni<>'Zns' AND geometria1>=2500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def budynekMieszkalnySymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND geometria1<500")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def budynekUzytecznosciPublicznejSymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os', '1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>=200")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def budynekPrzemyslowySymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def budynekGospodarczySymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def ruinaSymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("(x_katIstni='Zns' AND geometria1>=600) OR (x_katIstni='Zns' AND zabytek = 1)")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def swiatyniaChrzescijanskaSymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.Ck', '1272.Ks') AND x_katIstni<>'Zns' ")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def swiatyniaNiechrzescijanskaSymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.IR', '1272.Mc', '1272.Sn') AND x_katIstni<>'Zns' ")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty

    def kaplicaSymbol(self):
        warstwa = self.wyborWarstwy()
        QgsMessageLog.logMessage(str(warstwa.name()))
        expr = QgsExpression("funSzczego ='1272.Kp' AND x_katIstni<>'Zns' ")
        expr.prepare(warstwa.pendingFields())
        obiekty = filter(expr.evaluate, warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return obiekty