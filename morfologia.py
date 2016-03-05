from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.analysis import *
from WarstwaOperacje import *

class Morfologia:
    def laczeniePoligonow(self, warstwa, sciezka):
        laczenie = QgsGeometryAnalyzer().dissolve(warstwa, sciezka, onlySelectedFeatures=True, uniqueIdField=-1, p=None)
        return laczenie

    def bufor(self, warstwa, sciezka, szerokosc, tylkoWybrane, polacz):
        bufor = QgsGeometryAnalyzer().buffer(warstwa, sciezka, szerokosc, tylkoWybrane, polacz, -1)
        return bufor

    def dylacja(self, warstwa, sciezka, szerokosc, tylkoWybrane, polacz):
        if  warstwa.featureCount()>0:
            self.bufor(warstwa, sciezka, szerokosc, tylkoWybrane, polacz)
            #QgsGeometryAnalyzer().buffer(warstwa, "/home/ml/Documents/Praca magisterska/proby/buffer.shp", 10, False, True, -1)
            bufor = iface.addVectorLayer(sciezka, "buforDylacja", "ogr")
            iface.setActiveLayer(bufor)
            bufor.startEditing()

            remove_list = []
            for feature in bufor.getFeatures():
                geom = feature.geometry()
                # check if feature geometry is multipart
                if geom.isMultipart():

                    remove_list.append(feature.id())
                    QgsMessageLog.logMessage(str(remove_list))

                    new_features = []
                    temp_feature = QgsFeature(feature)
                    # create a new feature using the geometry of each part
                    for part in geom.asGeometryCollection ():
                        temp_feature.setGeometry(part)
                        new_features.append(QgsFeature(temp_feature))
                    # add new features to layer
                    bufor.addFeatures(new_features, False)
            # remove the original (multipart) features from layer
            if len(remove_list) > 0:
                for id in remove_list:
                    bufor.deleteFeature (id)
            bufor.commitChanges()
            #bufor.updateExtents()
            iface.mapCanvas().refresh()
            return bufor

    def erozja(self,warstwa, sciezka, szerokosc, tylkoWybrane, polacz):
        if  warstwa.featureCount()>0:
            self.bufor(warstwa, sciezka, szerokosc, tylkoWybrane, polacz)
            iface.addVectorLayer(sciezka, "buforErozja", "ogr")


#indeksowanie przestrzenne!
