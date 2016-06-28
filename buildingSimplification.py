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

class BuildingSimplification(Warstwa):
    def simplify(self):
        build = BUBD_A("OT_BUBD_A")
        budynekMieszkalnySkala = build.budynekMieszkalnySkala()
        budynekUzytecznosciPublicznejSkala = build.budynekUzytecznosciPublicznejSkala()
        budynekPrzemyslowySkala = build.budynekPrzemyslowySkala()
        budynekGospodarczySkala = build.budynekGospodarczySkala()
        szklarniaSkala = build.szklarniaSkala()
        budynekMieszkalnySymbol = build.budynekMieszkalnySymbol()
        budynekUzytecznosciPublicznejSymbol = build.budynekUzytecznosciPublicznejSymbol()
        budynekPrzemyslowySymbol = build.budynekPrzemyslowySymbol()
        budynekGospodarczySymbol = build.budynekGospodarczySymbol()
        ruinaSymbol = build.ruinaSymbol()
        swiatyniaChrzescijanskaSymbol = build.swiatyniaChrzescijanskaSymbol()
        swiatyniaNiechrzescijanskaSymbol = build.swiatyniaNiechrzescijanskaSymbol()
        kaplicaSymbol = build.kaplicaSymbol()

        oior = OIOR_A("OT_OIOR_A")
        ruinaSymbolO = oior.ruinaSymbol()
        szklarniaSkalaO = oior.szklarniaSkala()

        buwt = BUWT_A("OT_BUWT_A")
        budynekPrzemyslowySkalaB = buwt.budynekPrzemyslowySkala()
        budynekPrzemyslowySymbolB = buwt.budynekPrzemyslowySymbol()

        ruinaSymbol = self.polaczWarstwy("Polygon", "ruinaSymbol", ruinaSymbol, ruinaSymbolO)
        szklarniaSkala = self.polaczWarstwy("Polygon", "szklarniaSkala", szklarniaSkala, szklarniaSkalaO)
        budynekPrzemyslowySkala = self.polaczWarstwy("Polygon", "budynekPrzemyslowySkala", budynekPrzemyslowySkala, budynekPrzemyslowySkalaB)
        budynekPrzemyslowySymbol = self.polaczWarstwy("Polygon", "budynekPrzemyslowySymbol", budynekPrzemyslowySymbol, budynekPrzemyslowySymbolB)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekMieszkalnySkala)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekMieszkalnySymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekUzytecznosciPublicznejSkala)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekUzytecznosciPublicznejSymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekPrzemyslowySkala)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekPrzemyslowySymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekGospodarczySkala)
        # QgsMapLayerRegistry.instance().addMapLayer(budynekGospodarczySymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(ruinaSymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(swiatyniaChrzescijanskaSymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(swiatyniaNiechrzescijanskaSymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(kaplicaSymbol)
        # QgsMapLayerRegistry.instance().addMapLayer(szklarniaSkala)

        buildingArea = self.polaczWarstwy("Polygon", "zabudowa", self.wyborWarstwy("zabudowaWielorodzinnaGesta"), self.wyborWarstwy("zabudowaWielorodzinnaZwarta"), self.wyborWarstwy("zabudowaJednorodzinna"))

        budynekMieszkalnySkala.startEditing()
        for build in budynekMieszkalnySkala.getFeatures():
            for area in buildingArea.getFeatures():
                if build.geometry().intersects(area.geometry()):
                    budynekMieszkalnySkala.deleteFeature(build.id())
                    break
        budynekMieszkalnySkala.commitChanges()

        budynekMieszkalnySymbol.startEditing()
        for build in budynekMieszkalnySymbol.getFeatures():
            for area in buildingArea.getFeatures():
                if build.geometry().intersects(area.geometry()):
                    budynekMieszkalnySymbol.deleteFeature(build.id())
                    break
        budynekMieszkalnySymbol.commitChanges()

        #uproszczenie
        # dp = SimplifyGeometries()
        # if budynekMieszkalnySkala.featureCount()>0:
        #     budynekMieszkalnySkala = dp.processAlgorithm(budynekMieszkalnySkala, 7.5, "budynekMieszkalnySkala")
        # if budynekUzytecznosciPublicznejSkala.featureCount()>0:
        #     budynekUzytecznosciPublicznejSkala = dp.processAlgorithm(budynekUzytecznosciPublicznejSkala, 7.5, "budynekUzytecznosciPublicznejSkala")
        # if budynekPrzemyslowySkala.featureCount()>0:
        #     budynekPrzemyslowySkala = dp.processAlgorithm(budynekPrzemyslowySkala, 7.5, "budynekPrzemyslowySkala")
        # if budynekGospodarczySkala.featureCount()>0:
        #     budynekGospodarczySkala = dp.processAlgorithm(budynekGospodarczySkala, 7.5, "budynekGospodarczySkala")
        # if szklarniaSkala.featureCount()>0:
        #     szklarniaSkala = dp.processAlgorithm(szklarniaSkala, 7.5, "szklarniaSkala")

        ombb = OrientedMinimumBoundingBox()
        if budynekMieszkalnySkala.featureCount()>0:
            budynekMieszkalnySkala = ombb.featureOmbb2(budynekMieszkalnySkala, "budynekMieszkalnySkala", "Polygon")
        if budynekUzytecznosciPublicznejSkala.featureCount()>0:
            budynekUzytecznosciPublicznejSkala = ombb.featureOmbb2(budynekUzytecznosciPublicznejSkala, "budynekUzytecznosciPublicznejSkala", "Polygon")
        if budynekPrzemyslowySkala.featureCount()>0:
            budynekPrzemyslowySkala = ombb.featureOmbb2(budynekPrzemyslowySkala, "budynekPrzemyslowySkala", "Polygon")
        if budynekGospodarczySkala.featureCount()>0:
            budynekGospodarczySkala = ombb.featureOmbb2(budynekGospodarczySkala, "budynekGospodarczySkala", "Polygon")
        if szklarniaSkala.featureCount()>0:
            szklarniaSkala = ombb.featureOmbb2(szklarniaSkala, "szklarniaSkala", "Polygon")

        #nadanie atrybutu orientacji symbolom
        budynekMieszkalnySymbol.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        budynekMieszkalnySymbol.updateFields()
        budynekUzytecznosciPublicznejSymbol.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        budynekUzytecznosciPublicznejSymbol.updateFields()
        budynekPrzemyslowySymbol.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        budynekPrzemyslowySymbol.updateFields()
        budynekGospodarczySymbol.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        budynekGospodarczySymbol.updateFields()
        ruinaSymbol.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        ruinaSymbol.updateFields()
        indorient = budynekMieszkalnySymbol.fieldNameIndex("orientacja")
        list = [budynekMieszkalnySymbol, budynekUzytecznosciPublicznejSymbol, budynekPrzemyslowySymbol, budynekGospodarczySymbol, ruinaSymbol]
        for lyr in list:
            lyr.startEditing()
            for inFeat in lyr.getFeatures():
                geometry, area, perim, angle, width, height = ombb.OMBBox(inFeat.geometry())
                lyr.changeAttributeValue(inFeat.id(), indorient, angle)
            lyr.commitChanges()

        #poligony na punkty
        centroid = CentroidPoligonu()
        budynekMieszkalnySymbol = centroid.centroidPoligonu(budynekMieszkalnySymbol)
        budynekUzytecznosciPublicznejSymbol = centroid.centroidPoligonu(budynekUzytecznosciPublicznejSymbol)
        budynekPrzemyslowySymbol = centroid.centroidPoligonu(budynekPrzemyslowySymbol)
        budynekGospodarczySymbol = centroid.centroidPoligonu(budynekGospodarczySymbol)
        ruinaSymbol = centroid.centroidPoligonu(ruinaSymbol)
        swiatyniaChrzescijanskaSymbol = centroid.centroidPoligonu(swiatyniaChrzescijanskaSymbol)
        swiatyniaNiechrzescijanskaSymbol = centroid.centroidPoligonu(swiatyniaNiechrzescijanskaSymbol)
        kaplicaSymbol = centroid.centroidPoligonu(kaplicaSymbol)

        QgsMapLayerRegistry.instance().addMapLayer(budynekMieszkalnySkala)
        QgsMapLayerRegistry.instance().addMapLayer(budynekMieszkalnySymbol)
        QgsMapLayerRegistry.instance().addMapLayer(budynekUzytecznosciPublicznejSkala)
        QgsMapLayerRegistry.instance().addMapLayer(budynekUzytecznosciPublicznejSymbol)
        QgsMapLayerRegistry.instance().addMapLayer(budynekPrzemyslowySkala)
        QgsMapLayerRegistry.instance().addMapLayer(budynekPrzemyslowySymbol)
        QgsMapLayerRegistry.instance().addMapLayer(budynekGospodarczySkala)
        QgsMapLayerRegistry.instance().addMapLayer(budynekGospodarczySymbol)
        QgsMapLayerRegistry.instance().addMapLayer(ruinaSymbol)
        QgsMapLayerRegistry.instance().addMapLayer(swiatyniaChrzescijanskaSymbol)
        QgsMapLayerRegistry.instance().addMapLayer(swiatyniaNiechrzescijanskaSymbol)
        QgsMapLayerRegistry.instance().addMapLayer(kaplicaSymbol)
        QgsMapLayerRegistry.instance().addMapLayer(szklarniaSkala)

        style_path = "/home/ml/.qgis2/python/plugins/Generalization/style/"
        qml_path = style_path + "budynekMieszkalnySkala.qml"
        budynekMieszkalnySkala.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekMieszkalnySymbol.qml"
        budynekMieszkalnySymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekUzytecznosciPublicznejSkala.qml"
        budynekUzytecznosciPublicznejSkala.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekUzytecznosciPublicznejSymbol.qml"
        budynekUzytecznosciPublicznejSymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekPrzemyslowySkala.qml"
        budynekPrzemyslowySkala.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekPrzemyslowySymbol.qml"
        budynekPrzemyslowySymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekGospodarczySkala.qml"
        budynekGospodarczySkala.loadNamedStyle(qml_path)
        qml_path = style_path + "budynekGospodarczySymbol.qml"
        budynekGospodarczySymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "ruinaSymbol.qml"
        ruinaSymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "swiatyniaChrzescijanskaSymbol.qml"
        swiatyniaChrzescijanskaSymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "swiatyniaNiechrzescijanskaSymbol.qml"
        swiatyniaNiechrzescijanskaSymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "kaplicaSymbol.qml"
        kaplicaSymbol.loadNamedStyle(qml_path)
        qml_path = style_path + "szklarniaSkala.qml"
        szklarniaSkala.loadNamedStyle(qml_path)