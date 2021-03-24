from operator import itemgetter


def topolinecreator(mainpolylist,indextemplist_with_coords,prior,temp_points):

    '''find the topo priority (more than all of them) '''
    prior=sorted(prior,key=itemgetter(0))
    #prior 0:prioroty 1:[toplayer] 2:[bottomlayer] 3:type]
    topoprior = prior[-1][0]+1
    temp_point_af_ed=list()
    '''........................................ '''
    for pl in range(0,len(mainpolylist)):
        for ind in indextemplist_with_coords:
            if mainpolylist[pl][0]==ind[1]:
                coord1=ind[2:]
            elif mainpolylist[pl][1]==ind[1]:
                coord2=ind[2:]
        pointlist=[coord1,coord2]
        ############################################
        #for first and last parallel lines
        if pl==1:
            maxfirst=pointlist[0]
        if pl==len(mainpolylist)-2:
            maxlast=pointlist[1]
        ############################################
        for nnnn in temp_points: #adding surface points
            if nnnn[0]=="surface":
                for each_prio in nnnn[1]:
                    if each_prio[6] in ["topography", "Topography"] and mainpolylist[pl][0]==each_prio[0]:
                        pointlist.append(each_prio[3:6])
        pointlist=sorted(pointlist,key=itemgetter(0)) #sort by X                
        #polytemp=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlist]),"Unknown",True,False)
        polytemp=None
        for allpnts in range(0,len(pointlist)-1):
            mainpolylist[pl][2].append([topoprior,'Topography',polytemp,pointlist[allpnts],pointlist[allpnts+1]])
    #############################################
    for nnnn in temp_points: #remove surface from temp points for later analysis
        if nnnn[0]!="surface":
            temp_point_af_ed.append(nnnn)
    #############################################    
    return mainpolylist, maxfirst,maxlast,temp_point_af_ed
