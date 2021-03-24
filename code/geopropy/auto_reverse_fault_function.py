
#IMPORTANT faultpart=zone[2]
#critical_bhs=zone[0]
#faultpart=[ [ priority, [points (from mainpointlist)] ] ,...]
#priority,priority_type=criticals[0],criticals[2]
from operator import itemgetter
import math
#############################################################################
def extraccord_and_faultpoint(indextemplist_with_coords,i,j,side):    
    #extract x and y of i[0] and i[1] and calculate the fault point and append to fault_line_list
    for bhp in indextemplist_with_coords:
        if bhp[1]==i[1] and side=="right" or bhp[1]==i[0] and side=="left":
            xt = bhp[2] #unknown right bh
            yt= bhp[3] # unknown right bh
    x0 = j[2][0]
    y0= j[2][1]
    z0=j[2][2]
    x1 = j[3][0]
    y1= j[3][1]
    z1=j[3][2]
    #############################
    #t[3]=startpoint
    #t[4]=endpoint
    len3=math.sqrt(math.pow(x1-x0,2)+math.pow(y1-y0,2)+math.pow(z1-z0,2))
    sinalpha=float(abs(z1-z0))/(len3)
    cosalpha=math.sqrt(1-math.pow(sinalpha,2))
    tanalpha=sinalpha/cosalpha
    if side=="right":
        distparallel = math.sqrt( math.pow((x1-xt),2)   + math.pow((y1-yt),2) )
    elif side=="left":
        distparallel = math.sqrt( math.pow((x0-xt),2)   + math.pow((y0-yt),2))
    difelev = tanalpha * distparallel
    if z0 < z1 and side=="right" or z1<z0 and side=="left":
        zt = z1 + difelev
    else:
        zt = z1 - difelev
    #############################
    i[3]=[xt,yt,zt]
    if side=="right":
        i[2]=j[3]
        i[3]=[xt,yt,zt]
    else:
        i[3]=j[2]
        i[2]=[xt,yt,zt]
    return i
#############################################################################
def other_fault_generate_line(other_fault_line,mainpolylist,temporary_manual_list,maxpriority,mainpointlist,mainpointlistreverse,priority,priority_type):    
    for i in range(0,len(other_fault_line)-1):
                for polies in mainpolylist:
                    if other_fault_line[i][0]==polies[0] and other_fault_line[i+1][0]==polies[1]:
                        polies[2].append([maxpriority+1,'auto_reverse_fault',None,[other_fault_line[i][2],other_fault_line[i][3],other_fault_line[i][4]],[other_fault_line[i+1][2],other_fault_line[i+1][3],other_fault_line[i+1][4]],priority,priority_type])
                        temporary_manual_list.append([[other_fault_line[i][2],other_fault_line[i][3],other_fault_line[i][4]],[other_fault_line[i+1][2],other_fault_line[i+1][3],other_fault_line[i+1][4]]])
                        #change pointsit
                        for ii in mainpointlist+mainpointlistreverse:
                            if ii[0]==other_fault_line[i][5]:
                                if ii[8]==0:
                                    ii[8]=2
                                elif ii[8]==1:
                                    ii[8]=3
                            elif ii[0]==other_fault_line[i+1][5]:
                                if ii[8]==0:
                                    ii[8]=1
                                elif ii[8]==2:
                                    ii[8]=3
    return mainpolylist,temporary_manual_list,mainpointlist,mainpointlistreverse
#mainpolylist,temporary_manual_list,mainpointlist,mainpointlistreverse=other_fault_generate_line(other_fault_line,mainpolylist,temporary_manual_list,maxpriority,mainpointlist,mainpointlistreverse)
#############################################################################
def rev_fault_fun(priority,priority_type,mainpointlistreverse,mainpolylist,mainpointlist,zonepnts,faultpart,critical_bhs,indextemplist_with_coords,maxpriority):
    temporary_manual_list=list()
    #######
    #1.find the intersection of the fault with the critical boreholes
    #2.for every zonepnts, if they are higher, they have the same code, if they are lower, other code
    #3.draw lines between the points, update the sitpoint status. leave the loose (unfinished) ends. they will be completed in secondstagelinecompleter
    fault_line_list=list()
    bhpairs_not_in_faults=list()
    #faultpart=zone[2]
    faultpoints=faultpart[0][1]
    faultpoints=sorted(faultpoints,key=itemgetter(1))
    critical_bhs=sorted(critical_bhs)
    for i in range(0,len(faultpoints)-1):
        fault_line_list.append([faultpoints[i][1],faultpoints[i+1][1],faultpoints[i][5],faultpoints[i+1][5],"real_fault_point"]) #fault_line_list=[[bhind,bhind+1,coord1,coord+1,"condition"],...]

    critical_bhs_temp=list()
    fault_line_list_temp=list()
    for i in range(0,len(critical_bhs)-1):
        critical_bhs_temp.append([critical_bhs[i],critical_bhs[i+1]])
    for j in fault_line_list:
        fault_line_list_temp.append([j[0],j[1]])
    for i in critical_bhs_temp:
            if i not in fault_line_list_temp:
                bhpairs_not_in_faults.append([i[0],i[1],None,None,"virtual_fault_point"]) #bhpairs_not_in_faults=[bh,bh+1,None]

    for i in bhpairs_not_in_faults:
        for j in fault_line_list:
            #extract x and y of i[0] and i[1] and calculate the fault point and append to fault_line_list
            if i[1] == j[0]: #left side (beggining)
                i=extraccord_and_faultpoint(indextemplist_with_coords,i,j,"left")
            ###########################################
            elif i[0] == j[1]: #right side (end)
                i=extraccord_and_faultpoint(indextemplist_with_coords,i,j,"right")
            ################################
    fault_line_list=fault_line_list+bhpairs_not_in_faults
    fault_in_bh_point=list()
    for i in fault_line_list:
        if [i[0],i[2]] not in fault_in_bh_point:
            fault_in_bh_point.append([i[0],i[2]])
        if [i[1],i[3]] not in fault_in_bh_point:
            fault_in_bh_point.append([i[1],i[3]])
    fault_in_bh_point=sorted(fault_in_bh_point,key=itemgetter(0))
    '''
    now we have fault points in all boreholes. by comparing every zonepnts
        with fault point cordination(up or down), we can decide their which
        lines have to connect. have in mind that intersection of the lines with
        fault lines can not be completed in continued line creator since the
        function can grab the wrong line in the borehole. the solution in to
        add a condition to continuedlinecreator function that the old line have
        to have the same z with the point. (continuedLineCreator already checks
        for the same z coordination!)
        continued...
    '''
    #zonepnts (higher_fault_line)=[pnt:[bhind,norm/rev,x,y,z,poindid]]
    #fault_in_bh_point=[ [ bhind,[coordinates] ]  ,...]
    higher_fault_line=list()
    lower_fault_line=list()
    for pnt in zonepnts:
        for fltpnt in fault_in_bh_point:
            if pnt[0]==fltpnt[0]:
                if pnt[4]>=fltpnt[1][2]:
                    higher_fault_line.append(pnt)
                else:
                    lower_fault_line.append(pnt)
    higher_fault_line=sorted(higher_fault_line,key=itemgetter(0))
    lower_fault_line=sorted(lower_fault_line,key=itemgetter(0))
    #make the lines and change the sit
    #for higher
    mainpolylist,temporary_manual_list,mainpointlist,mainpointlistreverse=other_fault_generate_line(higher_fault_line,mainpolylist,temporary_manual_list,maxpriority,mainpointlist,mainpointlistreverse,priority,priority_type)
    #for lower
    mainpolylist,temporary_manual_list,mainpointlist,mainpointlistreverse=other_fault_generate_line(lower_fault_line,mainpolylist,temporary_manual_list,maxpriority,mainpointlist,mainpointlistreverse,priority,priority_type)
    faultsit='auto_reverse_fault'
    return mainpolylist,mainpointlist,faultsit,temporary_manual_list
