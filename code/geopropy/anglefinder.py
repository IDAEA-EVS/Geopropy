import math
import operator


def anglecalculator(sp,ep): #sp: start point #ep: end point

    len_2dim_beside=math.sqrt( math.pow((sp[0]-ep[0]),2)   + math.pow((sp[1]-ep[1]),2) )
    len_2dim_front=float(sp[2]-ep[2])
    tanalpha=float(len_2dim_front)/len_2dim_beside
    if sp[2]> ep[2]:
        upordown="down"
    else:
        upordown="up"
    return tanalpha, upordown
##################################################################
def anglefinder(mainpolylist,prior,fault_table,predefined_angle_degree):

    #making the angles list
    angles=list()

    for n in prior:
        if ([n[0],n[3],None ,0, [] ]) not in angles:
            angles.append([n[0],n[3],None,0,None, [], []]    )
            #angles= [ [0:prio_num, 1:type, 2:tan_angle, 3:quantity, 4:from left (up or down) ,5:[ [index1,index2,startpoint,endpoint] ], 6:[upordown_dic]   ] ,...]
    #######################
    for i in range(0,len(angles)):
        if angles[i][1] not in  ['intrusion', 'dyke']:
            #extracting the polylines for every priority (excluding virtuals)
            for j in range(1,len(mainpolylist)-1):
                for poliess in mainpolylist[j][2]:
                    if poliess[0]==angles[i][0] and poliess[1]==angles[i][1]:
                        if [mainpolylist[j][0],mainpolylist[j][1],poliess[3],poliess[4]] not in angles[i][5]:
                            angles[i][5].append([mainpolylist[j][0],mainpolylist[j][1],poliess[3],poliess[4]])
        #calculating the angle
        ang_temp_average=None
        ang_temp_list=list()
        upordown_dic={"up": 0,"down":0}
        upordown=None
        for pol in angles[i][5]:
            #print "pol\n", pol
            tanalpha_temp, upordownpoly =anglecalculator(pol[2],pol[3])
            ang_temp_list.append(tanalpha_temp)
            upordown_dic[upordownpoly] = upordown_dic.get(upordownpoly)+1
        if len(ang_temp_list)>0:
            ang_temp_average=sum(ang_temp_list)/len(ang_temp_list)
            if ang_temp_average>0:
                upordown="down"
            elif ang_temp_average<0:
                upordown="up"
            else:
                upordown=max(upordown_dic.iteritems(), key=operator.itemgetter(1))[0]
        angles[i][2]=ang_temp_average
        angles[i][3]=len(ang_temp_list)
        angles[i][4]=upordown
        angles[i][6]=upordown_dic
    ######################
    #fault processing:
    #print 'angles before fault processing in anglefinder.py', angles
    for k in angles:
        if k[1]=="fault" and k[2]== None: #FAULTS IN CHRONOPRIORITY TABLE OVERWRITE THE ANGLES IN FAULT TABLE
            #print 'in faultps 1'
            for fault in fault_table:
                if fault[0]==k[0]:
                    #print 'in faulttps2'
                    if fault[2] != None and fault[2]>=0:
                        k[2]=math.tan(math.radians(fault[2]))
                        k[4]="up"
                        #print 'in faultps3'
                    elif fault[2] != None and fault[2]<0:
                        k[2]=abs(math.tan(math.radians(fault[2])))
                        k[4]="down"
                        #print 'in faultps4'
                    else:
                        if predefined_angle_degree >= 0:
                            if predefined_angle_degree==90:
                                predefined_angle_degree=89
                            elif predefined_angle_degree==0:
                                predefined_angle_degree=1
                                #print 'in faultps else'
                            k[2]=math.tan(math.radians(predefined_angle_degree))
                            k[4]="up"
                        else:
                            if predefined_angle_degree==-90:
                                predefined_angle_degree=89
                                #print 'in faultps else'
                            k[2]=math.tan(math.radians(math.abs(predefined_angle_degree)))
                            k[4]="down"
                            #read from the fault_table. if not existed
    #######################
    #Now the only one with the None are the priority numbers that do not have a line
    return  angles
##################################################################    
def angleupdater(gg,uy,angles):
    #angles= [ [0:prio_num, 1:type, 2:tan_angle, 3:quantity, 4:from left (up or down) ,5:[ [index1,index2,startpoint,endpoint] ], 6:[upordown_dic]   ] ,...]
    for ang in angles:
        if uy[3]==ang[0]:
            for linee in ang[5]:
                if gg[1]==linee[2] and gg[2]==linee[3]:
                    if ang[3]>1:
                        sum_tan_angle_old=ang[2]*ang[3]
                        tanalpha, upordown=anglecalculator(linee[2],linee[3])
                        ang[3]=ang[3]-1
                        ang[2]= float((sum_tan_angle_old - tanalpha))/(ang[3])
                        ang[6][upordown]=ang[6].get(upordown)-1
                        ang[4]=max(ang[6].iteritems(), key=operator.itemgetter(1))[0]
                    else:
                        ang[2]=None
                        ang[3]=None
                        ang[4]=None
                        ang[5]=list()
    return angles
##################################################################    
def angleestimator(poi, mainpointlist, mainpolylist,leftorrightcompleteor):
    #angles= [ [0:prio_num, 1:type, 2:tan_angle, 3:quantity, 4:from left (up or down) ,5:[ [index1,index2,startpoint,endpoint] ], 6:[upordown_dic]   ] ,...]
    bhpoints=list()
    nearest_uppoint=None
    nearest_downpoint=None
    tan_angle_temp=None
    upordown_temp=None
    if poi[4]=='normal': #just do the procedure it the point is normal contact
        for points in mainpointlist:
            if poi[1]==points[1] and poi[5] != points[5]:
                if points[5][2]> poi[5][2]:
                    #higher point
                    if nearest_uppoint==None:
                        nearest_uppoint=points
                    if points[5][2]<nearest_uppoint[5][2]:
                        nearest_uppoint=points
                else:
                    #lower point
                    if nearest_downpoint==None:
                        nearest_downpoint=points
                    if points[5][2]>=nearest_downpoint[5][2]:
                        nearest_downpoint=points
        #left or right
        if leftorrightcompleteor=="left":
            bh1=poi[1]-1
            bh2=poi[1]
        else:
            bh1=poi[1]
            bh2=poi[1]+1
        ############
        #up
        if nearest_uppoint != None and nearest_uppoint[4]=="normal" and nearest_uppoint[3]==poi[3]+1:
            for polyliness in mainpolylist:
                if polyliness[0]==bh1 and polyliness[1]==bh2:
                    for pol in polyliness[2]:
                        if pol[0]==nearest_uppoint[3]:
                            tan_angle_temp, upordown_temp=anglecalculator(pol[3],pol[4])
        #down
        elif nearest_downpoint !=None and nearest_downpoint[4]=="normal" and nearest_downpoint[3]==poi[3]-1:
            for polyliness in mainpolylist:
                if polyliness[0]==bh1 and polyliness[1]==bh2:
                    for pol in polyliness[2]:
                        if pol[0]==nearest_downpoint[3]:
                            tan_angle_temp, upordown_temp=anglecalculator(pol[3],pol[4])
        else:
            pass
    return tan_angle_temp, upordown_temp
