from WarstwaOperacje import *
import processing
from qgis.utils import *
from PyQt4.QtCore import QVariant
from selekcja50k import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion
from PyQt4.QtGui import QAction, QIcon
from math import degrees, atan2

class RoadSimplification(Warstwa):
    def simplify(self):
        skdr = SKDR_L("OT_SKDR_L")
        autostrada = skdr.autostrada()
        autostradawBudowie = skdr.autostradawBudowie()
        drEksDwujezdniowa = skdr.drogaEkspresowaDwujezdniowa()
        drEksJednojezdniowa = skdr.drogaEkspresowaJednojezdniowa()
        drEkswBudowie = skdr.drogaEkspresowawBudowie()
        drGlDwujezdniowa = skdr.drogaGlownaDwujezdniowa()
        drGlJednojezdniowa= skdr.drogaGlownaJednojezdniowa()
        drZbDwujezdniowa = skdr.drogaZbiorczaDwujezdniowa()
        drZbJednonezdniowa = skdr.drogaZbiorczaJednojezdniowa()
        #OT_SKDR_L_o - warstwa drog polaczonych
        skdr2 = SKDR_L("OT_SKDR_L_o")
        drLokTwarda = skdr2.drogaLokalnaTwarda()
        drLokUtwardzona = skdr2.drogaLokalnaUtwardzona()
        drLokGruntowa = skdr2.drogaLokalnaGruntowa()
        drDojazdowa = skdr2.drogaDojazdowa()

        skjz = SKJZ_L("OT_SKJZ_L")
        jAutostrady = skjz.jezdniaAutostrady()
        jDrEks = skjz.jezdniadrogiEkspresowej()
        jDrGlSym = skjz.jezdniaDrogiGlownejSymbol()
        jDrZbSym = skjz.jezdniaDrogiZbiorczejSymbol()

        # QgsMapLayerRegistry.instance().addMapLayer(autostrada)
        # QgsMapLayerRegistry.instance().addMapLayer(autostradawBudowie)
        # QgsMapLayerRegistry.instance().addMapLayer(drEksDwujezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drEksJednojezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drEkswBudowie)
        # QgsMapLayerRegistry.instance().addMapLayer(drGlDwujezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drGlJednojezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drZbDwujezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drZbJednonezdniowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drLokTwarda)
        # QgsMapLayerRegistry.instance().addMapLayer(drLokUtwardzona)
        # QgsMapLayerRegistry.instance().addMapLayer(drLokGruntowa)
        # QgsMapLayerRegistry.instance().addMapLayer(drDojazdowa)
        # QgsMapLayerRegistry.instance().addMapLayer(jAutostrady)
        # QgsMapLayerRegistry.instance().addMapLayer(jDrEks)
        # QgsMapLayerRegistry.instance().addMapLayer(jDrGlSym)
        # QgsMapLayerRegistry.instance().addMapLayer(jDrZbSym)

        #drogi wyzszych klas
        #jezdnie
        inddroga = jAutostrady.fieldNameIndex("skdr_l1")
        jList = [jAutostrady, jDrEks]
        for lyr in jList:
            for feature in lyr.getFeatures():
                for feature2 in lyr.getFeatures():
                    buf1 = feature.geometry().buffer(50,2)
                    buf2 = feature2.geometry().buffer(50,2)
                    intersect = buf1.intersection(buf2)
                    if intersect.area>10:
                        lyr.startEditing()
                        if feature2.attributes()[inddroga] != NULL:
                            lyr.deleteFeature(feature2.id())
                        if feature.attributes()[inddroga] != NULL:
                            lyr.deleteFeature(feature.id())
                        lyr.commitChanges()
        #rozjazdy
        rozjazdyEks = []
        for feature in drEksJednojezdniowa.getFeatures():
            for rozjazd in jDrEks.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyEks.append(rozjazd.id())
                        for rozjazd2 in jDrEks.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyEks.append(rozjazd2.id())
        for feature in drEksDwujezdniowa.getFeatures():
            for rozjazd in jDrEks.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyEks.append(rozjazd.id())
                        for rozjazd2 in jDrEks.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyEks.append(rozjazd2.id())
        jDrEks.startEditing()
        for feat in jDrEks.getFeatures():
            if feat.attributes()[inddroga] == NULL:
                if feat.id() not in rozjazdyEks:
                    jDrEks.deleteFeature(feat.id())
        jDrEks.commitChanges()

        rozjazdyGl = []
        for feature in drGlJednojezdniowa.getFeatures():
            for rozjazd in jDrGlSym.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyGl.append(rozjazd.id())
                        for rozjazd2 in jDrGlSym.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyGl.append(rozjazd2.id())
        for feature in drGlDwujezdniowa.getFeatures():
            for rozjazd in jDrGlSym.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyGl.append(rozjazd.id())
                        for rozjazd2 in jDrGlSym.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyGl.append(rozjazd2.id())
        jDrGlSym.startEditing()
        for feat in jDrGlSym.getFeatures():
                if feat.id() not in rozjazdyGl:
                    jDrGlSym.deleteFeature(feat.id())
        jDrGlSym.commitChanges()

        rozjazdyZb = []
        for feature in drZbJednonezdniowa.getFeatures():
            for rozjazd in jDrZbSym.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyZb.append(rozjazd.id())
                        for rozjazd2 in jDrZbSym.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyZb.append(rozjazd2.id())
        for feature in drZbDwujezdniowa.getFeatures():
            for rozjazd in jDrZbSym.getFeatures():
                if rozjazd.attributes()[inddroga] == NULL:
                    if feature.geometry().intersects(rozjazd.geometry()):
                        rozjazdyZb.append(rozjazd.id())
                        for rozjazd2 in jDrZbSym.getFeatures():
                            if rozjazd2.attributes()[inddroga] == NULL:
                                if rozjazd.geometry().intersects(rozjazd2.geometry()):
                                    rozjazdyZb.append(rozjazd2.id())
        jDrZbSym.startEditing()
        for feat in jDrZbSym.getFeatures():
                if feat.id() not in rozjazdyZb:
                    jDrZbSym.deleteFeature(feat.id())
        jDrZbSym.commitChanges()

        roadsH = [autostrada, autostradawBudowie, drEksDwujezdniowa, drEksJednojezdniowa, drEkswBudowie, drGlDwujezdniowa, drGlJednojezdniowa, drZbDwujezdniowa, drZbJednonezdniowa, jAutostrady, jDrEks, jDrZbSym, jDrGlSym]
        for r in roadsH:
            if r.featureCount()>0:
                QgsMapLayerRegistry.instance().addMapLayer(r)
        #------------------------------------------------------------------------------------------------------------------------------------------
        #drogi nizszych klas
        #dodanie atrybutow do warstw
        drLokTwarda.dataProvider().addAttributes([QgsField("ranga", QVariant.Int)])
        drLokTwarda.dataProvider().addAttributes([QgsField("touch", QVariant.Int)])
        drLokTwarda.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        drLokTwarda.updateFields()

        drLokUtwardzona.dataProvider().addAttributes([QgsField("ranga", QVariant.Int)])
        drLokUtwardzona.dataProvider().addAttributes([QgsField("touch", QVariant.Int)])
        drLokUtwardzona.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        drLokUtwardzona.updateFields()

        drLokGruntowa.dataProvider().addAttributes([QgsField("ranga", QVariant.Int)])
        drLokGruntowa.dataProvider().addAttributes([QgsField("touch", QVariant.Int)])
        drLokGruntowa.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        drLokGruntowa.updateFields()

        drDojazdowa.dataProvider().addAttributes([QgsField("ranga", QVariant.Int)])
        drDojazdowa.dataProvider().addAttributes([QgsField("touch", QVariant.Int)])
        drDojazdowa.dataProvider().addAttributes([QgsField("orientacja", QVariant.Double)])
        drDojazdowa.updateFields()

        indorient = drLokTwarda.fieldNameIndex("orientacja")
        drLokTwarda.startEditing()
        for feat in drLokTwarda.getFeatures():
            if len(feat.geometry().asPolyline())>0:
                p1 = feat.geometry().asPolyline()[0]
                p2 = feat.geometry().asPolyline()[-1]
                xDiff = p2.x() - p1.x()
                yDiff = p2.y() - p1.y()
                orient = degrees(atan2(yDiff, xDiff))
                drLokTwarda.changeAttributeValue(feat.id(), indorient, orient)
        drLokTwarda.commitChanges()
        drLokUtwardzona.startEditing()
        for feat in drLokUtwardzona.getFeatures():
            p1 = feat.geometry().asPolyline()[0]
            p2 = feat.geometry().asPolyline()[-1]
            xDiff = p2.x() - p1.x()
            yDiff = p2.y() - p1.y()
            orient = degrees(atan2(yDiff, xDiff))
            drLokUtwardzona.changeAttributeValue(feat.id(), indorient, orient)
        drLokUtwardzona.commitChanges()
        drLokGruntowa.startEditing()
        for feat in drLokGruntowa.getFeatures():
            p1 = feat.geometry().asPolyline()[0]
            p2 = feat.geometry().asPolyline()[-1]
            xDiff = p2.x() - p1.x()
            yDiff = p2.y() - p1.y()
            orient = degrees(atan2(yDiff, xDiff))
            drLokGruntowa.changeAttributeValue(feat.id(), indorient, orient)
        drLokGruntowa.commitChanges()

        drDojazdowa.startEditing()
        for feat in drDojazdowa.getFeatures():
            p1 = feat.geometry().asPolyline()[0]
            p2 = feat.geometry().asPolyline()[-1]
            xDiff = p2.x() - p1.x()
            yDiff = p2.y() - p1.y()
            orient = degrees(atan2(yDiff, xDiff))
            drDojazdowa.changeAttributeValue(feat.id(), indorient, orient)
            drDojazdowa.commitChanges()


        indranga = drLokTwarda.fieldNameIndex("ranga")
        buildingArea = [self.wyborWarstwy("zabudowaWielorodzinnaGesta"), self.wyborWarstwy("zabudowaWielorodzinnaZwarta"), self.wyborWarstwy("zabudowaJednorodzinna")]
        tempGeom = QgsGeometry()
        first = True
        for i in buildingArea:
            for j in i.getFeatures():
                buf = j.geometry().buffer(1,2)
                if first:
                    tempGeom = buf
                    first = False
                else:
                    tempGeom = tempGeom.combine(buf)
        buildings = QgsFeature()
        buildings.setGeometry(tempGeom)

        selected = []
        ind = drLokTwarda.fieldNameIndex("nazwa")
        ind2 = drLokTwarda.fieldNameIndex("klasaDrogi")

        build = BUBD_A("OT_BUBD_A")
        przemyslowySkala = build.budynekPrzemyslowySkala()
        przemyslowySymbol = build.budynekPrzemyslowySymbol()
        publicznySkala = build.budynekUzytecznosciPublicznejSkala()
        publicznySymbol = build.budynekUzytecznosciPublicznejSymbol()
        mieszkalnySkala = build.budynekMieszkalnySkala()
        mieszkalnySymbol = build.budynekMieszkalnySymbol()
        gospodarczySkala = build.budynekGospodarczySkala()
        gospodarczySymbol = build.budynekGospodarczySymbol()
        swiatyniaChrzescijanska = build.swiatyniaChrzescijanskaSymbol()
        swiatyniaNiechrzescijanska = build.swiatyniaNiechrzescijanskaSymbol()
        buwt = BUWT_A("OT_BUWT_A")
        przemyslowySkalabuwt=  buwt.budynekPrzemyslowySkala()
        przemyslowySymbolbuwt = buwt.budynekPrzemyslowySymbol()
        building = self.polaczWarstwy("Polygon", "przemyslowePubliczne", przemyslowySkala, przemyslowySymbol, przemyslowySkalabuwt, przemyslowySymbolbuwt, publicznySkala, publicznySymbol )

        #nadanie rang
        drLokTwarda.startEditing()
        for feat in drLokTwarda.getFeatures():
            #droga z nazwa
            if feat.attributes()[ind]:
                drLokTwarda.changeAttributeValue(feat.id(), indranga, 0)
            elif feat.attributes()[ind2] == "L" and not feat.attributes()[ind]:
                # droga lokalna poza zabudowa
                if not feat.geometry().intersects(buildings.geometry()):
                    drLokTwarda.changeAttributeValue(feat.id(), indranga, 1)
                #droga lokalna na zabudowie o szerokosci korony znacznie wiekszej niz szerokosc drogi i bez nazwy
                elif feat.geometry().intersects(buildings.geometry()):
                    #droga lokalna na zabudowie bez nazwy
                    if not feat.attributes()[ind]:
                        drLokTwarda.changeAttributeValue(feat.id(), indranga, 2)
            #drogi dojazdowe i inne
            elif (feat.attributes()[ind2] == "D" or feat.attributes()[ind2] == "I") and not feat.attributes()[ind]:
                for build in buildingArea[2].getFeatures():
                    if not feat.geometry().intersects(build.geometry()):
                        #droga poza zabudowa jednorodzinna i krotsza niz 150
                        if feat.geometry().length() <= 150:
                            drLokTwarda.deleteFeature(feat.id())
                            break
                    else:
                        #droga na zabudowie jednorodzinnej i krotsza niz 150 lub krotsza niz 200 bez nazwy
                        if feat.geometry().length() <= 200:
                            drLokTwarda.deleteFeature(feat.id())
                            break
                #drogi do budynkow przemyslowych, budynkow uzytecznosci publicznej
                if building.featureCount()>0:
                    for build in building.getFeatures():
                        if feat.geometry().buffer(10,2).intersects(build.geometry()):
                            drLokTwarda.changeAttributeValue(feat.id(), indranga, 1)
                        else:
                            drLokTwarda.changeAttributeValue(feat.id(), indranga, 2)
                else:
                    drLokTwarda.changeAttributeValue(feat.id(), indranga, 2)
        drLokTwarda.updateFields()
        drLokTwarda.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(drLokTwarda)

        building2 = self.polaczWarstwy("Polygon", "buildings", building, mieszkalnySkala, mieszkalnySymbol, gospodarczySkala, gospodarczySymbol, swiatyniaNiechrzescijanska, swiatyniaChrzescijanska )
        roads = drLokTwarda
        drLokUtwardzona.startEditing()
        for feat in drLokUtwardzona.getFeatures():
            if feat.attributes()[ind]:
                drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 0)
            elif feat.attributes()[ind2] == "L" and not feat.attributes()[ind]:
                if feat.geometry().intersects(buildings.geometry()):
                    drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 2)
                if not feat.geometry().intersects(buildings.geometry()):
                    drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 2)
                    if building2.featureCount() > 0:
                        for build in building2.getFeatures():
                            if feat.geometry().buffer(10, 2).intersects(build.geometry()):
                                drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 1)
                            else:
                                drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 3)
                    for road in roads.getFeatures():
                        if feat.geometry().buffer(5,2).intersects(road.geometry()):
                            drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 1)
                        else:
                            drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 3)
            elif (feat.attributes()[ind2] == "D" or feat.attributes()[ind2] == "I") and not feat.attributes()[ind]:
                if feat.geometry().length() <= 125:
                    drLokUtwardzona.deleteFeature(feat.id())
                    continue
                if building.featureCount() > 0:
                    for build in building.getFeatures():
                        if feat.geometry().buffer(10, 2).intersects(build.geometry()):
                            drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 1)
                        else:
                            drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 2)
                else:
                    drLokUtwardzona.changeAttributeValue(feat.id(), indranga, 2)
        drLokUtwardzona.updateFields()
        drLokUtwardzona.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(drLokUtwardzona)

        roads2 = self.polaczWarstwy("LineString", "roads2", roads, drLokUtwardzona)
        drLokGruntowa.startEditing()
        for feat in drLokGruntowa.getFeatures():
            if feat.attributes()[ind]:
                drLokGruntowa.changeAttributeValue(feat.id(), indranga, 0)
            elif feat.attributes()[ind2] == "L" and not feat.attributes()[ind]:
                if feat.geometry().intersects(buildings.geometry()) and not feat.attributes()[ind]:
                    drLokGruntowa.changeAttributeValue(feat.id(), indranga, 2)
                if not feat.geometry().intersects(buildings.geometry()) and not feat.attributes()[ind]:
                    drLokGruntowa.changeAttributeValue(feat.id(), indranga, 2)
                    if building2.featureCount() > 0:
                        for build in building2.getFeatures():
                                if feat.geometry().buffer(10, 2).intersects(build.geometry()) :
                                    drLokGruntowa.changeAttributeValue(feat.id(), indranga, 1)
                                else:
                                    drLokGruntowa.changeAttributeValue(feat.id(), indranga, 3)
                    for road in roads2.getFeatures():
                        if feat.geometry().buffer(5,2).intersects(road.geometry()):
                            drLokGruntowa.changeAttributeValue(feat.id(), indranga, 1)
                        else:
                            drLokGruntowa.changeAttributeValue(feat.id(), indranga, 3)
        drLokGruntowa.updateFields()
        drLokGruntowa.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(drLokGruntowa)

        #usuwanie drog lezacych zbyt blisko siebie
        buffers = []
        for road1 in drLokGruntowa.getFeatures():
            if road1.attributes()[ind2] == "L" :
                if not road1.geometry().intersects(buildings.geometry()):
                        if road1.attributes()[indranga] == 1:
                            buf = road1.geometry().buffer(25,2)
                            attr = road1.id()
                        else:
                            buf = road1.geometry().buffer(100, 2)
                            attr = road1.id()
                else:
                    buf = road1.geometry().buffer(37.5, 2)
                    attr = road1.id()
                outFeat = QgsFeature()
                outFeat.setGeometry(buf)
                outFeat.setAttributes([attr])
                buffers.append(outFeat)
        drLokGruntowa.startEditing()
        for i, buf1 in enumerate(buffers):
            for j, buf2 in enumerate(buffers):
                if i>=j:
                    continue
                if (buf1.geometry().intersection(buf2.geometry())).area()>150*150:
                    for dr1 in drLokGruntowa.getFeatures():
                        for dr2 in drLokGruntowa.getFeatures():
                            if buf1.attributes()[0] == dr1.id() and buf2.attributes()[0] == dr2.id():
                                if abs(dr1.attributes()[indorient]-dr2.attributes()[indorient])<20 and not dr1.geometry().touches(dr2.geometry()):
                                    if dr1.attributes()[indranga]>dr2.attributes()[indranga]:
                                        drLokGruntowa.deleteFeature(dr1.id())
                                        break
                                    elif dr1.attributes()[indranga]<dr2.attributes()[indranga]:
                                        drLokGruntowa.deleteFeature(dr2.id())
                                    else:
                                        if dr1.geometry().length() > dr2.geometry().length():
                                            drLokGruntowa.deleteFeature(dr2.id())
                                        else:
                                            drLokGruntowa.deleteFeature(dr1.id())
                                            break
        drLokGruntowa.commitChanges()

        buffers = []
        for road1 in drLokUtwardzona.getFeatures():
            if road1.attributes()[ind2] == "L":
                if not road1.geometry().intersects(buildings.geometry()):
                    if road1.attributes()[indranga] == 1:
                        buf = road1.geometry().buffer(25,2)
                        attr = road1.id()
                    else:
                        buf = road1.geometry().buffer(100, 2)
                        attr = road1.id()
                else:
                    buf = road1.geometry().buffer(37.5, 2)
                    attr = road1.id()
                outFeat = QgsFeature()
                outFeat.setGeometry(buf)
                outFeat.setAttributes([attr])
                buffers.append(outFeat)
        drLokUtwardzona.startEditing()
        for i, buf1 in enumerate(buffers):
            for j, buf2 in enumerate(buffers):
                if i>=j:
                    continue
                if (buf1.geometry().intersection(buf2.geometry())).area()>150*150:
                    for dr1 in drLokUtwardzona.getFeatures():
                        for dr2 in drLokUtwardzona.getFeatures():
                            if buf1.attributes()[0] == dr1.id() and buf2.attributes()[0] == dr2.id():
                                if abs(dr1.attributes()[indorient]-dr2.attributes()[indorient])<20 and not dr1.geometry().touches(dr2.geometry()):

                                    if dr1.attributes()[indranga]>dr2.attributes()[indranga]:
                                        drLokUtwardzona.deleteFeature(dr1.id())
                                        break
                                    elif dr1.attributes()[indranga]<dr2.attributes()[indranga]:
                                        drLokUtwardzona.deleteFeature(dr2.id())
                                    else:
                                        if dr1.geometry().length() > dr2.geometry().length():
                                            drLokUtwardzona.deleteFeature(dr2.id())
                                        else:
                                            drLokUtwardzona.deleteFeature(dr1.id())
                                            break
        drLokUtwardzona.commitChanges()

        drLokTwarda.startEditing()
        for road in drLokTwarda.getFeatures():
            for road1 in drLokGruntowa.getFeatures():
                if road.geometry().touches(road1.geometry()) and road.attributes()[indranga] == NULL:
                    drLokTwarda.changeAttributeValue(road.id(), indranga, 1)
        drLokTwarda.updateFields()
        drLokTwarda.commitChanges()

        buffers = []
        for road1 in drLokTwarda.getFeatures():
            if road1.attributes()[ind2] == "L":
                if road1.geometry().intersects(buildings.geometry()):
                    buf = road1.geometry().buffer(37.5, 2)
                    attr = road1.id()
                outFeat = QgsFeature()
                outFeat.setGeometry(buf)
                outFeat.setAttributes([attr])
                buffers.append(outFeat)
        drLokTwarda.startEditing()
        for i, buf1 in enumerate(buffers):
            for j, buf2 in enumerate(buffers):
                if i>=j:
                    continue
                if (buf1.geometry().intersection(buf2.geometry())).area()>150*150:
                    for dr1 in drLokTwarda.getFeatures():
                        for dr2 in drLokTwarda.getFeatures():
                            if buf1.attributes()[0] == dr1.id() and buf2.attributes()[0] == dr2.id():
                                if abs(dr1.attributes()[indorient]-dr2.attributes()[indorient])<20 and not dr1.geometry().touches(dr2.geometry()):
                                    if dr1.attributes()[indranga]>dr2.attributes()[indranga]:
                                        drLokTwarda.deleteFeature(dr1.id())
                                        break
                                    elif dr1.attributes()[indranga]<dr2.attributes()[indranga]:
                                        drLokTwarda.deleteFeature(dr2.id())
                                    else:
                                        if dr1.geometry().length() > dr2.geometry().length():
                                            drLokTwarda.deleteFeature(dr2.id())
                                        else:
                                            drLokTwarda.deleteFeature(dr1.id())
                                            break
        drLokTwarda.commitChanges()

        roads = self.polaczWarstwy("LineString", "roads3", drLokTwarda, drLokGruntowa, drLokUtwardzona)
        drDojazdowa.startEditing()
        for feat in drDojazdowa.getFeatures():
            if (feat.attributes()[ind2] == "D" or feat.attributes()[ind2] == "I") and not feat.attributes()[ind]:
                if feat.geometry().length() <= 125:
                    drDojazdowa.deleteFeature(feat.id())
                    continue
                for road in roads.getFeatures():
                    if feat.geometry().touches(road.geometry()):
                        drDojazdowa.changeAttributeValue(feat.id(), indranga, 1)
                    else:
                        drDojazdowa.changeAttributeValue(feat.id(), indranga, 3)
        drDojazdowa.updateFields()
        for feat in drDojazdowa.getFeatures():
            if feat.attributes()[indranga] != 1 and feat.attributes()[indranga] != 0:
                drDojazdowa.deleteFeature(feat.id())
        drDojazdowa.updateFields()
        drDojazdowa.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(drDojazdowa)

        #usuniecie drog z dwoma slepymi zakonczeniami
        indtouch = drLokTwarda.fieldNameIndex("touch")
        roads = self.polaczWarstwy("LineString", "roads3", drLokTwarda, drLokUtwardzona, drLokGruntowa, autostrada, autostradawBudowie, drEksDwujezdniowa, drEksJednojezdniowa, drEkswBudowie, drGlDwujezdniowa, drGlJednojezdniowa, drZbDwujezdniowa, drZbJednonezdniowa)
        drLokTwarda.startEditing()
        drLokUtwardzona.startEditing()
        drLokGruntowa.startEditing()
        for r in roads.getFeatures():
            for r2 in drLokTwarda.getFeatures():
                if not r.geometry().equals(r2.geometry()):
                    if r.geometry().buffer(5,2).intersects(r2.geometry()):
                        drLokTwarda.changeAttributeValue(r2.id(), indtouch, 1)
            for r3 in drLokUtwardzona.getFeatures():
                if not r.geometry().equals(r3.geometry()):
                    if r.geometry().buffer(5,2).intersects(r3.geometry()):
                        drLokUtwardzona.changeAttributeValue(r3.id(), indtouch, 1)
            for r4 in drLokGruntowa.getFeatures():
                if not r.geometry().equals(r4.geometry()):
                    if r.geometry().buffer(5,2).intersects(r4.geometry()):
                        drLokGruntowa.changeAttributeValue(r4.id(), indtouch, 1)
        for r in drLokTwarda.getFeatures():
            if r.attributes()[indtouch] != 1:
                drLokTwarda.deleteFeature(r.id())
        for r in drLokUtwardzona.getFeatures():
            if r.attributes()[indtouch] != 1:
                drLokUtwardzona.deleteFeature(r.id())
        for r in drLokGruntowa.getFeatures():
            if r.attributes()[indtouch] != 1:
                drLokGruntowa.deleteFeature(r.id())
        drLokTwarda.commitChanges()
        drLokUtwardzona.commitChanges()
        drLokGruntowa.commitChanges()

        style_path = "/home/ml/.qgis2/python/plugins/Generalization/style/"
        qml_path = style_path + "autostrada.qml"
        autostrada.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaEkspresowaJednojezdniowa.qml"
        drEksJednojezdniowa.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaGlownaJednojezdniowa.qml"
        drGlJednojezdniowa.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaLokalnaGruntowa.qml"
        drLokGruntowa.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaLokalnaTwarda.qml"
        drLokTwarda.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaLokalnaUtwardzona.qml"
        drLokUtwardzona.loadNamedStyle(qml_path)
        qml_path = style_path + "drogaZbiorczaJednojezdniowa.qml"
        drZbJednonezdniowa.loadNamedStyle(qml_path)