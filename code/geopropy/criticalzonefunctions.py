#extract point sits and dictionary
#this function have to be used when the mainpointlist and mainpointlistreverse
# is updated.it updated the points situation, then updates the dictionary.
import same_prio_bh_rev_layer_connector
from operator import itemgetter
from tabulate import tabulate
import copy
from segmentlineintersection3d import segmentlineintersection3d

def surface_point_manual_stage_merge(zone,temp_surface_list,zonepnts,counter_surface_points):
                for prio_in_topo in temp_surface_list: 
                    if  prio_in_topo[3]==False and (prio_in_topo[0] in zone[0] or prio_in_topo[0]-1 in zone[0]):
                        #add manual topo points to 
                        prio_in_topo[3]="merged" #indicate in surface points that is is already merged!
                        zone[4]="manual_zone_surface_points_merged"
                        for pnt_surf in prio_in_topo[1]: #surface points
                            if pnt_surf[5]=="reverse":
                                pol=1
                            else:
                                pol=0
                            ##topopoints=bhpairs[4]=topo_pnt_ind,'X','Y','Z','Type',polarity,angle,0,reserved=None    
                            counter_surface_points=counter_surface_points-1      
                            zonepnts.append(
                                [
                                    prio_in_topo[0], #bhind
                                    pol, #polarity
                                    pnt_surf[1],#x
                                    pnt_surf[2],#y
                                    pnt_surf[3],#z
                                    counter_surface_points,
                                    -1, #point sit for surface
                                    "Surface_points"])
                        id_temp=list()
                        for ii in zonepnts:
                            id_temp.append(ii[5])
                        for bh_pnts in prio_in_topo[2]: #bh points
                            if bh_pnts!=None and bh_pnts[8] not in id_temp:
                                if pnt_surf[5]=="reverse":
                                    pol=1
                                else:
                                    pol=0
                                zonepnts.append([bh_pnts[0],pol,bh_pnts[1],bh_pnts[2],bh_pnts[3],bh_pnts[8],pnt_surf[6],"Borehole_points"])
                                id_temp.append(bh_pnts[8])
                return zone,temp_surface_list,counter_surface_points,zonepnts
##########################################################
def surf_temp_list(priority_num,maintopolist):
            temp_surface_list=list()
            for tp in maintopolist:
                if tp[0]==priority_num:
                    for bh_pair in tp[2]:
                        if bh_pair[6][0]=="manual_topo_point":
                            temp_surface_list.append(
                                [
                                    bh_pair[0], #left borehole index
                                    bh_pair[4], #surface points
                                    bh_pair[5], #borehole points
                                    False #situation
                                ]
                            )
            return temp_surface_list  
##########################################################              
def sitpointdic(mainpointlist,mainpointlistreverse,rev_same_bh):
    #updating the point situation
    #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
    for bhss in rev_same_bh:
        sitpointdic={'leftconnected' : 0 , 'rightconnected' : 0, 'zerozero' : 0, 'rest' : 0 }
        for pairpnts in bhss[1]:
            for ii in mainpointlist+mainpointlistreverse:
                if ii[0]==pairpnts[0][6]: #point id
                    if len(pairpnts[0])==6:
                        pairpnts[0].append(ii[8])
                    else:
                        pairpnts[0][5]=ii[8]

                elif pairpnts[1]==None:
                    pass

                elif ii[0]==pairpnts[1][6]:
                    if len(pairpnts[1])==6:
                        pairpnts[1].append(ii[8])
                    else:
                        pairpnts[1][5]=ii[8]

            #updating dictionary ( by regenerating)
            if pairpnts[1]==None or [pairpnts[0][5],pairpnts[1][5]]==[0,0]:
                sitpointdic["zerozero"]=sitpointdic.get("zerozero", 0)+1
            elif [pairpnts[0][5],pairpnts[1][5]] in [[0,1],[1,1],[1,0] ]:
                sitpointdic["leftconnected"]=sitpointdic.get("leftconnected", 0)+1
            elif [pairpnts[0][5],pairpnts[1][5]] in [ [0,2],[2,0],[2,2] ]:
                sitpointdic["rightconnected"]=sitpointdic.get("rightconnected", 0)+1
            else:
                sitpointdic["rest"]=sitpointdic.get("rest", 0)+1
        bhss[2]=sitpointdic
    return rev_same_bh
#######################
#######################
#The following function applies to every critical zone in every priority and in
#case theere is any need for new input, it will interrupt the program and  ask
#the user for it.
def printandinputdata(priority,priority_type,box_points_list,zonepnts,maxpriority,indextemplist_with_coords,mainpolylist,mainpointlist,mainpointlistreverse,all_faults,zone_type):
    #box_points_list=zone[1]
    #all_faults=zone[2]
    #zone_type=zone[3]
    temporary_manual_list=list()
    manualzone_priority=maxpriority+1
    #zonepnts=[bhind,normor reverse, x,y,z,id]
    if len (zonepnts)>1:
        print "\n##########################################################################################\n##########################################################################################\n##########################################################################################\nStructure Determination"
        print "priority:", priority
        print "priority_type" ,priority_type
        print "\n###########\nzone box:"

        print tabulate([box_points_list[i][2:5] for i in range(0,4)] ,headers=["X","Y","Z"], tablefmt='orgtbl')    
        print "#############################################"
        print "### RELATED FAULTS ###"
        if len(all_faults)!=0:
            for i in all_faults:

                print "fault prioroty:", i[0]
                print "fault points:"

                print tabulate([ [ j[2], j[5],j[0] ] for j in i[1] ],headers=["BOREHOLE_ID", "[X,Y,Z]", "POINT_ID"], tablefmt='orgtbl' )
        else:
            print "No related fault detected"
        print "\n#############################################\n### ZONE INFORMATION ###\n"
        #print "BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID\n"
        points_temp=list()
        points_temptt=list()
        points_temp_id=['SEPARATE']
        for i in zonepnts:
            #print "zonepnts"
            #print i
            for ind in indextemplist_with_coords:
                if ind[1]==i[0]:
                    id=ind[0]
            if i[1]==0:
                pol="Normal"
            else:
                pol="Reverse"
            if i[6]==0: pnt_sit="Not Connected"
            elif i[6]==1: pnt_sit="Left Connected"
            elif i[6]==2: pnt_sit="Right Connected"
            elif i[6]==3: pnt_sit="Fully connected"
            elif i[6]==-1: pnt_sit="surface point"
            else: pnt_sit=i[6]
            #print id,i[0],[i[2],i[3],i[4]],pol,i[5]
            points_temp.append([i[7],id,i[0],[i[2],i[3],i[4]],i[1],i[6],i[5]])
            points_temptt.append([i[7],id,i[0],[i[2],i[3],i[4]],pol,pnt_sit,i[5]])
            points_temp_id.append(i[5])
        points_temp=sorted(points_temp,key=itemgetter(2))
        points_temptt=sorted(points_temptt,key=itemgetter(2))
        print tabulate(points_temptt,headers=["POINT_TYPE","BOREHOLE_ID", "BOREHOLE_INDEX", "[X,Y,Z]", "POLARITY"," POINT SIT.", "POINT_ID"], tablefmt='orgtbl')
        #for kk in points_temp:
        #    print kk
        if zone_type not in ["manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]:
            print "\n#######################################################################\n################# Stage 2: Semi-Automatic ############################\n#######################################################################\n"
            print "please introduce consecutive POINT_IDs that you wish to connect in form of a list.\n In case the critical zone consist of more than one part, write 'SEPARATE' between POINT_IDs.\n Note that the introduced points have to follow the borehole arrangement \n"
            print "In case this stage preferred to be done manually, Type:'jumptomanual'\n"
            print "EXAMPLE: [25,26,37,38,'SEPARATE',45,46,'SEPARATE',65,68] or 'jumptomanual' \n"
            
            point_id_list=None
            cnt=0
            while point_id_list==None:
                cnt=cnt+1
                if cnt!=1:
                    print 'unacceptable input!!, please refer to the example shown in previous lines!, to quit, type quit()!'
                
                point_id_list=input("Enter the POINT_ID list:")
                if type(point_id_list) !=list:
                    if point_id_list=='jumptomanual': #jump from stage 2 to 3
                        printpnts=points_temp
                        zerozero_existed=True
                    else:
                        point_id_list=None
                        print "USER INPUT IS NOT A LIST"
                elif type(point_id_list) ==list:
                    for i in point_id_list:
                        if i not in points_temp_id:
                            print i, "not in the table above, please use the point id's in the table above to illustrate the relation"
                            point_id_list=None
                            
            if point_id_list!='jumptomanual': #no jumping, analyzing stage 2
                #######################################
                #creating the lines and appending them to mainpolylist:
                rev_same_bh=list()
                printpnts=list()
                for id in range(0,len(point_id_list)-1):
                    #point_id_list=[25,26,37,38,'SEPARATE',45,46,'SEPARATE',65,68]
                    p1="SEPARATE"
                    p2="SEPARATE"
                    for k in points_temp:
                        #points_temp=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID"]
                        if k[6]==point_id_list[id]:
                            p1=k
                        elif k[6]==point_id_list[id+1]:
                            p2=k
                    if "SEPARATE" not in [p1,p2]:  #no SEPARATE
                        '''print "p1,p2"
                        print p1
                        print p2'''
                        if p1[2] !=p2[2]: #if both points are not in one borehole:
                            #print "both points are not in one borehole"
                            if p2[3][0]>p1[3][0]: #finding the first point
                                pfirst=p1
                                plast=p2
                            else:
                                pfirst=p2
                                plast=p1
                            for polies in mainpolylist: #creating polyline and changing pointsit
                                if pfirst[2]==polies[0] and plast[2]==polies[1]:
                                    #intersection check with old lines in mainpolylins (from topo)
                                    intt=False
                                    interslist=list()
                                    for check_for_inter in polies[2]:
                                        if check_for_inter[1] not in ["bottombox","Topography"]:
                                            inters=segmentlineintersection3d([pfirst[3],plast[3]],[check_for_inter[3],check_for_inter[4]])
                                            if inters!=False:
                                                interslist.append(check_for_inter)
                                                intt=True
                                    if intt==False:            
                                        polies[2].append([manualzone_priority,zone_type,None,pfirst[3],plast[3],priority,priority_type])
                                        temporary_manual_list.append([pfirst[3],plast[3]]) #append coordinations
                                        #print 'creating polyline in criticalzonefunctions not in one bh- polyline:'
                                        #change pointsit
                                        for ii in mainpointlist+mainpointlistreverse:
                                            if ii[0]==pfirst[6]:
                                                if ii[8]==0:
                                                    ii[8]=2
                                                elif ii[8]==1:
                                                    ii[8]=3
                                            elif ii[0]==plast[6]:
                                                if ii[8]==0:
                                                    ii[8]=1
                                                elif ii[8]==2:
                                                    ii[8]=3
                                    else:
                                        printpnts.append(pfirst)
                                        printpnts.append(plast)
                                        print "There is intersection between the following line and already existed lines:\n new line point ids:\n",pfirst[6],"-----",plast[6]
                                        print "old line(s) info:"
                                        for i in interslist: print i
                        else: #if both points are in one borehole
                            #print "both points are in one borehole"
                            pntexist=False
                            for bhss in rev_same_bh:
                                if len(rev_same_bh)>0 and p1[2]==bhss[0]:
                                    bhss[1].append([p1,p2])
                                    pntexist=True
                            if pntexist==False:
                                rev_same_bh.append([p1[2],[[p1,p2]],None])
                                #rev_same_bh=[[ bh , [ [p1,p2],...] ,same bh point situation],...]
                    elif id != 0 and point_id_list[id-1]==point_id_list[id+1]=="SEPARATE" and point_id_list[id] !="SEPARATE": #one point between 2 SEPARATE
                        pntexist=False
                        for bhss in rev_same_bh:
                            if len(rev_same_bh)>0 and p1[2]==bhss[0]:
                                bhss[1].append([p1,None])
                                pntexist=True
                        if pntexist==False:
                            rev_same_bh.append([p1[2],[[p1,None]],None])
                #creating the polylines for points with the same priority in the same borehole
                #rev_same_bh=[[ bh , [ [p1,p2],...],sitpointdic ],...]
                #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
                rev_same_bh=sitpointdic(mainpointlist,mainpointlistreverse,rev_same_bh)
                #print "rev_same_bh"
                #print rev_same_bh
                for bhsr in rev_same_bh:
                    same_bh_intersec=False
                    while bhsr[2]["leftconnected"]+bhsr[2]["rightconnected"] !=0 and same_bh_intersec==False:
                        for revpoints in bhsr[1]:
                            if revpoints[1]==None:
                                pass
                            elif [revpoints[0][5], revpoints[1][5]] in [ [1,0],[0,1],[1,1] ]:
                                #left connected, needs a function to connect right side (min z bh needed, next bh x and y needed),update mainpointlist and mainpointlistreverse
                                mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec=same_prio_bh_rev_layer_connector.same_prio_bh_rev_layer_connector_connect_right(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_type)
                                #intersection check with old lines in mainpolylins (from topo)
                                if same_bh_intersec==False:
                                    rev_same_bh=sitpointdic(mainpointlist,mainpointlistreverse,rev_same_bh)
                            elif [revpoints[0][5], revpoints[1][5]] in [ [2,0],[0,2],[2,2] ]:
                                #right connected, needs a function to connect left side (min z bh needed, next bh x and y needed),update mainpointlist and mainpointlistreverse
                                mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec=same_prio_bh_rev_layer_connector.same_prio_bh_rev_layer_connector_connect_left(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_type)
                                #intersection check with old lines in mainpolylins (from topo)
                                if same_bh_intersec==False:
                                    rev_same_bh=sitpointdic(mainpointlist,mainpointlistreverse,rev_same_bh)
                    if same_bh_intersec==True: #in case of intersection, append points to printpnts so they will show up in manual stage
                       #print "same_bh_intersec==True"
                        #print revpoints
                        for revpoints in bhsr[1]:
                            #print "line260criticappendprintpnts"
                            printpnts.append(revpoints[0])
                            printpnts.append(revpoints[1])
                #print the points with zero zero, and ask for further input data
                #rev_same_bh=[[ bh , [ [p1,p2],...],sitpointdic ],...]
                #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
                zerozero_existed=False
                for bhsr in rev_same_bh:
                    if bhsr[2]["zerozero"]>0:
                        zerozero_existed=True
                        #save points to print
                        for twopnts in bhsr[1]:
                            if twopnts[1]==None or [twopnts[0][5],twopnts[1][5]]==[0,0]:
                                if twopnts[0] not in printpnts:
                                    printpnts.append(twopnts[0])
                                if twopnts[1] not in printpnts and twopnts[1]!=None:
                                    printpnts.append(twopnts[1])
        
        else: #zone_type in ["manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]
            zerozero_existed=True
            printpnts=points_temp
        if zerozero_existed==True:
            #print "298:printpnts", printpnts
            ##########
            #update points_temp and printpnts
            for tnps in mainpointlist+mainpointlistreverse:
                for pri_p in printpnts:
                    if pri_p[6]==tnps[0]:
                        pri_p[5]=tnps[8]
                for pnt_tmp in points_temp:
                    if pnt_tmp[6]==tnps[0]:
                        pnt_tmp[5]=tnps[8]
            ##########
            print "\n#######################################################################\n#################Additional data needed, Stage 3:Manual ################\n#######################################################################\n"
            print "There are points which are not connected from any side to any borehole. please specify how they have to connect. Use the instruction below:\n"
            print "priority:", priority
            print "\npriority_type" ,priority_type
            print "\nIMPORTANT NOTE: FOLLOWING SAMPLE POINT INFORMATION IS JUST FOR GUIDING THE USER, DO NOT INTRODUCE THE BOREHOLE IDS IBASED ON 'ZONE INFORMATION'. INTRODUCE IDs AVAILABLE IN 'Disconnected sample points' \n "
            print "### ZONE INFORMATION ###\n"
            points_temp2=list()
            for i in points_temp:
                if i[5]==0: pnt_sit="Not Connected"
                elif i[5]==1: pnt_sit="Left Connected"
                elif i[5]==2: pnt_sit="Right Connected"
                elif i[5]==3: pnt_sit="Fully connected"
                elif i[5]==-1: pnt_sit="surface point"
                else: pnt_sit=i[5]
                if i[4]==0:
                    pol="Normal"
                else:
                    pol="Reverse"
                points_temp2.append(i[:4]+[pol]+[pnt_sit]+[i[-1]])
            print tabulate(points_temp2,headers=["POINT_TYPE","BOREHOLE_ID", "BOREHOLE_INDEX", "[X,Y,Z]", "POLARITY"," POINT SIT.", "POINT_ID"], tablefmt='orgtbl')
            print "\n######################## 3rd STAGE GUIDE ##############################\n"
            print "point IDs have to introduce in pairs, accompanied by a keyword that identify their situation:\n"
            print "If both points are in 2 CONSECUTIVE borehole or surface points: [point_id 1,point_id 2, 'normal_connection'] (point_id 1 is the sample point with smaller BOREHOLE_INDEX)\n"
            if zone_type not in ["manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]:
                print "If both points are in the same borehole, based on the side that you want them to connect: [point_id 1,point_id 2, 'same_bh_connect_left'] or [point_id 1,point_id 2, 'same_bh_connect_right']\n "
            print "If it is preferred that the program take care of a point: [point_id 1,'', 'user_skipped'] (NOT RECOMMENDED)\n"
            print "If it is preferred to introduce new coordinations and point ids, every group of lines (group of lines that are connected together) have to be introduced in different lists. the coordination of the new point and the related borehole id (if new introduced point is between two boreholes, use left side borehole id  ) have to be introduced.\n"
            print "Note that if the manual introduced structure lines going to pass the boreholes, the coordination of the point in borehole and borehole id have to be introduced .\n"
            print "structure: [ [Coord_X,Coord_Y,Coord_Z,'BOREHOLE_ID' (string)], point_id1, point_id2, [Coord_X,Coord_Y,Coord_Z,'BOREHOLE_ID' (string)],.... ] , '' , 'new_points']. Maintain sequence of the points. Note that in this part, it is possible to use points with ids that shown before. \n"
            print "################Disconnected sample points##################\n"
            #################
            printpnts2=list()
            #print printpnts
            for i in printpnts:
                if i[5]==0: pnt_sit="Not Connected"
                elif i[5]==1: pnt_sit="Left Connected"
                elif i[5]==2: pnt_sit="Right Connected"
                elif i[5]==3: pnt_sit="Fully connected"
                elif i[5]==-1: pnt_sit="surface point"
                else: pnt_sit=i[5]
                if i[4]==0:
                    pol="Normal"
                else:
                    pol="Reverse"
                printpnts2.append(i[:4]+[pol]+[pnt_sit]+[i[-1]])
            ################
            print tabulate(printpnts2,headers=["POINT_TYPE","BOREHOLE_ID", "BOREHOLE_INDEX", "[X,Y,Z]", "POLARITY"," POINT SIT.", "POINT_ID"], tablefmt='orgtbl')
            
            #ask user
            second_point_id_list=None
            cnt=0
            while second_point_id_list==None:
                cnt=cnt+1
                if cnt!=1:
                    print 'unacceptable input!!, please refer to the example shown in previous lines (3rd stage)!, to quit, type quit()!'
                second_point_id_list=input("\nEnter POINT_ID list as mentioned:\n\n")
                if second_point_id_list!="skip":
                    if type(second_point_id_list)!=list:
                        print "Introduced data is not a list!"
                        second_point_id_list=None
                    else:
                        if len(second_point_id_list)==0: pass
                        else:
                            for i in second_point_id_list:
                                if i[2] not in ['normal_connection','same_bh_connect_left','same_bh_connect_right','new_points','user_skipped']:
                                    print "error in connection type. it has to be 'normal_connection' , 'same_bh_connect_left' , 'same_bh_connect_right' , 'user_skipped' or 'new_points'"
                                    second_point_id_list=None
                                elif i[2] in  ['normal_connection','same_bh_connect_left','same_bh_connect_right'] and  (type(i[0])!=int or type(i[1])!=int):
                                    print "In 'normal_connection' , 'same_bh_connect_left' and 'same_bh_connect_right' First and second item of the list have to be point IDs "
                                    second_point_id_list=None
                                elif  i[2]=='user_skipped' and (type(i[0])!=int or i[1]!=''):
                                    print "wrong structure for 'user_skipped'"
                                    second_point_id_list=None
                                elif i[2]=="new_points":
                                    if i[1]!='':
                                        print "second item in 'new_points' list have to be empty!"
                                        second_point_id_list=None
                                    if type(i[0])!=list:
                                        print "first item in 'new_points' list have to be a list of points (point IDs or new coordination)!"
                                        second_point_id_list=None
                                    else:
                                        for ji in i[0]:
                                            if type(ji) not in (int,list):
                                                print "items inside the first item in 'new_points' list have to be a list containing [X,Y,Z,bhid (string)] or point ID !"
                                                second_point_id_list=None
                                            elif type(ji)==list:
                                                if len(ji)!=4:
                                                    print "new coordinations in 'new_points' have 4 elements: [X,Y,Z,bhid (string)] "
                                                    second_point_id_list=None
                                                elif type(ji[3])!=str:
                                                    print "borehole ids in new coordinations in 'new_points' have to be strings ex: '11' or 'ch_12'! "
                                                    second_point_id_list=None



            #deal with the new data
            #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
            if second_point_id_list=="skip":
                pass
            else:    
                for i in second_point_id_list:
                    same_bh_intersec=False
                    if i[2]=='normal_connection':
                        #find points
                        for j in printpnts:
                            if i[0]==j[6]:
                                p1=j
                            elif i[1]==j[6]:
                                p2=j
                        #########################        
                        if p1[3][0]<p2[3][0]:
                            pass
                        else:
                            p_t=copy.deepcopy(p2)
                            p2=copy.deepcopy(p1)
                            p1=p_t
                        #########################
                        #generate polylines:
                        for polies in mainpolylist:
                            #topo
                            if polies[0]==int(p1[2]) or polies[1]==int(p2[2]):
                                polies[2].append([manualzone_priority,zone_type,None,p1[3],p2[3],priority,priority_type])
                                temporary_manual_list.append([p1[3],p2[3]])
                                #update mainpointlist & mainpointlistreverse
                                #change pointsit
                                for ii in mainpointlist+mainpointlistreverse:
                                    #topo points: it updates if the points is there (which is not in case of topography)
                                    if ii[0]==p1[6]:
                                        if ii[8]==0:
                                            ii[8]=2
                                        elif ii[8]==1:
                                            ii[8]=3
                                    elif ii[0]==p2[6]:
                                        if ii[8]==0:
                                            ii[8]=1
                                        elif ii[8]==2:
                                            ii[8]=3
                    elif i[2]=='same_bh_connect_left' and zone_type not in ["manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]:
                        #find points
                        for j in printpnts:
                            if i[0]==j[6]:
                                p1=j
                            elif i[1]==j[6]:
                                p2=j
                        #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
                        revpoints=[p1,p2]
                        mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec=same_prio_bh_rev_layer_connector.same_prio_bh_rev_layer_connector_connect_left(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_type)
                    elif i[2]=='same_bh_connect_right' and zone_type not in ["manual_zone_surface_points_merged","manual_zone_surface_points_selfstand"]:
                        #find points
                        for j in printpnts:
                            if i[0]==j[6]:
                                p1=j
                            elif i[1]==j[6]:
                                p2=j
                        #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
                        revpoints=[p1,p2]
                        mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec=same_prio_bh_rev_layer_connector.same_prio_bh_rev_layer_connector_connect_right(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_type)
                                                                                                                                                                                
                    elif i[2]=='new_points':
                        #second_point_id_list=[[old_point_id1,old_point_id2],[new_point_X,new_point_Y,new_point_Z],'new_point']
                        #find points
                        for newpnts in range(0,len(i[0])-1):
                            pntcord=list()
                            norm_temp_1=False
                            norm_temp_2=False
                            if type(i[0][newpnts])==int: #point 1 id
                                if i[0][newpnts]>=0:
                                    for iii in mainpointlist+mainpointlistreverse:
                                        if iii[0]==i[0][newpnts]:
                                            norm_temp_1= iii[5]+[iii[1]]    
                                else: #topo points
                                    for tnp in points_temp:
                                        if tnp[6]==i[0][newpnts]:
                                            norm_temp_1=tnp[3]+[tnp[2]]
                            if type(i[0][newpnts+1])==int: #point 2 id
                                if i[0][newpnts+1]>=0:
                                    for iii in mainpointlist+mainpointlistreverse:
                                        if iii[0]==i[0][newpnts+1]:
                                            norm_temp_2= iii[5]+[iii[1]] 
                                else: #topo points
                                    for tnp in points_temp:
                                        if tnp[6]==i[0][newpnts+1]:
                                            norm_temp_2=tnp[3]+[tnp[2]]
                            ###################
                            if norm_temp_1==False: #list
                                for ind in indextemplist_with_coords: #change from bhid to bhindex
                                    if i[0][newpnts][3]==ind[0]:
                                        i[0][newpnts][3]=ind[1]
                                pntcord.append(i[0][newpnts])
                            ####    
                            elif norm_temp_1 != False : #just the point id, sit have to be changed
                                #changesit
                                #update sits
                                for ii in mainpointlist+mainpointlistreverse:
                                    if ii[0]==i[0][newpnts]:
                                        if norm_temp_2 != False: #second point is a pntid
                                            if norm_temp_1[0] < norm_temp_2[0]:
                                                #topo points
                                                if ii[8]==0:
                                                    ii[8]=2
                                                elif ii[8]==1:
                                                     ii[8]=3   
                                            else:
                                                if ii[8]==0:
                                                    ii[8]=1
                                                elif ii[8]==2:    
                                                    ii[8]=3

                                        elif norm_temp_2 == False: #second point is a list
                                            if norm_temp_1[0] < i[0][newpnts+1][0]:
                                                #topo points
                                                if ii[8]==0:
                                                    ii[8]=2
                                                elif ii[8]==1:
                                                     ii[8]=3   
                                            else:
                                                if ii[8]==0:
                                                    ii[8]=1
                                                elif ii[8]==2:    
                                                    ii[8]=3
                                ##################
                                #append coord
                                pntcord.append(norm_temp_1)
                            ####    
                            if norm_temp_2==False: #list
                                for ind in indextemplist_with_coords: #change from bhid to bhindex
                                    if i[0][newpnts+1][3]==ind[0]:
                                        i[0][newpnts+1][3]=ind[1]
                                pntcord.append(i[0][newpnts+1])
                            elif norm_temp_2 != False: #just the point id, sit have to be changed
                                #changesit
                                #update sits
                                for ii in mainpointlist+mainpointlistreverse:
                                    if ii[0]==i[0][newpnts+1]:
                                        if norm_temp_1 != False: #first point is a pntid
                                            if norm_temp_1[0] < norm_temp_2[0]:
                                                #topo points
                                                if ii[8]==0:
                                                    ii[8]=1
                                                elif ii[8]==2:
                                                    ii[8]=3   
                                            else:
                                                if ii[8]==0:
                                                    ii[8]=2
                                                elif ii[8]==1:    
                                                    ii[8]=3
                                        elif norm_temp_1 == False: #first point is a list
                                            if i[0][newpnts][0] < norm_temp_2[0]:
                                                #topo points
                                                if ii[8]==0:
                                                    ii[8]=1
                                                elif ii[8]==2:
                                                    ii[8]=3   
                                            else:
                                                if ii[8]==0:
                                                    ii[8]=2
                                                elif ii[8]==1:    
                                                    ii[8]=3
                                ##################    
                                pntcord.append(norm_temp_2)      
                            #append line
                            if pntcord[0][0]<pntcord[1][0]:
                                pntcord2=pntcord
                            else:
                                pntcord2=[pntcord[1],pntcord[0]]
                            for polies in mainpolylist:
                                if polies[0]==int(pntcord2[0][3]):
                                    polies[2].append([manualzone_priority,zone_type,None,pntcord2[0][:-1],pntcord2[1][:-1],priority,priority_type])
                                    temporary_manual_list.append([pntcord2[0][:-1],pntcord2[1][:-1]])
                    elif i[2]=='user_skipped':
                        pass
    return mainpointlist,mainpointlistreverse,mainpolylist,temporary_manual_list
