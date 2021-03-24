import arcpy
from os.path import expanduser
from os.path import join as joinadd

def create_3d_polygons(polygns_3d):

    #polygns_3d=[0:lit ,1:polygonpoints, 2: 3dpolygon]
    #arcgistempdb_2d.gdb
    homeadd =joinadd(expanduser("~"),"arcgistemp")
    allpoints=list()

    for i in polygns_3d:
        for jj in i[1]:

            allpoints.append(jj)

    ################################
    list_to_gdb=list()
    #polygon 3d insert
    con=0
    litlist=list()
    ##############
    #This is added to do merging
    for ii in polygns_3d:
        if [ii[0],[]] not in litlist:
            litlist.append([ii[0],[]])
    for lit in litlist:
        for poly in polygns_3d:
            if poly[0]==lit[0]:
                lit[1].append([poly[1],poly[2]])
    for j in litlist:
        listformerge=list()
        for ii in j[1]:

            con=con+1
            temppolygonname="polygon_3d_"+str(con)+"_"+str(j[0])
            arcpy.CreateFeatureclass_management("in_memory",temppolygonname ,"POLYGON","", "DISABLED", "ENABLED","")
            listformerge.append(joinadd("in_memory",temppolygonname))

            cursor = arcpy.da.InsertCursor(joinadd("in_memory",temppolygonname), ["SHAPE@"])
            cursor.insertRow([ii[1]])
            del cursor
        mergedpolygonname=joinadd(homeadd,"merged_polygon_3d_"+str(j[0]))
        arcpy.CreateFeatureclass_management(homeadd,"merged_polygon_3d_"+str(j[0]) ,"POLYGON","", "DISABLED", "ENABLED","")
        arcpy.Merge_management(listformerge, mergedpolygonname)
        list_to_gdb.append(mergedpolygonname+".shp")
    ###############################

    '''for ii in polygns_3d:
        con=con+1
        temppolygonname="polygon_3d_"+str(con)+"_"+str(ii[0])
        arcpy.CreateFeatureclass_management("in_memory",temppolygonname ,"POLYGON","", "DISABLED", "ENABLED","")
        list_to_gdb.append(temppolygonname)
        cursor = arcpy.da.InsertCursor(temppolygonname, ["SHAPE@"])
        #print "type ii[2]", type(ii[2])
        cursor.insertRow([ii[2]])
        del cursor'''
    ####################################
    #points insert

    arcpy.CreateFeatureclass_management(homeadd,"polygon_3d_points","POINT","", "DISABLED", "ENABLED","")

    cursor = arcpy.da.InsertCursor(joinadd(homeadd,"polygon_3d_points.shp"), ["SHAPE@"])
    for t in allpoints:
        cursor.insertRow([t])
    del cursor
    #polygon_3d_points_layer= arcpy.MakeFeatureLayer_management(joinadd(homeadd,"polygon_3d_points.shp"),"polygon_3d_points_layer")
    list_to_gdb.append(joinadd(homeadd,"polygon_3d_points.shp"))
    #######################################
    arcgistempdb_2d_name=joinadd(homeadd,"arcgistempdb_3d_polygons.gdb")
    arcpy.CreateFileGDB_management(homeadd, "arcgistempdb_3d_polygons.gdb")
    arcpy.FeatureClassToGeodatabase_conversion (list_to_gdb, arcgistempdb_2d_name)
    #for iii in list_to_gdb:
    #    arcpy.Delete_management(iii)
    return

def create_3d_polygons_allpoints(polygns_3d):

    #polygns_3d=[0:lit ,1:polygonpoints, 2: 3dpolygon]
    #arcgistempdb_2d.gdb
    homeadd =joinadd(expanduser("~"),"arcgistemp")
    allpoints=list()

    for i in polygns_3d:
        for jj in i[1]:

            allpoints.append(jj)

    ################################
    list_to_gdb=list()
    #polygon 3d insert
    con=0
    litlist=list()
    ##############
    #This is added to do merging
    for ii in polygns_3d:
        '''if [ii[0],[]] not in litlist:
            litlist.append([ii[0],[]])
    for lit in litlist:
        for poly in polygns_3d:
            if poly[0]==lit[0]:
                lit[1].append([poly[1],poly[2]])
    for j in litlist:
        listformerge=list()
        for ii in j[1]:'''

        con=con+1
        temppolygonname=joinadd(homeadd,"polygon_3d_"+str(con)+"_"+str(ii[0])+".shp")
        arcpy.CreateFeatureclass_management(homeadd,"polygon_3d_"+str(con)+"_"+str(ii[0]) ,"POLYGON","", "DISABLED", "ENABLED","")
        list_to_gdb.append(temppolygonname)

        cursor = arcpy.da.InsertCursor(temppolygonname, ["SHAPE@"])
        #print "type ii[2]", type(ii[2])
        cursor.insertRow([ii[2]])
        del cursor
        #mergedpolygonname=joinadd(homeadd,"merged_polygon_3d_"+str(j[0]))
        #print mergedpolygonname
        #print listformerge
        #arcpy.CreateFeatureclass_management(homeadd,"merged_polygon_3d_"+str(j[0]) ,"POLYGON","", "DISABLED", "ENABLED","")
        #arcpy.Merge_management(listformerge, mergedpolygonname)
        #list_to_gdb.append(mergedpolygonname+".shp")
    ###############################

    '''for ii in polygns_3d:
        con=con+1
        temppolygonname="polygon_3d_"+str(con)+"_"+str(ii[0])
        arcpy.CreateFeatureclass_management("in_memory",temppolygonname ,"POLYGON","", "DISABLED", "ENABLED","")
        list_to_gdb.append(temppolygonname)
        cursor = arcpy.da.InsertCursor(temppolygonname, ["SHAPE@"])
        #print "type ii[2]", type(ii[2])
        cursor.insertRow([ii[2]])
        del cursor'''
    ####################################
    #points insert

    arcpy.CreateFeatureclass_management(homeadd,"polygon_3d_points","POINT","", "DISABLED", "ENABLED","")

    cursor = arcpy.da.InsertCursor(joinadd(homeadd,"polygon_3d_points.shp"), ["SHAPE@"])
    for t in allpoints:
        cursor.insertRow([t])
    del cursor
    #polygon_3d_points_layer= arcpy.MakeFeatureLayer_management(joinadd(homeadd,"polygon_3d_points.shp"),"polygon_3d_points_layer")
    list_to_gdb.append(joinadd(homeadd,"polygon_3d_points.shp"))
    #######################################
    arcgistempdb_2d_name=joinadd(homeadd,"arcgistempdb_3d_polygons.gdb")
    arcpy.CreateFileGDB_management(homeadd, "arcgistempdb_3d_polygons.gdb")
    arcpy.FeatureClassToGeodatabase_conversion (list_to_gdb, arcgistempdb_2d_name)
    #for iii in list_to_gdb:
    #    arcpy.Delete_management(iii)
    return
