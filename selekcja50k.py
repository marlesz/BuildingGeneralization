# -*- coding: utf-8 -*-

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from WarstwaOperacje import *

class BUBD_A:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)


    def budynekMieszkalnySkala(self):

        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND $area>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekMieszkalnySkala")

    def budynekUzytecznosciPublicznejSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" (funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os','1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni <> 'Zns' AND  $area >=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekUzytecznosciPublicznejSkala")

    def budynekPrzemyslowySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression(" funOgolnaB = '1251' AND x_katIstni<>'Zns' AND $area>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekGospodarczySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND $area>=500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekGospodarczySkala")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego='1271.Sz' AND x_katIstni<>'Zns' AND $area>=2500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "szklarniaSkala")

    def budynekMieszkalnySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1121','1122') OR funSzczego IN ('1110.Dj', '1110.Dl', '1130.Dz', '1130.Kl', '1130.Km')) AND x_katIstni<>'Zns' AND $area<500")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "budynekMieszkalnySymbol")

    def budynekUzytecznosciPublicznejSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB IN ('1211', '1212', '1220', '1230', '1261', '1262', '1263', '1264', '1265') OR funSzczego IN ('1110.Ls', '1130.Bs', '1130.Db', '1330.Dd', '1130.Os', '1130.Dp', '1130.Ds', '1130.Hr', '1130.In', '1130.Po', '1130.Ra', '1130.Rb', '1130.Rp', '1130.Zk', '1130.Zp', '1241.Da', '1241.Dk', '1241.Dl', '1241.Kg', '1241.Tp', '1242.Pw', '1272.Bc', '1272.Dp', '1272.Kr', '1274.As', '1274.Sc', '1274.Tp')) AND x_katIstni<>'Zns' AND $area<500 AND $area>=200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekUzytecznosciPublicznejSymbol")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funOgolnaB = '1251' AND x_katIstni<>'Zns' AND $area<500 AND $area>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySymbol")

    def budynekGospodarczySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(funOgolnaB='1252' OR funSzczego IN ('1241.Kk', '1241.Kp', '1241.Ct', '1241.Hg', '1241.Lk', '1241.Rt', '1241.Ab' ,'1241.Tr', '1241.Tb', '1242.Gr', '1271.Bg', '1271.Bp', '1271.St', '1272.Dz', '1273.Zb', '1274.Bc', '1274.Sg', '1274.Sp', '1274.St', '1274.Zk', '1274.Zp')) AND x_katIstni<>'Zns' AND $area<500 AND $area>200")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekGospodarczySymbol")

    def ruinaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("(x_katIstni='Zns' AND geometria1>=600) OR (x_katIstni='Zns' AND zabytek = 1)")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa,"Polygon",obiekty, "ruinaSymbol")

    def swiatyniaChrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.Ck', '1272.Ks') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "swiatyniaChrzescijanskaSymbol")

    def swiatyniaNiechrzescijanskaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego IN ('1272.IR', '1272.Mc', '1272.Sn') AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "swiatyniaNiechrzescijanskaSymbol")

    def kaplicaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("funSzczego ='1272.Kp' AND x_katIstni<>'Zns' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "kaplicaSymbol")

class OIOR_A:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)

    def ruinaSymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Rzb' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "ruinaSymbol")

    def szklarniaSkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Skl' AND $area>=2500 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "szklarniaSkala")

class BUWT_A:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)

    def budynekPrzemyslowySkala(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Ckm' AND x_katIstni<>'Zns' AND $area>=500 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySkala")

    def budynekPrzemyslowySymbol(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Ckm' AND x_katIstni<>'Zns' AND $area<500 AND $area>200 ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "budynekPrzemyslowySymbol")

class PTZB_A(Warstwa):
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)

    def zabudowaWielorodzinnaZwarta(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Wld' AND charakter='Zwr' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaWielorodzinnaZwarta")

    def zabudowaWielorodzinnaGesta(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Wld' AND charakter='Gst' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaWielorodzinnaGesta")

    def zabudowaJednorodzinna(self):
        QgsMessageLog.logMessage(str(self.warstwa.name()))
        expr = QgsExpression("rodzaj='Jrd' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "Polygon",obiekty, "zabudowaJednorodzinna")


class SKDR_L:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)

    def autostrada(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Eks' AND x_rodzajRe IN ('OG', 'LU') ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "autostrada")

    def autostradawBudowie(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Bud' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "autostradawBudowie")

    def drogaEkspresowaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND liczbaJezd >=2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaEkspresowaDwujezdniowa")

    def drogaEkspresowaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND liczbaJezd =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaEkspresowaJednojezdniowa")

    def drogaEkspresowawBudowie(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND x_katIstni = 'Bud' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaEkspresowawBudowie")

    def drogaGlownaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'G' AND liczbaJezd >=2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaGlownaDwujezdniowa")

    def drogaGlownaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'G' AND liczbaJezd =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaGlownaJednojezdniowa")

    def drogaZbiorczaDwujezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND liczbaJezd =2 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaZbiorczaDwujezdniowa")

    def drogaZbiorczaJednojezdniowa(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND liczbaJezd =1 AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaZbiorczaJednojezdniowa")

    def drogaLokalnaTwarda(self):
        #expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        #expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') ")
        expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa ='t' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaLokalnaTwarda")

    def drogaLokalnaUtwardzona(self):
        #expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Pb', 'Tl', 'Zw') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        #expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa IN ('Pb', 'Tl', 'Zw') ")
        expr = QgsExpression("klasaDrogi IN ('L', 'D', 'I') AND materialNa ='u' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaLokalnaUtwardzona")

    def drogaLokalnaGruntowa(self):
        #expr = QgsExpression("klasaDrogi = 'L' AND materialNa IN ('Gr', 'Gz') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        #expr = QgsExpression("klasaDrogi = 'L' AND materialNa IN ('Gr', 'Gz') ")
        expr = QgsExpression("klasaDrogi IN ('L') AND materialNa ='g' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaLokalnaGruntowa")

    def drogaDojazdowa(self):
        #expr = QgsExpression("klasaDrogi IN ('D', 'I') AND materialNa IN ('Gr', 'Gz') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG'  ")
        #expr = QgsExpression("klasaDrogi IN ('D', 'I') AND materialNa IN ('Gr', 'Gz') ")
        expr = QgsExpression("klasaDrogi IN ('D', 'I') AND materialNa ='g' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "drogaDojazdowa")

class SKJZ_L:
    def __init__(self, nazwaWarstwy):
        self.nazwaWarstwy = nazwaWarstwy
        self.nowaWarstwa = Warstwa()
        self.warstwa = self.nowaWarstwa.wyborWarstwy(self.nazwaWarstwy)

    def jezdniaAutostrady(self):
        expr = QgsExpression("klasaDrogi = 'A' AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "jezdniaAutostrady")

    def jezdniadrogiEkspresowej(self):
        expr = QgsExpression("klasaDrogi IN ('S', 'GP') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "jezdniadrogiEkspresowej")

    def jezdniaDrogiGlownejSymbol(self):
        expr = QgsExpression("klasaDrogi = 'G' AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "jezdniaDrogiGlownejSymbol")

    def jezdniaDrogiZbiorczejSymbol(self):
        expr = QgsExpression("klasaDrogi = 'Z' AND materialNa IN ('Bt', 'Br', 'Kl', 'Kk', 'Kp', 'Mb') AND x_katIstni = 'Eks' AND x_rodzajRe = 'OG' ")
        expr.prepare(self.warstwa.pendingFields())
        obiekty = filter(expr.evaluate, self.warstwa.getFeatures())
        return self.nowaWarstwa.utworzNowaWartswe(self.warstwa, "LineString",obiekty, "jezdniaDrogiZbiorczej")
        

        
        
        