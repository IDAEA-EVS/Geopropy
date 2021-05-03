from operator import itemgetter
import criticalzonefunctions
import copy
import auto_reverse_fault_function
from zone_decision_to_auto_or_manual import zone_decision_to_auto_or_manual
from criticalzonefunctions import surf_temp_list, surface_point_manual_stage_merge
def foldfaulintrusionsitunationdeterminers(mainpointlist,mainpointlistreverse,mainpolylist,prior,indextemplist_with_coords,maintopolist):
    '''
    The goal of this function is to determine the situation of points with the
    same priority based on their polarity and location, being an intrusion or
    fold or a reverse fault

    the predicted procedure is :
    first, for every priority existed in mainpointlistreverse, extract the
    number of reverse and normal priorities and organize the points in every
     borehole.

    then, extract the beggining and ending of the abnormality region. (note that
     in the same priority, it could be more than one)

    then
    for every abnormality,
        check if there is a (reverse)fault in the same region.
            if there is a reverse polarity there also
            if yes, show every side of the fault independently to the user
            if no, automaticreversefault=True

        If the proirity is an intrusion, print the specification of the points
        and ask for instructions for that region from user.

        if not, the point is probably a fold. in this scenario:
            calculate the maximum possibilities
            interrupt the program by asking user if they want to determine the
            lines manualy or based on number of possibilities.
    if the abnormality was an intrusion, or a fold that draw manualy, set a
    priority to the abnormality point so other structures can not interfere with
    it, then correct the point situations for further line creations. note that
    in the end, after finishing the process, the priorities have to change to
    original so that the procedure of lines migrating and next steps will be
    done correctly
    ############################################
    ############################################
    pointsbypriority=[
        [
            0:priority_num,
            1:[
                [
                    0:bh_index,
                    1: number of normal polaroties in bh,
                    2:number of reverse polaroties in bh,
                    3:[ #points
                        [
                            0:normal(0) or reverse(1),
                            1:x,
                            2:y,
                            3:z,
                            4:point_id
                        ],[...],...
                    ]
                ],[...],...
            ],
            2:priority type,
            3:[ #zone information
                [
                    0:[bh index that are in critical zone]
                    1:[box boundary list - 5 points]
                    2:[ #faults info in critical zone
                        [ #each fault info
                            [
                                0:priority number of the fault,
                                1:[list of fault points with the same structure as mainpointlist],
                                2:[first fault point, last fault point] (like mainpointlist structure)
                            ],[...],...
                        ],[...],...
                    ]
                    3:zone type,
                    4:reserved,
                    5:reserved
                ],[...],...
            ]
        ],[...],...
    ]    
    ############################################
    ############################################
    '''
    counter_surface_points=0
    pointsbypriority=list()
    reversepointstemp=list()
    prior=sorted(prior,key=itemgetter(0),reverse=True)
    maxpriority=prior[0][0]+1 #plus one because of the topography line
    for revpoint in mainpointlistreverse: #excluding virtuals
        if revpoint[3] not in reversepointstemp and revpoint[1] not in [indextemplist_with_coords[0][1],indextemplist_with_coords[-1][1]] and revpoint[8]!=3:
            pointsbypriority.append([revpoint[3],[],revpoint[4],None])
            reversepointstemp.append(revpoint[3])
    #############################################################        
    #to add the normal points that repeats more than one time.
    for normpnts1 in mainpointlist: #excluding virtuals
        for normpnts2 in mainpointlist:
            if normpnts1 != normpnts2 and normpnts1 not in [indextemplist_with_coords[0][1],indextemplist_with_coords[-1][1]] and normpnts2 not in [indextemplist_with_coords[0][1],indextemplist_with_coords[-1][1]]:
                if normpnts1[3]==normpnts2[3]: #same prio

                    if normpnts1[1]==normpnts2[1]: #same bh

                        if normpnts1[3] not in reversepointstemp and normpnts1[8]!=3 :
                            pointsbypriority.append([normpnts1[3],[],normpnts1[4],None])
                            reversepointstemp.append(normpnts1[3])
    id_list_temp=list()
    for newpnt in pointsbypriority: #add reverse points
        reverseindextemp=list()
        for revpoint in mainpointlistreverse:
            if revpoint[3]==newpnt[0]:#same prio
                if revpoint[1] not in reverseindextemp:
                    newpnt[1].append([revpoint[1],0,0,[]])
                    reverseindextemp.append(revpoint[1])
                for newbhs in newpnt[1]:
                    if newbhs[0]==revpoint[1] and revpoint[8]!=3:
                        newbhs[3].append([1,revpoint[5][0],revpoint[5][1],revpoint[5][2],revpoint[0],revpoint[8]])
        ##############################################
        #normals that repeat more than one time
        for normpnts1 in mainpointlist:
            for normpnts2 in mainpointlist:
                if normpnts1 != normpnts2:
                    if normpnts1[3]==newpnt and normpnts2[3]==newpnt:
                        if normpnts1[1]==normpnts2[1]:
                            if normpnts1[1] not in reverseindextemp and normpnts1[8]!=3 :
                                newpnt[1].append([normpnts1[1],0,0,[]])
                                reverseindextemp.append(normpnts1[1])
                        for newbhs in newpnt[1]:
                            if newbhs[0]==normpnts1[1]:
                                if normpnts1[0] not in id_list_temp and normpnts1[8]!=3:
                                    newbhs[3].append([1,normpnts1[5][0],normpnts1[5][1],normpnts1[5][2],normpnts1[0],normpnts1[8]])
                                    id_list_temp.append(normpnts1[0])
                                if normpnts2[0] not in id_list_temp and normpnts2[8]!=3:
                                    newbhs[3].append([1,normpnts2[5][0],normpnts2[5][1],normpnts2[5][2],normpnts2[0],normpnts2[8]])
                                    id_list_temp.append(normpnts2[0])
        #count the number of reverses:
        for cntpnts in newpnt[1]:
            cntpnts[2]=len(cntpnts[3])
    #Now we add the points from mainpointlist:
    for prios in pointsbypriority:
        tempbhsrev=list()
        tempbhs=list()
        for bhss in prios[1]:
            if bhss[0] not in tempbhsrev:
                tempbhsrev.append(bhss[0])
        #to add the normal points of the reverse priority
        for normpnts in mainpointlist:
            if normpnts[3]==prios[0]:
                if normpnts[1] not in tempbhsrev and normpnts[1] not in tempbhs and normpnts1[8]!=3 :
                    tempbhs.append(normpnts[1])
                    prios[1].append([normpnts[1],0,0,[]])
                for bhs in prios[1]:
                    if bhs[0]==normpnts[1] and normpnts1[8]!=3:
                        bhs[3].append([0,normpnts[5][0],normpnts[5][1],normpnts[5][2],normpnts[0],normpnts[8]])
        #count the normal points and sort pointsbypriority :
        for cntpnts in prios[1]:
            cntpnts[1]=len(cntpnts[3])-cntpnts[2]
            cntpnts[3]=sorted(cntpnts[3],key=itemgetter(3),reverse=True)
        prios[1]=sorted(prios[1],key=itemgetter(0))
    #sort pointsbypriority from high to low
    pointsbypriority=sorted(pointsbypriority,key=itemgetter(0),reverse=True)

    #############################################################################
    #############################################################################
    ''' the pointsbypriority list have all the points that have a priority that
     is reversed, and the points with the same priority that is more than one in
      a borehole.'''
    #identifing critical zones!
    for prios in pointsbypriority:
        bhid_list=list()
        zones=list()
        newzone=list()
        for bhs in range(0,len(prios[1])):
            if bhs not in [0,len(prios[1])-1]: #not for the first and last bh
                if prios[1][bhs][1]+prios[1][bhs][2] >1 or prios[1][bhs][2]>0 : #more than one reverse or more than one
                    if prios[1][bhs-1][0] not in bhid_list: #new zone
                        if len(newzone)!=0:
                            zones.append([newzone,[],[],None,None,None])
                        newzone=list()
                        bhid_list.append(prios[1][bhs][0])
                        newzone.append(prios[1][bhs][0])
                        if prios[1][bhs-1][0]==prios[1][bhs][0]-1:
                            if prios[1][bhs-1][1]+prios[1][bhs-1][2]>0: #previous bh
                                bhid_list.append(prios[1][bhs-1][0])
                                newzone.append(prios[1][bhs-1][0])
                        if prios[1][bhs+1][0]==prios[1][bhs][0]+1:        
                            if prios[1][bhs+1][1]+prios[1][bhs+1][2]>0: #next bh
                                bhid_list.append(prios[1][bhs+1][0])
                                newzone.append(prios[1][bhs+1][0])
                    else: #add to the existed zone (next borehole, because the main borehole already added in the previous iteration)
                        if prios[1][bhs+1][0]==prios[1][bhs][0]+1:   
                            if prios[1][bhs+1][1]+prios[1][bhs+1][2]>0: #next bh
                                bhid_list.append(prios[1][bhs+1][0])
                                newzone.append(prios[1][bhs+1][0])
            elif bhs==0:
                if prios[1][bhs][1]+prios[1][bhs][2]>1 or prios[1][bhs][2]>0:
                    newzone=list()
                    bhid_list.append(prios[1][bhs][0])
                    newzone.append(prios[1][bhs][0])
                    if prios[1][bhs+1][1]+prios[1][bhs+1][2]>0: #next bh
                        bhid_list.append(prios[1][bhs+1][0])
                        newzone.append(prios[1][bhs+1][0])
            elif bhs==len(prios[1])-1: #last bh
                if prios[1][bhs][1]+prios[1][bhs][2] >1 or prios[1][bhs][2]>0 :
                    if prios[1][bhs-1][0] not in bhid_list:
                        if len(newzone)!=0:
                            zones.append([newzone,[],[],None,None,None])
                        newzone=list()
                        bhid_list.append(prios[1][bhs][0])
                        newzone.append(prios[1][bhs][0])
                        if prios[1][bhs-1][1]+prios[1][bhs-1][2]>0: #previous bh
                            bhid_list.append(prios[1][bhs-1][0])
                            newzone.append(prios[1][bhs-1][0])
                    else: #if the last bh is already in bhid_list, there is no need to do anything
                        pass
                zones.append([newzone,[],[],None,None,None]) #to append the last newzone
        prios[3]=zones
    pointsbypriority=sorted(pointsbypriority,key=itemgetter(0),reverse=True)
    #############################################################################
    '''
    Now we know the critical prioroties, and critical points.
    next step is making desicions about further procedure of trating as a fault, fold or intrusion.

    '''
    #############################################################################
    #extracting the fault points from mainpointlist:
    faultpoint=list()
    for priority in prior:
        if priority[3]=="fault":
            faultpoint.append([priority[0],[],None])
    for fault in faultpoint:
        faultfirstp=None
        faultlastp=None
        for points in mainpointlist:
            if points[3]==fault[0]: #same prio
                fault[1].append(points)
                if faultfirstp==None or faultfirstp[1]>points[1]:
                    faultfirstp=points
                if faultlastp==None or faultlastp[1]<points[1]:
                    faultlastp=points
        fault[2]=[faultfirstp,faultlastp]
    faultpoints=list()
    for fault in faultpoint: # we just consider faults with more than one points
        if len(fault[1]) > 1:
            faultpoints.append(fault)
    #############################################################################
    #main processing
    manual_all_intersection=None #to check the intersection in manual lines
    cnt_whole=0
    for criticals in pointsbypriority: #processing
        #############################################
        #make a temporary list of manual surface zones that are "manual_topo"
        temp_surface_list=surf_temp_list(criticals[0],maintopolist)
        #############################################
        for zone in criticals[3]: #we are in each critical zone from now on
            zonepnts=list()
            if len(zone[0]) !=1: #if the critical zone is not just one borehole
                firstbh=zone[0][0]
                lastbh=zone[0][-1]
                pnt_highz=None
                pnt_lowz=None
                for BHZONE in zone[0]:
                    for bhs in criticals[1]:
                        if bhs[0]==BHZONE:
                            for pnt in bhs[3]:
                                zonepnts.append([BHZONE,pnt[0],pnt[1],pnt[2],pnt[3],pnt[4],pnt[5],"Borehole_points"])
                                if pnt_highz==None or pnt_highz<pnt[3]:
                                    pnt_highz=pnt[3]
                                if pnt_lowz==None or pnt_lowz>pnt[3]:
                                    pnt_lowz=pnt[3]
                #extract the x and y of the first and last bh:
                for ind in indextemplist_with_coords:
                    if ind[1]==firstbh:
                        xnpre=ind[2]
                        ynpre=ind[3]
                    elif ind[1]==lastbh:
                        xnnex=ind[2]
                        ynnex=ind[3]
                first_bh_pnt_highz=[criticals[0],firstbh,xnpre,ynpre,pnt_highz,"virtual"]
                last_bh_pnt_highz=[criticals[0],lastbh,xnnex,ynnex,pnt_highz,"virtual"]
                last_bh_pnt_lowz=[criticals[0],lastbh,xnnex,ynnex,pnt_lowz,"virtual"]
                first_bh_pnt_lowz=[criticals[0],firstbh,xnpre,ynpre,pnt_lowz,"virtual"]
                #zone[1]=[first_bh_pnt_highz, last_bh_pnt_highz, last_bh_pnt_lowz, first_bh_pnt_lowz, first_bh_pnt_highz]
                #####################################################################
            else: #critical zone is just one bh (for sure more than one point)
                #find the distance between max and min ,control the man bh, next and previous one in that z.
                bh=zone[0]
                prevbh=bh-1
                nextbh=bh+1
                for bhs in criticals[1]:
                    if bhs[0]==bh:
                        for pnt in bhs[3]:
                            zonepnts.append([bh,pnt[0],pnt[1],pnt[2],pnt[3],pnt[4],pnt[5],"Borehole_points"])
                            zup=None
                            zdon=None
                            if zup==None or zup[4]<pnt[3]:
                                zup=[criticals[0],bh,pnt[1],pnt[2],pnt[3],"virtual"]
                            if zdon==None or zdon[4]>pnt[3]:
                                zdon=[criticals[0],bh,pnt[1],pnt[2],pnt[3],"virtual"]
                zdist=abs(zup[4]-zdon[4])
                #extract the x and y of the next and prev bh:
                for ind in range(0,len(indextemplist_with_coords)):
                    if indextemplist_with_coords[ind][1]==prevbh:
                        xnpre=indextemplist_with_coords[ind][2]
                        ynpre=indextemplist_with_coords[ind][3]
                    elif indextemplist_with_coords[ind][1]==nextbh:
                        xnnex=indextemplist_with_coords[ind][2]
                        ynnex=indextemplist_with_coords[ind][3]
                    elif indextemplist_with_coords[ind]==bh:
                        xthat=indextemplist_with_coords[ind][2]
                        ythat=indextemplist_with_coords[ind][3]
                    xnpre=float(xthat-xnpre)/3+xnpre
                    ynpre=float(ythat-ynpre)/3+ynpre
                    xnnex=float(xnnex-xthat)/3+xthat
                    ynnex=float(ynnex-ythat)/3+ythat     
                first_bh_pnt_highz=[criticals[0],prevbh,xnpre,ynpre,zup[4]+float(zdist)/3,"virtual"]
                first_bh_pnt_lowz=[criticals[0],prevbh,xnpre,ynpre,zdon[4]-float(zdist)/3,"virtual"]
                last_bh_pnt_highz=[criticals[0],nextbh,xnnex,ynnex,zup[4]+float(zdist)/3,"virtual"]
                last_bh_pnt_lowz=[criticals[0],nextbh,xnnex,ynnex,zdon[4]-float(zdist)/3,"virtual"]
            zone[1]=[first_bh_pnt_highz, last_bh_pnt_highz, last_bh_pnt_lowz, first_bh_pnt_lowz, first_bh_pnt_highz]
            #we also have zones which is the points in every zone.[bhind,normor reverse, x,y,z,id]
            #fault
            fault_criticalzone_intersection=False
            faultswithinter=list()
            for fault in faultpoints:
                if fault[0]>criticals[0]: #priority check
                    #zone[1]=[first_bh_pnt_highz, last_bh_pnt_highz, last_bh_pnt_lowz, first_bh_pnt_lowz, first_bh_pnt_highz]
                    if (fault[2][0][1] <= zone[1][0][1] and fault[2][1][1] <= zone[1][0][1]) or (fault[2][0][1] >= zone[1][1][1] and fault[2][1][1] >= zone[1][1][1]) or (fault[2][0][5][2] <= zone[1][2][4] and fault[2][1][5][2] <= zone[1][2][4]) or (fault[2][0][5][2] >= zone[1][0][4] and fault[2][1][5][2] >= zone[1][0][4]):
                        #if both bhind more or less than critical zone or if z of both points are higher or lower than critical zone
                        pass
                    else:
                        fault_criticalzone_intersection=True
                        faultswithinter.append([fault[0],fault[1]])
            ########################################################################
            #surface_point_manual_stage_merge: add or merge critical zones
            zone,temp_surface_list,counter_surface_points,zonepnts=surface_point_manual_stage_merge(zone,temp_surface_list,zonepnts,counter_surface_points)
            ########################################################################
            #The procedure to see if we use auto reverse fault function or not!        
            zone[2]=faultswithinter
            if len(faultswithinter)==1 and zone[4]!="manual_zone_surface_points_merged": #auto reverse fault detection
            #Zones that there is just 2 point
                autoflt=True
                for fltpnt in faultswithinter[0][1]:
                    if autoflt==True:
                        for cricpoints in criticals[1]:
                            if autoflt==True and cricpoints[0]==fltpnt[1]: #bh index check
                                if cricpoints[1]<3 and cricpoints[2]==0: #number of normal and reverse in bh check it can be one or 2 normal points
                                    for pntts in range(0,len(cricpoints[3])-1):
                                        if fltpnt[5][2]>cricpoints[3][pntts][3] or fltpnt[5][2]<cricpoints[3][pntts+1][3]: #z coord check
                                            autoflt=False
                                else:
                                    autoflt=False
                if autoflt==True:
                    zone[3]="auto_reverse_fault"
                else:
                    zone[3]="manual_reverse_fault"
            elif len(faultswithinter)>1 and zone[4]!="manual_zone_surface_points_merged": #more than one fault
                zone[3]="manual_reverse_fault"
            else: #no fault
                #fold or intrusion or topo points
                #intrusion:
                if zone[4]=="manual_zone_surface_points_merged":
                    zone[3]="manual_zone_surface_points_merged"
                elif criticals[2]=="intrusion":
                    zone[3]="manual_intrusion"
                else:
                    zone[3]="manual_fold"
            ###################################################
            #zone type determined, now using printandinputdata function in criticalzonefunctions.py, we interrupt the user and ask for new data
            #This also checks for intersection between user defined lines and if there are any intersections, it asks user again.
            #prior_num=criticals[0]
            #prior_type=criticals[2]
            mainpolylist,mainpointlistreverse,mainpointlist,manual_all_intersection,cnt_whole=zone_decision_to_auto_or_manual(mainpointlist,mainpointlistreverse,mainpolylist,zone,criticals[0],criticals[2],indextemplist_with_coords,maxpriority,zonepnts,manual_all_intersection,cnt_whole)

        #here, the temp_surface_list have to be checked, for false values, and incase there is some, they have to be added to zone list as an individual critical zones to process
        #for that, the lines above (382:445) can be converted to a function to reuse here
        #we have to prepare zones 
        #box points
        ###################
        #we have to prepare zonepnts
        '''
        temp_surface_list=[
            [
                0:#left borehole index
                1:#surface points
                2:#borehole points
                3: False or merged #situation
            ],[...],...
        ]
        '''
        for bhpair in temp_surface_list:
            if bhpair[3]==False: #if not merged
                #boundaries:
                for ind in indextemplist_with_coords:
                    if ind[1]==bhpair[0]:
                        xnpre=ind[2]
                        ynpre=ind[3]
                        znpre=ind[4]
                    elif ind[1]==bhpair[0]+1:
                        xnnex=ind[2]
                        ynnex=ind[3]
                        znnex=ind[4]
                #finding the minimum of boundary and appending bhs to znpnts:
                zonepnts=list()
                ###########
                z_high=max(znnex,znpre)
                z_down=z_high
                for pnt_surf in bhpair[2]:
                    if pnt_surf!=None:
                        if pnt_surf[3]<z_down:
                            z_down=pnt_surf[3]
                        if pnt_surf[5]=="reverse":
                            pol=1
                        else:
                            pol=0       
                        zonepnts.append([pnt_surf[0],pol,pnt_surf[1],pnt_surf[2],pnt_surf[3],pnt_surf[8],pnt_surf[6],"Borehole_points"])
                first_bh_pnt_highz=[criticals[0],bhpair[0],xnpre,ynpre,z_high,"virtual"]
                last_bh_pnt_highz=[criticals[0],bhpair[0]+1,xnnex,ynnex,z_high,"virtual"]
                last_bh_pnt_lowz=[criticals[0],bhpair[0]+1,xnnex,ynnex,z_down,"virtual"]
                first_bh_pnt_lowz=[criticals[0],bhpair[0],xnpre,ynpre,z_down,"virtual"]

                ###########################
                new_z=[
                   [bhpair[0],bhpair[0]+1], #bhindexes
                   [first_bh_pnt_highz, last_bh_pnt_highz, last_bh_pnt_lowz, first_bh_pnt_lowz, first_bh_pnt_highz], #boundaries
                   [], #faults
                   "manual_zone_surface_points_selfstand", #zone type
                   None,
                   None
                ]
                #################################
                
                for pnt_surf in bhpair[1]:
                    if pnt_surf[5]=="reverse":
                        pol=1
                    else:
                        pol=0 
                    counter_surface_points=counter_surface_points-1          
                    zonepnts.append(
                        [
                            pnt_surf[0], #point ind
                            pol, #polarity
                            pnt_surf[1], #x
                            pnt_surf[2], #y
                            pnt_surf[3], #z
                            counter_surface_points, #it has to be point id
                            -1, #polarity
                            "Surface_points"
                        ]
                    )
                mainpolylist,mainpointlistreverse,mainpointlist,manual_all_intersection,cnt_whole=zone_decision_to_auto_or_manual(mainpointlist,mainpointlistreverse,mainpolylist,new_z,criticals[0],criticals[2],indextemplist_with_coords,maxpriority,zonepnts,manual_all_intersection,cnt_whole)
                bhpair[3]="selfstand"

    #to change the priority to normal one:
    for poliesss in mainpolylist:
        for kk in range(0,len(poliesss[2])):
            if poliesss[2][kk][0]==maxpriority+1:
                poliesss[2][kk]=[poliesss[2][kk][5],poliesss[2][kk][6],poliesss[2][kk][2],poliesss[2][kk][3],poliesss[2][kk][4]]
    mainpointlist=mainpointlist+mainpointlistreverse

    return mainpointlist,mainpolylist
