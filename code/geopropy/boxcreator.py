from operator import itemgetter
'''This is the box with two options: ratiobottombox or normalbottombox'''
def boxcreator2(typebottombox,box_bottom_rate,fault_table, rawdata,prior,mainpolylist,indextemplist_with_coords):
    pointsforbox=list()
    minlist=list()
    for b in range(0,len(indextemplist_with_coords)):
        minbot=None
        for n in rawdata:
            if n[1]==indextemplist_with_coords[b][0]:
                if minbot==None or minbot >= n[3]:
                    minbot=n[3]
        #Taking into account minimums in fault table
        for z in fault_table:
            for g in z[1]:
                if g[0]==indextemplist_with_coords[b][0]:
                    elevfault = indextemplist_with_coords[b][4] - g[1]
                    if minbot >= elevfault:
                        minbot=elevfault
        minlist.append(minbot)
        if typebottombox=='ratiobottombox':
            #add bottom box to raw data
            if  minbot != (box_bottom_rate * minbot):
                rawdata.append([indextemplist_with_coords[b][1],indextemplist_with_coords[b][0],minbot,(box_bottom_rate * minbot),'bottombox'])
            pointsforbox.append([indextemplist_with_coords[b][2],indextemplist_with_coords[b][3],(box_bottom_rate * minbot)])
    #raw data for normal bottombox
    if typebottombox=='normalbottombox':
        minlist.sort()
        minim=minlist[0]
        for b in range(0,len(indextemplist_with_coords)):
            '''extracting the points '''
            if  minim != (box_bottom_rate * minim):
                rawdata.append([indextemplist_with_coords[b][1],indextemplist_with_coords[b][0],minim,(box_bottom_rate * minim),'bottombox'])
            pointsforbox.append([indextemplist_with_coords[b][2],indextemplist_with_coords[b][3],(box_bottom_rate * minim)])
    rawdata=sorted(rawdata,key=itemgetter(2),reverse=True)
    rawdata=sorted(rawdata,key=itemgetter(0))
    '''find the bottom box priority (less than all of them) '''
    prior=sorted(prior,key=itemgetter(0),reverse=True)
    #prior 0:prioroty 1:[toplayer] 2:[bottomlayer] 3:type]
    boxprior = prior[-1][0]-1
    '''........................................ '''
    #drawing and adding polylines
    for i in range(0,len(pointsforbox)-1):
        pointlist=[pointsforbox[i],pointsforbox[i+1]]
        polytemp=None
        mainpolylist[i][2].append([boxprior,'bottombox',polytemp,pointlist[0],pointlist[1]])
        #boxpoints=[]
        #for n in range(1,len(pointsforbox)-1):
    boxpoints=[]
    return mainpolylist,boxpoints,rawdata
