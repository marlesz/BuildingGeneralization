from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.analysis import *
from WarstwaOperacje import *
import math

class RamerDouglasPeucker:
    def __init__(self, tolerance):
        self.tolerance = tolerance

    def extractPoints(self, feature):
        geom = feature.geometry()
        multi_geom = QgsGeometry()
        temp_geom = []
        if geom.type() == 2:  # it's a polygon
            if geom.isMultipart():
                multi_geom = geom.asMultiPolygon()
                for i in multi_geom: #i is a polygon
                    for j in i: #j is a line
                        temp_geom.extend(j)
            else:
                multi_geom = geom.asPolygon()
                for i in multi_geom: #i is a line
                    temp_geom.extend(i)
        QgsMessageLog.logMessage(str(temp_geom))

        return temp_geom

    def simplify(self, feature):
        pointList = self.extractPoints(feature)
        dmax = 0
        index = 0
        end = len(pointList)
        for i in range(1,end-1):
            d = self.distancePointToSegment(pointList[i], pointList[0], pointList[end-2])
            if d>dmax:
                index = i
                dmax = d
        if dmax>self.tolerance:
            result1 = self.simplify(pointList[:(index+1)])
            result2 = self.simplify(pointList[index:])
            result = result1[0:len(result1)-1] + result2
        else:
            result =[pointList[0], pointList[end-2]]
        return result

    def distancePointToSegment(self, point, lineStart, lineEnd):
        v=[lineEnd.x() - lineStart.x(), lineEnd.y() - lineStart.y()]
        QgsMessageLog.logMessage(str(lineStart.x()))
        QgsMessageLog.logMessage(str(lineEnd.x()))


        n = [-v[1], v[0]] #normal vector
        #Ax + By + C = 0
        A = n[0]
        B = n[1]
        C = -(A * lineEnd.x() + B * lineEnd.y())
        return (math.fabs(A*point.x() + B * point.y() + C))/math.sqrt(math.pow(A, 2) + math.pow(B, 2))

    def runsimplify(self, warstwa):
        for feature in warstwa.getFeatures():
            self.simplify(feature)

    """def simplifypointList(self, pointlist):
        return pointlist"""


