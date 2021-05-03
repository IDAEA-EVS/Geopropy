#create test polyline featureclass
import arcpy
from os.path import expanduser
from os.path import join as joinadd
import os
import copy
def createpolyfeatureclass(mainpolylist,pfcadd,postbottomboxlist,minsfirst,minslast,maxfirst,maxlast,prior):
    #postbottomboxlist=[ [point1coord,point2coord,point 1 borehole or mid (0 or 1) ,point 2 borehole or mid (0 or 1), polyline] ,... ]
    allpolies_temp=list()
    homeadd =joinadd(expanduser("~"),"arcgistemp")
    #################
    'making  priorpolylist [ priority number, [polyline1,polyline2,...] ]'
    for i in range(1,len(mainpolylist)-1):
        for j in mainpolylist[i][2]:

            allpolies_temp.append([j[0],j[3],j[4]])
            #allpolies=[prio_num,p1 coord,p2 coord]
    allpolies_temp.append(["firstbhline",maxfirst,minsfirst[1]])

    #pointlist=[maxfirst,minsfirst[1]]

    #pointlist=[maxlast,minslast[1]]
    allpolies_temp.append(["lastbhline",maxlast,minslast[1]])



    #######
    priorpolylist_temp=list()

    for n in allpolies_temp:
        if [n[0],[]] not in priorpolylist_temp:
            priorpolylist_temp.append([ n[0],[ ] ] )


    for m in priorpolylist_temp:
        for b in allpolies_temp:
            if b[0] == m[0]:

                m[1].append([b[1],b[2]])
    #################################
    #################################
    #priorpolylist=[ [prio_num,[[p1,p2],[p1,p2],...]],... ]
    #this is for solving  arcgis 3 dimension dissolve Dissolve_management malfunction:
    priorpolylist=list()

    '''zhigh=None
    zdown=None

    for m in priorpolylist_temp:

        for pnts in m[1]:
            if zhigh==None or pnts[0][2]>zhigh:
                zhigh=pnts[0][2]
            elif zdown==None or pnts[0][2]<zdown:
                zdown=pnts[0][2]
            if zhigh==None or pnts[1][2]>zhigh:
                zhigh=pnts[1][2]
            elif zdown==None or pnts[1][2]<zdown:
                zdown=pnts[1][2]
    print "zdown,zhigh", zdown,zhigh
    print 'priorpolylist_temp
    for mm in priorpolylist_temp:
        print mm[0]
        for mmm in mm[1]:
            print mmm
            mmm[0]=copy.deepcopy(mmm[0])
            mmm[1]=copy.deepcopy(mmm[1])'''
    #priorpolylist=[ [prio_num,[[p1,p2],[p1,p2],...]],... ]
    for m in priorpolylist_temp:
        polss=list()
        for pnts in m[1]:
            '''if zdown!=zhigh  :

                pnts[0][0]=pnts[0][0]+(float(pnts[0][2]-zhigh)/(zdown-zhigh))*0.01
                pnts[0][1]=pnts[0][1]+(float(pnts[0][2]-zhigh)/(zdown-zhigh))*0.01

                pnts[1][0]=pnts[1][0]+(float(pnts[1][2]-zhigh)/(zdown-zhigh))*0.01
                pnts[1][1]=pnts[1][1]+(float(pnts[1][2]-zhigh)/(zdown-zhigh))*0.01'''
            polylinee=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in [ pnts[0] , pnts[1] ]]),"Unknown",True,False)
            polss.append(polylinee)

        if type(m[0])==float:
            m[0]=int(m[0])
        priorpolylist.append([m[0],polss])

    #########################################
    #########################################
    #########################################

    #print 'priorpolylist' , priorpolylist

    #######
    tempost=list()
    for kk in postbottomboxlist:
        tempost.append(kk[4])
    priorpolylist.append( ["post_bottombox",tempost ] )
    ######
    con=0
    polylineadlist=[pfcadd]
    polylineadlistmerge=[]
    for ii in range(0,len(priorpolylist)):
        con=con+1
        temppolyname="temppoly"+str(con)
        #mypolyname=joinadd(homeadd,"mypoly")+str(con)
        #plnslayertempname=joinadd("in_memory","plnslayertemp"+str(con))+"_"+str(priorpolylist[ii][0])
        #plnslayername=joinadd(homeadd,"plnslayer")+str(con)+".shp"
        #mainplnsadd=joinadd(homeadd,"mainplns")+str(con)+".shp"
        ############
        arcpy.CreateFeatureclass_management("in_memory",temppolyname ,"POLYLINE","", "DISABLED", "ENABLED","")
        cursor = arcpy.da.InsertCursor(joinadd("in_memory",temppolyname) , ["SHAPE@"])
        for t in priorpolylist[ii][1]:
            cursor.insertRow([t])
        del cursor

        #arcpy.Dissolve_management (joinadd("in_memory",temppolyname), plnslayertempname, "", "", "", "UNSPLIT_LINES")
        #polylineadlist.append(plnslayertempname)
        ########test 2019##########
        polylineadlist.append(joinadd("in_memory",temppolyname))
        ######################
        #arcpy.Delete_management(temppolyname)



    arcgistempdb=joinadd(homeadd,"arcgistempdb.gdb")

    arcpy.CreateFileGDB_management(homeadd, "arcgistempdb.gdb")
    arcpy.FeatureClassToGeodatabase_conversion (polylineadlist, arcgistempdb)
    #for iii in polylineadlist:
    #    arcpy.Delete_management(iii)

    return arcgistempdb
#########################################
#########################################
def createpolyfeatureclass_2d(mainpolylist_2d,postbottomboxlist_2d,minsfirst,minslast,maxfirst,maxlast,prior,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,smooth_2d):
    '''
    arcpy.ExtendLine_edit(joinadd("in_memory","all_lines_2d_dissolved"),"5")
    ExtendLine_edit_distance=The maximum distance a line segment can be extended to an intersecting feature.
    arcpy.TrimLine_edit (joinadd("in_memory","all_lines_2d_dissolved"),"2", "kEEP_SHORT")
    TrimLine_edit_dangle_length=Line segments that are shorter than the specified Dangle Length and do not touch another line at both endpoints (dangles) will be trimmed.
    arcpy.Integrate_management(joinadd("in_memory","all_lines_2d_dissolved"), 0.01)
    Integrate_management_distance=The distance that determines the range in which feature vertices aremade coincident. To minimize undesired movement of vertices, the x,ytolerance should be fairly small.
    '''
    #arcpy.CreateFeatureclass_management("C:\Users\usuari\Desktop\Interpretation-test01-2018.mdb", "mainpolyli", "POLYLINE","", "DISABLED", "ENABLED")
    allpolies=list()
    infpolies=list()
    ##################
    'filenames1'
    homeadd =joinadd(expanduser("~"),"arcgistemp_2d")
    #plnsadd=joinadd(homeadd,"plns_2d")
    #################
    'making  priorpolylist [ priority number, [polyline1,polyline2,...] ]'
    for i in range(0,len(mainpolylist_2d)):
        for j in mainpolylist_2d[i][2]:
            allpolies.append([j[0],j[2]])
    #######
    #postbottomboxlist=[ [point1coord,point2coord,point 1 borehole or mid (0 or 1) ,point 2 borehole or mid (0 or 1), polyline] ,... ]
    for kk in postbottomboxlist_2d:
        allpolies.append( ["post_bottombox_2d",kk[4] ] )
    ######
    pointlist=[maxfirst,minsfirst[1]]
    firstbhline_2d=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlist]),"Unknown",False,False)
    allpolies.append(["firstbhline_2d",firstbhline_2d])

    pointlist=[maxlast,minslast[1]]
    lastbhline_2d=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlist]),"Unknown",False,False)
    allpolies.append(["lastbhline_2d",lastbhline_2d])

    #######

    priorpolylist=list()
    #print 'allpolies is:', allpolies


    for n in allpolies:
        if [n[0],[]] not in priorpolylist:
            priorpolylist.append([ n[0],[ ] ] )


    for m in priorpolylist:
        for b in allpolies:
            if b[0] == m[0]:

                m[1].append(b[1])

    #print 'priorpolylist_2d' , priorpolylist
    ###################
    'creating the main polyline featureclass'

    con=0
    polylineadlistmerge=[]
    polylineadlistmerge_smooth=[]
    arcpy.CreateFeatureclass_management("in_memory","all_lines_2d" ,"POLYLINE","", "DISABLED", "DISABLED","")
    for ii in range(0,len(priorpolylist)):
        con=con+1

        'names'
        temppolyname="temppoly_2d"+str(con)
        #plnslayername=joinadd(homeadd,"plnslayer_2d")+str(con)+".shp"
        #mainplnsadd=joinadd(homeadd,"mainplns_2d")+str(con)+".shp"
        #mainplnsadd2=joinadd(homeadd,"mainplns_2d")+str(con+1)
        ############
        arcpy.CreateFeatureclass_management("in_memory",temppolyname ,"POLYLINE","", "DISABLED", "DISABLED","")

        cursor = arcpy.da.InsertCursor(joinadd("in_memory",temppolyname) , ["SHAPE@"])
        for t in priorpolylist[ii][1]:
            cursor.insertRow([t])
        del cursor
        ############### test 2019
        cursor = arcpy.da.InsertCursor(joinadd("in_memory","all_lines_2d") , ["SHAPE@"])
        for t in priorpolylist[ii][1]:
            cursor.insertRow([t])
        del cursor
        ###################
        #dissolve:basic
        #integrate: basic
        #ExtendLine_edit: standard
        #TrimLine_edit: standard
        #Integrate_management:basic
        #RepairGeometry_management:basic
        #FeatureToPolygon_management: advanced
        #
        arcpy.Dissolve_management (joinadd("in_memory",temppolyname), joinadd("in_memory","plnslayertemp_2d"+str(con)), "", "", "", "UNSPLIT_LINES")
        arcpy.Integrate_management(joinadd("in_memory","plnslayertemp_2d"+str(con)), 0.01)
        polylineadlistmerge.append(joinadd("in_memory","plnslayertemp_2d"+str(con)))
        #arcpy.FeatureVerticesToPoints_management(joinadd("in_memory","plnslayertemp_2d"+str(con)),joinadd(homeadd,"dangle"+str(con)),"DANGLE")
        ################
        if smooth_2d==True:
            #smoothing
            arcpy.SmoothLine_cartography(joinadd("in_memory","plnslayertemp_2d"+str(con)), joinadd("in_memory","smoothed"+str(con)), "BEZIER_INTERPOLATION","", "FIXED_CLOSED_ENDPOINT","")
            polylineadlistmerge_smooth.append(joinadd("in_memory","smoothed"+str(con)))
    #############test 2019
    arcpy.Dissolve_management (joinadd("in_memory","all_lines_2d"), joinadd("in_memory","all_lines_2d_dissolved"), "", "", "", "UNSPLIT_LINES")
    arcpy.ExtendLine_edit(joinadd("in_memory","all_lines_2d_dissolved"),str(ExtendLine_edit_distance))
    arcpy.TrimLine_edit (joinadd("in_memory","all_lines_2d_dissolved"),str(TrimLine_edit_dangle_length), "kEEP_SHORT")
    arcpy.Integrate_management(joinadd("in_memory","all_lines_2d_dissolved"), Integrate_management_distance)
    arcpy.RepairGeometry_management(joinadd("in_memory","all_lines_2d_dissolved"))
    arcpy.FeatureToPolygon_management (joinadd("in_memory","all_lines_2d_dissolved"), joinadd("in_memory","all_lines_2d_dissolved_feat_to_poly"), "0.02", "", "")
    polylineadlistmerge.append(joinadd("in_memory","all_lines_2d_dissolved_feat_to_poly"))
    ###################
    #smoothing
    if smooth_2d==True:
        arcpy.SmoothLine_cartography(joinadd("in_memory","all_lines_2d_dissolved"), joinadd("in_memory","all_lines_2d_dissolved_smoothed"), "BEZIER_INTERPOLATION","", "FIXED_CLOSED_ENDPOINT","")
        arcpy.FeatureToPolygon_management (joinadd("in_memory","all_lines_2d_dissolved_smoothed"), joinadd("in_memory","all_lines_2d_dissolved_feat_to_poly_smoothed"), "0.02", "", "")
        polylineadlistmerge_smooth.append(joinadd("in_memory","all_lines_2d_dissolved_feat_to_poly_smoothed"))
        arcpy.CreateFileGDB_management(homeadd, "arcgistempdb_2d_smoothed.gdb")
        arcpy.FeatureClassToGeodatabase_conversion (polylineadlistmerge_smooth, joinadd(homeadd,"arcgistempdb_2d_smoothed.gdb"))
    ###################
    mergedpolygonsfromlines_2d=joinadd("in_memory","mergedpolygonsfromlines_2d")

    arcgistempdb_2d=joinadd(homeadd,"arcgistempdb_2d.gdb")

    arcpy.FeatureToPolygon_management (polylineadlistmerge, mergedpolygonsfromlines_2d, "", "", "")

    polylineadlistmerge.append(mergedpolygonsfromlines_2d)
    arcpy.CreateFileGDB_management(homeadd, "arcgistempdb_2d.gdb")
    arcpy.FeatureClassToGeodatabase_conversion (polylineadlistmerge, arcgistempdb_2d)
    #####################
    return arcgistempdb_2d
