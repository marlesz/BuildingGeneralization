from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from WarstwaOperacje import *
"""class Warstwa:
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

    def utworzNowaWartswe(self, warstwa, typ, obiekty, nowaNazwaWarstwy):
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

class CentroidPoligonu:

    def centroidPoligonu(self, warstwa):
        iface.setActiveLayer(warstwa)

        provider = warstwa.dataProvider()
        fields = provider.fields()
        outputLayer = QgsVectorLayer("Point?crs=EPSG:2180", "Punkt" + warstwa.name(), "memory")
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
        return outputLayer"""


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
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekMieszkalnySkala")

    def budynekUzytecznosciPublicznejSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os','1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni <> 'Zns' AND  geometria1 >=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekUzytecznosciPublicznejSkala")

    def budynekPrzemyslowySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekGospodarczySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekGospodarczySkala")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego='1271.Sz' AND x_katIstni<>'Zns' AND geometria1>=2500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "szklarniaSkala")

    def budynekMieszkalnySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND geometria1<500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekMieszkalnySymbol")

    def budynekUzytecznosciPublicznejSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os', '1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>=200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekUzytecznosciPublicznejSymbol")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funOgolnaB = '1251' AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySymbol")

    def budynekGospodarczySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekGospodarczySymbol")

    def ruinaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(x_katIstni='Zns' AND geometria1>=600) OR (x_katIstni='Zns' AND zabytek = 1)")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "ruinaSymbol")

    def swiatyniaChrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.Ck', '1272.Ks') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "swiatyniaChrzescijanskaSymbol")

    def swiatyniaNiechrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.IR', '1272.Mc', '1272.Sn') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "swiatyniaNiechrzescijanskaSymbol")

    def kaplicaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego ='1272.Kp' AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "kaplicaSymbol")

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
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "ruinaSymbol")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Skl' AND geometria1>=2500 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "szklarniaSkala")

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
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Ckm' AND x_katIstni<>'Zns' AND geometria1<500 AND geometria1>200 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySymbol")

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
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaWielorodzinnaZwarta")

    def zabudowaWielorodzinnaGesta(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Wld' AND charakter='Gst' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaWielorodzinnaGesta")

    def zabudowaJednorodzinna(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Jrd' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        #ids = [i.id() for i in obiekty]
        #warstwa.setSelectedFeatures( ids )
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaJednorodzinna")


class SKDR_L:

    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_SKDR_L')

    def autostrada(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "autostrada")

    def autostradawBudowie(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Bud' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "autostradawBudowie")

    def drogaEkspresowaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND liczbaJez >=2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaEkspresowaDwujezdniowa")

    def drogaEkspresowaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND liczbaJez =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaEkspresowaJednojezdniowa")

    def drogaEkspresowawBudowie(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND x_katIstni = 'Bud' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaEkspresowawBudowie")

    def drogaGlownaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'G' AND liczbaJez >=2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaGlownaDwujezdniowa")

    def drogaGlownaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'G' AND liczbaJez =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaGlownaJednojezdniowa")

    def drogaZbiorczaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND liczbaJez =2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaZbiorczaDwujezdniowa")

    def drogaZbiorczaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNaw IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND liczbaJez =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaZbiorczaJednojezdniowa")

    def drogaLokalnaTwarda(self):
        expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaLokalnaTwarda")

    def drogaLokalnaUtwardzona(self):
        expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Pb', 'Tl', 'Zw') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaLokalnaUtwardzona")

    def drogaLokalnaGruntowa(self):
        expr = QgsExpression("klasaDrogi = 'L' AND materialNa IN ('Gr', 'Gz') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaLokalnaGruntowa")

    def drogaDojazdowa(self):
        expr = QgsExpression("klasaDrogi IN ('D', 'I') AND materialNaw IN ('Gr', 'Gz') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG'  ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "drogaDojazdowa")

class SKJZ_L:

    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_SKJZ_L')

    def jezdniaAutostrady(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "jezdniaAutostrady")

    def jezdniadrogiEkspresowej(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "jezdniadrogiEkspresowej")

    def jezdniaDrogiGlownejSymbol(self):
        expr = QgsExpression("klasaDrogi = 'G' AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "jezdniaDrogiGlownejSymbol")

    def jezdniaDrogiZbiorczejSymbol(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "jezdniaDrogiZbiorczej")

class SKRP_L:

    nowaWarstwa = Warstwa()
    warstwa = nowaWarstwa.wyborWarstwy('OT_SKRP_L')

    def alejkaPasazSymbol(self):
        expr = QgsExpression("(klasaCiagu = 'Ap' AND szerokosc >= 5) OR klasaCiagu = 'Pm' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "alejkaPasazSymbol")

    def sciezka(self):
        expr = QgsExpression("klasaCiagu= 'Sc' OR (klasaCiagu = 'Ap' AND szerokosc < 5) ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        QgsMessageLog.logMessage(str(len(obiekty)))
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Line",obiekty, "sciezka")
        
"""build =BUBD_A()
build.budynekMieszkalnySkala()
build.budynekUzytecznosciPublicznejSkala()
build.budynekPrzemyslowySkala()
build.budynekGospodarczySkala()
build.szklarniaSkala()
build.budynekMieszkalnySymbol()
build.budynekUzytecznosciPublicznejSymbol()
build.budynekPrzemyslowySymbol()
build.budynekGospodarczySymbol()
build.ruinaSymbol()
build.swiatyniaChrzescijanskaSymbol()
build.swiatyniaNiechrzescijanskaSymbol()
build.kaplicaSymbol()
oior = OIOR_A()
oior.ruinaSymbol()
oior.szklarniaSkala()
buwt = BUWT_A()
buwt.budynekPrzemyslowySkala()
buwt.budynekPrzemyslowySymbol()
ptzb = PTZB_A()
ptzb.zabudowaJednorodzinna()
ptzb.zabudowaWielorodzinnaGesta()
ptzb.zabudowaWielorodzinnaZwarta()
warstwa = Warstwa()
warstwa.polaczWarstwy("Polygon", "szklarniaSkala2",build.szklarniaSkala(), oior.szklarniaSkala())
warstwa.polaczWarstwy("Polygon", "ruinaSymbol2",build.ruinaSymbol(), oior.ruinaSymbol())
warstwa.polaczWarstwy("Polygon", "budynekPrzemyslowySkala2", build.budynekPrzemyslowySkala(), buwt.budynekPrzemyslowySkala() )
warstwa.polaczWarstwy("Polygon", "budynekPrzemyslowySymbol2", build.budynekPrzemyslowySymbol(), buwt.budynekPrzemyslowySymbol() )"""
        
        
        