
from operator import itemgetter
from segmentlineintersection3d import segmentlineintersection3d
import criticalzonefunctions
import copy
import auto_reverse_fault_function
def zone_decision_to_auto_or_manual(mainpointlist,mainpointlistreverse,mainpolylist,zone,prior_num,prior_type,indextemplist_with_coords,maxpriority,zonepnts,manual_all_intersection,cnt_whole):
    #prior_num=criticals[0]
    #prior_type=criticals[2]
    #zone type determined, now using printandinputdata function in criticalzonefunctions.py, we interrupt the user and ask for new data
    #This also checks for intersection between user defined lines and if there are any intersections, it asks user again.
    cnt=0
    intersec=True
    while intersec==True:
        cnt=cnt+1
        cnt_whole=cnt_whole+1
        if zone[3]=="auto_reverse_fault":
            mainpolylist2=copy.deepcopy(mainpolylist)
            mainpointlist2=copy.deepcopy(mainpointlist)
            mainpointlistreverse2=copy.deepcopy(mainpointlistreverse)
            mainpolylist2,mainpointlist2,faultsit,temporary_manual_list=auto_reverse_fault_function.rev_fault_fun(prior_num,prior_type,mainpointlistreverse2,mainpolylist2,mainpointlist2,zonepnts,zone[2],zone[0],indextemplist_with_coords,maxpriority)
            zone[3]=faultsit
            intersec=False
            if cnt_whole==1 and faultsit=="auto_reverse_fault":
                mainpointlist=mainpointlist2
                mainpointlistreverse=mainpointlistreverse2
                mainpolylist=mainpolylist2
                manual_all_intersection=temporary_manual_list
            else:
                #if we are using the auto reverse fault function, and the generated fault have intersection
                # with the lines that made before, then the algorithm change from auto to manual
                if faultsit=="auto_reverse_fault":
                    for poltemp in temporary_manual_list:
                        if intersec==False: #for less loops
                            for polpri in manual_all_intersection:
                                intersectionss=segmentlineintersection3d(poltemp,polpri)
                                if intersectionss != False:
                                    intersec=True
                                    zone[3]="auto_to_manual_reverse_fault"
                    if intersec==False:
                        manual_all_intersection.extend(temporary_manual_list)
                        mainpointlist=mainpointlist2
                        mainpointlistreverse=mainpointlistreverse2
                        mainpolylist=mainpolylist2
                    intersec=False
        ###################################################    
        if zone[3] in ["manual_reverse_fault","manual_intrusion","manual_fold","auto_to_manual_reverse_fault","manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]:
            if cnt_whole==1:
                mainpointlist,mainpointlistreverse,mainpolylist,temporary_manual_list=criticalzonefunctions.printandinputdata(prior_num,prior_type,zone[1],zonepnts,maxpriority,indextemplist_with_coords,mainpolylist,mainpointlist,mainpointlistreverse,zone[2],zone[3])
                manual_all_intersection=temporary_manual_list
                del temporary_manual_list
                intersec=False
            else:
                if cnt>1:
                    print " \n #WARNING# \n \nINTERSECTION IN USER DEFINED LINES. PLEASE INTRODUCE THE POINTS AGAIN"
                mainpolylist2=copy.deepcopy(mainpolylist)
                mainpointlistreverse2=copy.deepcopy(mainpointlistreverse)
                mainpointlist2=copy.deepcopy(mainpointlist)
                mainpointlist2,mainpointlistreverse2,mainpolylist2,temporary_manual_list=criticalzonefunctions.printandinputdata(prior_num,prior_type,zone[1],zonepnts,maxpriority,indextemplist_with_coords,mainpolylist2,mainpointlist2,mainpointlistreverse2,zone[2],zone[3])
                #check for intersection between temporary_manual_list and the old ones
                intersec=False
                for poltemp in temporary_manual_list:
                    if intersec==False: #for less loops
                        for polpri in manual_all_intersection:
                            intersectionss=segmentlineintersection3d(poltemp,polpri)
                            if intersectionss != False:
                                intersec=True
                if intersec==False:
                    manual_all_intersection.extend(temporary_manual_list)
                    mainpointlist=mainpointlist2
                    mainpointlistreverse=mainpointlistreverse2
                    mainpolylist=mainpolylist2
                del temporary_manual_list
    return mainpolylist,mainpointlistreverse,mainpointlist,manual_all_intersection,cnt_whole