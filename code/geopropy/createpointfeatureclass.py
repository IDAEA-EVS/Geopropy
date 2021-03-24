import arcpy
from os.path import expanduser
from os.path import join as joinadd
import os

def createpointfeatureclass(boxpoints,mainpointlist,intersectionpoints, postbottomboxlist,lastvirtbhindex):
    pointlistgeometry=[]
    postbottomboxtemp=list()
    for i in mainpointlist:
        if i[2] not in [-1,0]:
            pointlistgeometry.append(arcpy.PointGeometry(arcpy.Point(*i[5]),"Unknown",True,False))

    for j in intersectionpoints:
        if j[0] !=1 and j[1]!=lastvirtbhindex: 
            pointlistgeometry.append(arcpy.PointGeometry(arcpy.Point(*j[4]),"Unknown",True,False))
        #intersectionpoints=[ [index1, index2,prio_num1, prio_num2,intersectioncoord, intersectiontype] ]

    for k in postbottomboxlist:
        if k[2] not in postbottomboxtemp:
            postbottomboxtemp.append(k[2])
        if k[3] not in postbottomboxtemp:
            postbottomboxtemp.append(k[3])

    for r in postbottomboxtemp:
        #print 'r is', r
        pointlistgeometry.append(arcpy.PointGeometry(arcpy.Point(*r),"Unknown",True,False))

    #allpoints=boxpoints+pointlistgeometry
    allpoints=pointlistgeometry





    homeadd =joinadd(expanduser("~"),"arcgistemp")
    """pfcadd=joinadd(homeadd,"pfc.shp"
    plnsadd=joinadd(homeadd,"plns.shp")
    if os.path.exists(pfcadd):
        arcpy.DeleteFeatures_management(pfcadd)
    if os.path.exists(plnsadd):
        arcpy.DeleteFeatures_management(plnsadd)"""

    arcpy.env.overwriteOutput = True
    arcpy.CreateFeatureclass_management(homeadd, "pfc.shp", "POINT","", "DISABLED", "ENABLED","")

    pointfeatureclasssadd =joinadd(homeadd,"pfc.shp")
    cursor = arcpy.da.InsertCursor(pointfeatureclasssadd, ["SHAPE@"])
    for t in allpoints:
        cursor.insertRow([t])
    del cursor
    pfclayer= arcpy.MakeFeatureLayer_management(pointfeatureclasssadd,"pfc_layer")

    return pfclayer
