
#This function:
#1.project the start and end line points from 3d to 2d
#2.make the polylines in 2d
#3.using arcpy, clean the 2d closed polygons (check for all lines to be complete)
#5.using arcpy, determines the polygones
#6.save the critical points their polylines in 2d
#7.transfer the ponit to 3d (with id??)
#8.draw polygons in 3d using new points
#9.change polygons to templineslist
from operator import itemgetter
import math
import createpolyfeatureclass
import createpolygon3dfeatureclass
import boundaryconditions
import sys
from os.path import expanduser,join as joinadd
import three_to_2d_v2_functions
###########################################################################
def cs_3d_to_2d(planenormalslist,mainpolylist,indextemplist_with_coords,postbottomboxlist,minsfirst,minslast,maxfirst,maxlast,prior,rawdata,epsbn_ratio,eps_ratio,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,smooth_2d):
    #sys.stdout = open('C:\Users\usuari\stdout.txt', 'w')
    #sys.stderr = open('C:\Users\usuari\stderr.txt', 'w')
    ###########################################################################
    #epsbn_ratio=0.05
    #eps_ratio=0.01
    ###########################################################################
    #determine the new coordinates and the planes cross products ax+by+cz+d=0 
    minslast_2d,maxlast_2d,maxfirst_2d,minsfirst_2d=three_to_2d_v2_functions.two_d_min_max_finder(planenormalslist,minsfirst,maxfirst,minslast,maxlast)
    ###########################################################################
    # mainpolylist from 3d to 2d and postbottombox in 2d
    mainpolylist_2d,postbottomboxlist_2d=three_to_2d_v2_functions.make_mainpolylist_2d_and_postbottombox_2d(planenormalslist,mainpolylist,postbottomboxlist,indextemplist_with_coords)
    ###########################################################################
    arcgistempdb_2d = createpolyfeatureclass.createpolyfeatureclass_2d(mainpolylist_2d,postbottomboxlist_2d,minsfirst_2d,minslast_2d,maxfirst_2d,maxlast_2d,prior,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,smooth_2d)
    ###########################################################################
    #extracting the polygons from the file to a new list:
    polygons_2d_list=three_to_2d_v2_functions.read_polygons_2d(planenormalslist,epsbn_ratio,eps_ratio)
    #polygons_2d_list = [ [polygon,[ [polygon vertics points: x,y, bhindex],...],raw data dictionary  ]
    ###########################################################################
    #preparing the rawdata
    rawdata_2d=three_to_2d_v2_functions.rawdata_2d_preparation(planenormalslist,rawdata)
    ###########################################################################    
    #polygon identifier
    polygons_2d_list=three_to_2d_v2_functions.polygon_identifier(rawdata_2d,polygons_2d_list)
    ###########################################################################
    #transfering 2d points to 3d points:
    polygns_3d=three_to_2d_v2_functions.points_2d_to_3d_transfer(polygons_2d_list,planenormalslist,epsbn_ratio,eps_ratio)
    #polygns_3d=[[0:lit ,1:polygonpoints, 2: 3dpolygon],.....]
    ###########################################################################
    createpolygon3dfeatureclass.create_3d_polygons(polygns_3d)
    ###########################################################################
    return arcgistempdb_2d, polygns_3d
