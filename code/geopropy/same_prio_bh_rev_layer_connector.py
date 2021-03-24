from segmentlineintersection3d import segmentlineintersection3d
#this function also update mainpointlists after drawing the lines
#left is already connected in this function, we try to connect right
#IMPORTANT:zone_typee=zone[3]
def same_prio_bh_rev_layer_connector_connect_right(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_typee):
    #rev_same_bh=[[ bh , [ [p1,p2],...],sitpointdic ],...]
    #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
    #revpoints=[p1,p2]
    #print "same_prio_bh_rev_layer_connector_connect_right used"
    #finding the distance of min and max in bh
    maxbh_up=None
    minbh_down=None
    for i in mainpointlist+mainpointlistreverse:
        if revpoints[0][2]==i[1]:
            if maxbh_up==None or maxbh_up< i[5][2]:
                maxbh_up= i[5][2]
            if minbh_down==None or minbh_down> i[5][2]:
                minbh_down= i[5][2]
    in_bh_distance=abs(minbh_down - maxbh_up)
    #finding the z ditance between p1 and p2:
    between_points_distance=abs(revpoints[0][3][2] - revpoints[1][3][2])
    #ratio
    ratio=float(between_points_distance)/in_bh_distance
    #finding the next bh x & y coord, then finding the middle 2 bh point point
    for ind in indextemplist_with_coords:
        if ind[1]==revpoints[0][2]+1:
            xnext=ind[2]
            ynext=ind[3]
    #middle of 2 bhs
    xmid=(xnext + revpoints[0][3][0])/2
    ymid=(ynext + revpoints[0][3][1])/2
    zmid=(revpoints[0][3][2] + revpoints[1][3][2])/2
    #finding new X & Y
    x_new=revpoints[0][3][0]+ratio*abs(xmid-revpoints[0][3][0])
    #if y nex> y first
    if revpoints[0][3][1] < ynext:
        y_new=revpoints[0][3][1]+ratio*abs(ymid-revpoints[0][3][1])
    #if y nex < y first
    else:
        y_new=revpoints[0][3][1]-ratio*abs(ymid-revpoints[0][3][1])
    #making the polyline:
    for polies in mainpolylist: #creating polyline and changing pointsit
        if revpoints[0][2]==polies[0] and revpoints[0][2]+1==polies[1]:
            for check_for_inter in polies[2]: #check for intersections
                inters1=segmentlineintersection3d([revpoints[0][3],[x_new,y_new,zmid]],[check_for_inter[3],check_for_inter[4]])
                inters2=segmentlineintersection3d([revpoints[1][3],[x_new,y_new,zmid]],[check_for_inter[3],check_for_inter[4]])
                if inters1!=False or inters2!=False:
                    same_bh_intersec=True
            if same_bh_intersec==False:        
                polies[2].append([manualzone_priority,zone_typee,None,revpoints[0][3],[x_new,y_new,zmid],priority,priority_type])
                temporary_manual_list.append([revpoints[0][3],[x_new,y_new,zmid]])
                polies[2].append([manualzone_priority,zone_typee,None,revpoints[1][3],[x_new,y_new,zmid],priority,priority_type])
                temporary_manual_list.append([revpoints[1][3],[x_new,y_new,zmid]])
    #update mainpointlist and mainpointlistreverse
    #change pointsit
    if same_bh_intersec==False:
        for ii in mainpointlist+mainpointlistreverse:
            if ii[0] in [revpoints[0][6], revpoints[1][6] ]:
                if ii[8]==0:
                    ii[8]=2
                elif ii[8]==1:
                    ii[8]=3
    return mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec

###########################################
###########################################
#right is already connected in this function, we try to connect left
#IMPORTANT:zone_typee=zone[3]
def same_prio_bh_rev_layer_connector_connect_left(same_bh_intersec,temporary_manual_list,mainpointlist,mainpointlistreverse,revpoints,indextemplist_with_coords,mainpolylist,manualzone_priority,priority,priority_type,zone_typee):
    #rev_same_bh=[[ bh , [ [p1,p2],...],sitpointdic ],...]
    #p=["BOREHOLE_ID, BOREHOLE_INDEX, [X,Y,Z], POLARITY, POINT_ID",sit]
    #revpoints=[p1,p2]
    #print "same_prio_bh_rev_layer_connector_connect_left function used"
    #finding the distance of min and max in bh
    maxbh_up=None
    minbh_down=None
    for i in mainpointlist+mainpointlistreverse:
        if revpoints[0][2]==i[1]:
            if maxbh_up==None or maxbh_up< i[5][2]:
                maxbh_up= i[5][2]
            if minbh_down==None or minbh_down> i[5][2]:
                minbh_down= i[5][2]
    in_bh_distance=abs(minbh_down - maxbh_up)
    #finding the z ditance between p1 and p2:
    between_points_distance=abs(revpoints[0][3][2] - revpoints[1][3][2])
    #ratio
    ratio=float(between_points_distance)/in_bh_distance
    #finding the next bh x & y coord, then finding the middle 2 bh point point
    for ind in indextemplist_with_coords:
        if ind[1]==revpoints[0][2]-1:
            xprev=ind[2]
            yprev=ind[3]
    #middle of 2 bhs
    xmid=(xprev + revpoints[0][3][0])/2
    ymid=(yprev + revpoints[0][3][1])/2
    zmid=(revpoints[0][3][2] + revpoints[1][3][2])/2
    #finding new X & Y
    x_new=revpoints[0][3][0]-ratio*abs(xmid-revpoints[0][3][0])
    #if y nex> y first
    if revpoints[0][3][1] < yprev:
        y_new=revpoints[0][3][1]+ratio*abs(ymid-revpoints[0][3][1])
    #if y nex < y first
    else:
        y_new=revpoints[0][3][1]-ratio*abs(ymid-revpoints[0][3][1])
    #making the polyline:
    for polies in mainpolylist: #creating polyline and changing pointsit
        if revpoints[0][2]-1==polies[0] and revpoints[0][2]==polies[1]:
            for check_for_inter in polies[2]: #check for intersections
                inters1=segmentlineintersection3d([[x_new,y_new,zmid],revpoints[0][3]],[check_for_inter[3],check_for_inter[4]])
                inters2=segmentlineintersection3d([[x_new,y_new,zmid],revpoints[1][3]],[check_for_inter[3],check_for_inter[4]])
                if inters1!=False or inters2!=False:
                    same_bh_intersec=True
            if same_bh_intersec==False:        
                polies[2].append([manualzone_priority,zone_typee,None,[x_new,y_new,zmid],revpoints[0][3],priority,priority_type])
                temporary_manual_list.append([[x_new,y_new,zmid],revpoints[0][3]])
                polies[2].append([manualzone_priority,zone_typee,None,[x_new,y_new,zmid],revpoints[1][3],priority,priority_type])
                temporary_manual_list.append([[x_new,y_new,zmid],revpoints[1][3]])
    #update mainpointlist and mainpointlistreverse
    #change pointsit
    if same_bh_intersec==False:
        for ii in mainpointlist+mainpointlistreverse:
            if ii[0] in [revpoints[0][6], revpoints[1][6] ]:
                if ii[8]==0:
                    ii[8]=1
                elif ii[8]==2:
                    ii[8]=3
    return mainpolylist,mainpointlist,mainpointlistreverse,temporary_manual_list,same_bh_intersec
