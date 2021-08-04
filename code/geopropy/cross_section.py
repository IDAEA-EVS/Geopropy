import arcpy
import sys
from operator import itemgetter
import readinginputdata
import layermerger
import boxcreator
import pointextraction
import definitelines
import secondstagelinecompleter
import createpolyfeatureclass
import createpointfeatureclass
import topolinecreator
import postbottombox
import anglefinder
import threeD_to_2d_projector_v2
import foldfaulintrusionsitunationdeterminer
import preprocess
import time
import topo_analysis
from topo_analysis import surface_pnt_process
import plane_calculator_topo_projector
import pypyodbc
########################################################################################################
def main_function(database_dir,bore_IDs,Lithology_table,box_bottom_rate= 1.1,bottomlength=15,predefined_angle_degree=None,Merge_Layers=False,bottom_box_type='normalbottombox',xshifter=0.5,yshifter=0.5,epsbn_ratio=0.05,eps_ratio=0.01,ExtendLine_edit_distance=5,TrimLine_edit_dangle_length=2,Integrate_management_distance=0.01,del_x=10,del_y=10,smooth_2d=False,gen_polygons=True):
    t_total_start=time.time()
    con_to_mdb = pypyodbc.win_connect_mdb(database_dir)
    arcpy.env.workspace=database_dir
    #arcpy.env.outputZFlag = "Enabled"
    ########################################################################################################
    '''Pre processing'''
    print "######### Pre-processing... #########"
    t0=time.time()
    bore,indextemplist,mainpolylist=preprocess.preprocessing(bore_IDs)
    t1=time.time()
    print "########## Pre-processing finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    print "######### Reading data... #########"
    t0=time.time()
    '''reading Borehole_table'''
    boidtable, x, y, elev,indextemplist_with_coords = readinginputdata.readBorehole_table(bore,xshifter,yshifter,indextemplist,con_to_mdb)
    '''reading Borehole_Litho table'''
    boid, top, bot, lit,fault_points_in_rawdata = readinginputdata.readBorehole_LithoTable(bore,boidtable,elev,Lithology_table,con_to_mdb)
    '''Read and pre - processing priority table '''
    prior = readinginputdata.readpriority_table(con_to_mdb)
    #format = [prior 0:prioroty 1:[toplayer] 2:[bottomlayer] 3:type]
    #top layer and bottom layer type is list'''
    '''reading fault_table'''
    fault_table = readinginputdata.readfault_table(prior,con_to_mdb)
    #fault_table=[ [priority_number,[ [bhid,elevation] , [bhid,elevation] , ...] ]
    #, [priority_number,[ [bhid,elevation] , [bhid,elevation] , ...] , ... ] , ...]
    '''reading surface data'''
    temp_points=readinginputdata.readtopo_points(prior,indextemplist_with_coords,del_x,del_y,con_to_mdb)
    con_to_mdb.close()
    t1=time.time()
    print "######### Reading data finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    '''merging the layers with the same Lithology and change the raw data structure'''
    if Merge_Layers==True:
        print "######### Merging layers... #########"
    rawdata = layermerger.layermerge(boid,top,bot,lit,indextemplist_with_coords,bore,Merge_Layers) #don't do the merge part when it is false
    if Merge_Layers==True:
        print "######### Merging layers finished #########"
    #########################################################################################################
    print "######### 3D plane calculator, Projecting surface points, Generating Topography and guide bottom boundary... #########"
    t0=time.time()
    '''plane calculator'''
    planenormalslist=plane_calculator_topo_projector.cross_product_and_planenormalslist_maker(indextemplist_with_coords)
    '''Projecting surface points'''
    temp_points=plane_calculator_topo_projector.surface_point_projector(planenormalslist,temp_points)

    ''' drawing the Box '''
    #ratiobottombox or normalbottombox:
    #normalbottombox find the minimum, and increase the box by a user defined ratio (consider faults)
    #ratiobottombox do it based on minimum of every borehole (consider faults)
    mainpolylist,boxpoints,rawdata = boxcreator.boxcreator2(bottom_box_type,box_bottom_rate,fault_table, rawdata,prior,mainpolylist,indextemplist_with_coords)
    ''' drawing the topo'''
    mainpolylist,maxfirst,maxlast,temp_points = topolinecreator.topolinecreator(mainpolylist,indextemplist_with_coords,prior,temp_points)
    t2=time.time()
    print "######### 3D plane calculator, Projecting surface points, Generating Topography and guide bottom boundary finished #########"
    print "Time:", t2-t0
    print "\n \n \n"
    ########################################################################################################
    '''point extraction (normal and fault poin extraction)'''
    print  "######### Point extraction... #########"
    t0=time.time()
    mainpointlist,mainpointlistreverse,point_id = pointextraction.pointextraction(rawdata,prior,indextemplist_with_coords,x,y,boidtable,fault_table,elev)
    #mainpointlist=[0=point_id, 1=index, 2=bhid, 3=priority, 4=type, 5=coordinates,
    #6=connectedleft point id, 7=connectedright point id, 8=pointcode ]
    #pointcodes:
    #   0 = not connected
    #   1 = just left connected
    #   2 = just right connected
    #   3 = fully connected'''
    t1=time.time()
    print  "######### Point extraction finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    #################################################################
    '''topography reading data and processing'''
    print "####topography reading data and processing####"
    t0=time.time()
    #to read and preprocess the surface data. Also to produce the maintopolist
    mainpointlist,mainpointlistreverse,mainpolylist,maintopolist=surface_pnt_process(mainpointlist,mainpointlistreverse,mainpolylist,prior,rawdata,temp_points,indextemplist_with_coords)
    t1=time.time()
    print  "####topography reading data and processing finished####"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''Manual stage'''
    print  "######### Critical zones processing... #########"
    t0=time.time()
    mainpointlist,mainpolylist=foldfaulintrusionsitunationdeterminer.foldfaulintrusionsitunationdeterminers(mainpointlist,mainpointlistreverse,mainpolylist,prior,indextemplist_with_coords,maintopolist)
    #IMPORTANT: output mainpointlist contains mainpointlistreverse also, the point situation for all points changed back 
    t1=time.time()
    print  "######### Critical zones processing finish #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''create definite lines'''
    print  "######### Generating automatic definite lines... #########"
    t0=time.time()
    temres = definitelines.definitelines(prior,indextemplist_with_coords,mainpointlist,mainpolylist)
    mainpointlist=temres[0]
    mainpolylist=temres[1]
    t1=time.time()
    print  "######### Generating automatic definite lines finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''calculate angles'''
    print  "######### Angle processing... #########"
    t0=time.time()
    angles=anglefinder.anglefinder(mainpolylist,prior,fault_table,predefined_angle_degree)
    #angles= [ [prio_num,type, tan_angle, quantity, [ [index1,index2,startpoint,endpoint] ]   ] ,...]
    t1=time.time()
    print  "######### Angle processing finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''create lines in stage 2 '''
    print  "######### Automatic structure completion... #########"
    t0=time.time()
    mainpointlist, mainpolylist = secondstagelinecompleter.secondstagelinecompleter(mainpointlist,prior,mainpolylist,rawdata,angles,indextemplist_with_coords)
    t1=time.time()
    print  "######### Automatic structure completion finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''post bottom box'''
    print  "######### Ultimate bottom boundary... #########"
    t0=time.time()
    intersectionpoints, postbottomboxlist,minsfirst,minslast= postbottombox.postbottombox(mainpolylist,mainpointlist,indextemplist_with_coords,bottomlength)
    t1=time.time()
    print  "######### Ultimate bottom boundary finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    '''Create point and polylines in 3d'''
    print  "######### Creating 3D point and layers (polylines) database... #########"
    t0=time.time()
    pfcadd=createpointfeatureclass.createpointfeatureclass(boxpoints,mainpointlist,intersectionpoints, postbottomboxlist,indextemplist_with_coords[-1][1])
    arcgistempdb=createpolyfeatureclass.createpolyfeatureclass(mainpolylist,pfcadd,postbottomboxlist,minsfirst,minslast,maxfirst,maxlast,prior)
    t1=time.time()
    print  "######### Creating 3D point and layers (polylines) database finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    #This is to stop the algorithm in case the user doesn't want the polygons
    if gen_polygons==False:
        print "'gen_polygons' variable is False. In case of need to 3D polygons and/or 2D lines and polygons, set 'gen_polygons' to True"
        sys.exit()
    ########################################################################################################
    '''This function make the 3d polygons between boreholes individually, then merge them'''
    print  "######### 3D to 2D Convertion, polygon determiner, 2D cross-section maker, 3D polygon database generator... #########"
    t0=time.time()
    #epsbn_ratio=0.05
    #eps_ratio=0.01
    arcgistempdb_2d, polygns_3d = threeD_to_2d_projector_v2.cs_3d_to_2d(planenormalslist,mainpolylist,indextemplist_with_coords,postbottomboxlist,minsfirst,minslast,maxfirst,maxlast,prior,rawdata,epsbn_ratio,eps_ratio,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,smooth_2d)
    t1=time.time()
    print  "######### 3D to 2D Convertion, polygon determiner, 2D cross-section maker, 3D polygon database generator finished #########"
    print "Time:", t1-t0
    print "\n \n \n"
    ########################################################################################################
    print "Total time:"
    t_total_end=time.time()
    print t_total_end-t_total_start
    print "\n \n \n"
    ########################################################################################################
    #return pfcadd,arcgistempdb, mainpolylist,mainpointlist,indextemplist,prior,fault_table,rawdata,angles,arcgistempdb_2d
    #return arcgistempdb,arcgistempdb_2d, mainpolylist,mainpointlist,indextemplist,prior,fault_table,rawdata,angles
    #return pfcadd,arcgistempdb, mainpolylist,mainpointlist,indextemplist,prior,fault_table,rawdata
    return
########################################################################################################
def cross_section(database_dir,bore_IDs,Lithology_table,box_bottom_rate= 1.1,bottomlength=15,predefined_angle_degree=None,Merge_Layers=False,bottom_box_type='normalbottombox',xshifter=0.5,yshifter=0.5,epsbn_ratio=0.05,eps_ratio=0.01,ExtendLine_edit_distance=5,TrimLine_edit_dangle_length=2,Integrate_management_distance=0.01,del_x=10,del_y=10,smooth_2d=False,gen_polygons=True,developer_mode=True):
    """
    #######################################################################################################################################
                            ############# Main Function Description #############\n\n
    newalgorithm2 function generate geological cross sections in 3D in 3 stages based on the available data.
    X coordination of introduced boreholes have to be increasing.\n\n
    ########################################################################################################################################
    ########################################################################################################################################
                            ############# Main Function default variables #############\n\n
    18 variables\n\n
    database_dir= A string to define Hydor geodatabase direction (.mdb) \n                   
    bore_IDs= A python list contains borehole ids (string). \n
    Lithology_table= Table in database that corresponds to geological units in boreholes \n
    box_bottom_rate= 1.1 (default) optional\n
    bottomlength=15 (default) optional\n
    predefined_angle_degree=None in degrees (default) optional\n
    Merge_Layers={False(default),True} optional \n
    bottom_box_type={'normalbottombox' (default),'ratiobottombox'} optional\n
    xshifter=0.5 (default) optional --Shift borehole x coordination in case it is same as previous borehole by xshifter amount\n
    yshifter=0.5 (default) optional --Shift borehole y coordination in case it is same as previous borehole by yshifter amount\n
    epsbn_ratio=0.05 (default) optional --A ratio based on borehole distance for 3D to 2D convertion of the points in boundary of the cross section\n   
    eps_ratio=0.01 (default) optional --A ratio based on borehole distance for 3D to 2D convertion of the points everywhere except in boundary of the cross section\n
    ExtendLine_edit_distance=5 (default) optional --The maximum distance a line segment can be extended to an intersecting feature. Refer to arcpy.ExtendLine_edit function for more info\n
    TrimLine_edit_dangle_length=2 (default) optional --Line segments that are shorter than the specified Dangle Length and do not touch another line at both endpoints (dangles) will be trimmed. Refer to arcpy.TrimLine_edit function for more info\n
    Integrate_management_distance=0.01 (default) optional --The distance that determines the range in which feature vertices are made coincident. To minimize undesired movement of vertices, the x,y tolerance should be fairly small. Refer to arcpy.Integrate_management function for more info \n
    del_x=10 (default) optional -- The radius in X axis to project surface point to 3D cross sections \n
    del_y=10 (default) optional -- The radius in Y axis to project surface point to 3D cross sections \n
    smooth_2d=False (default) optional --if true, a smoothed version of 2d cross section will be generated also \n
    gen_polygons=True (default) optional --if false, the procedure stops after generating 3d lines! This means 2D cross section is not gonna be generated also.\n
    developer_mode=True (default) optional --if false, the error handling is more general and with less details
    ########################################################################################################################################
    ########################################################################################################################################
    """
    if developer_mode==True:
        main_function(database_dir,bore_IDs,Lithology_table,box_bottom_rate,bottomlength,predefined_angle_degree,Merge_Layers,bottom_box_type,xshifter,yshifter,epsbn_ratio,eps_ratio,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,del_x,del_y,smooth_2d,gen_polygons)    
    elif developer_mode==False:
        try:
            main_function(database_dir,bore_IDs,Lithology_table,box_bottom_rate,bottomlength,predefined_angle_degree,Merge_Layers,bottom_box_type,xshifter,yshifter,epsbn_ratio,eps_ratio,ExtendLine_edit_distance,TrimLine_edit_dangle_length,Integrate_management_distance,del_x,del_y,smooth_2d,gen_polygons)
        except:
            print "Database, Input or internal error, for the details set 'developer_mode' to true "