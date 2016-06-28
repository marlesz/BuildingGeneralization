from WarstwaOperacje import *
import processing
from qgis.utils import *
from PyQt4.QtCore import QVariant
from selekcja50k import *
from simplification import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion
from PyQt4.QtGui import QAction, QIcon
from math import degrees, atan2
from RDP import *
from PyQt4.QtCore import QVariant
from Morphology import *

class BuildingsAreaSimplification(Warstwa):
    def simplify(self):

        ptzb = PTZB_A('OT_PTZB_A')
        zabudowaJednorodzinna = ptzb.zabudowaJednorodzinna()
        zabudowaWielorodzinnaGesta = ptzb.zabudowaWielorodzinnaGesta()
        zabudowaWielorodzinnaZwarta = ptzb.zabudowaWielorodzinnaZwarta()
        # QgsMapLayerRegistry.instance().addMapLayer(zabudowaJednorodzinna)
        # QgsMapLayerRegistry.instance().addMapLayer(zabudowaWielorodzinnaZwarta)
        # QgsMapLayerRegistry.instance().addMapLayer(zabudowaWielorodzinnaGesta)

        # morph = Morphology()
        morph = Morphology()
        dp = SimplifyGeometries()
        ombb = OrientedMinimumBoundingBox()
        simp = Simplification()

        # zabudowa wielorodzinna gesta
        if zabudowaWielorodzinnaGesta.featureCount()>0:
            # agregacja
            agrGesta = morph.morph(zabudowaWielorodzinnaGesta, 10, 2, 1, "zabudowaWielorodzinnaGestaagr")
            # zalamania - Douglas-Peucker
            rdpGesta = dp.processAlgorithm(agrGesta, 15, "zabudowaWielorodzinnaGestadp")
            # usuwanie malych obszarow
            ids = ombb.featureOmbb(rdpGesta, 30, 30)
            rdpGesta.startEditing()
            for fid in ids:
                rdpGesta.deleteFeature(fid)
            rdpGesta.commitChanges()
            # wypelnianie enklaw
            generalizeGesta = simp.fillHoles(rdpGesta, 30, 30, "zabudowaWielorodzinnaGesta")
            QgsMapLayerRegistry.instance().addMapLayer(generalizeGesta)

        # zabudowa wielorodzinna zwarta
        if zabudowaWielorodzinnaZwarta.featureCount()>0:
            # agregacja
            agregationZwarta = morph.morph(zabudowaWielorodzinnaZwarta, 10, 2, 1, "zabudowaWielorodzinnaZwartaagr")
            # zalamania - Douglas-Peucker
            rdpZwarta = dp.processAlgorithm(agregationZwarta, 15, "zabudowaWielorodzinnaZwartadp")
            # usuwanie malych obszarow
            ids = ombb.featureOmbb(rdpZwarta, 30, 30)
            rdpZwarta.startEditing()
            for fid in ids:
                rdpZwarta.deleteFeature(fid)
            rdpZwarta.commitChanges()
            # wypelnianie enklaw
            generalizeZwarta = simp.fillHoles(rdpZwarta, 30, 30, "zabudowaWielorodzinnaZwarta")
            QgsMapLayerRegistry.instance().addMapLayer(generalizeZwarta)

        # zabudowa jednorodzinna
        if zabudowaWielorodzinnaZwarta.featureCount()>0:
            # agregacja
            agregationJedno = morph.morph(zabudowaJednorodzinna, 10, 2, 1, "zabudowaJednorodzinnaagr")
            # zalamania - Douglas-Peucker
            rdpJedno = dp.processAlgorithm(agregationJedno, 15, "zabudowaJednorodzinna")
            #  usuwanie malych obszarow
            ids = ombb.featureOmbb(rdpJedno, 30, 30)
            rdpJedno.startEditing()
            for fid in ids:
                rdpJedno.deleteFeature(fid)
            rdpJedno.commitChanges()
            # wypelnianie enklaw
            generalizeJedno = simp.fillHoles(rdpJedno, 30, 30, "zabudowaJednorodzinna")
            QgsMapLayerRegistry.instance().addMapLayer(generalizeJedno)

        style_path = "/home/ml/.qgis2/python/plugins/Generalization/style/"
        qml_path = style_path + "zabudowaJednorodzinna.qml"
        generalizeJedno.loadNamedStyle(qml_path)
        qml_path = style_path + "zabudowaWielorodzinnaGesta.qml"
        generalizeGesta.loadNamedStyle(qml_path)
        qml_path = style_path + "zabudowaWielorodzinnaZwarta.qml"
        generalizeZwarta.loadNamedStyle(qml_path)