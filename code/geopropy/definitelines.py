from itertools import izip
from math import sqrt
#import intersectioncheck
#import intersectfun
#import intersectionchecklinesegment
from segmentlineintersection3d import segmentlineintersection3d

def definitelines(prior,indextemplist_with_coords,mainpointlist,mainpolylist):
    ounter=0
    ounter2=0
    
    for k in range(0,len(prior)): #select one priority
        #4 values below are list because of repetition
        for l in range(0,len(indextemplist_with_coords)-1): #for every 2 neighbor bhs
            #indextemplist_with_coords=[ 0=id, 1=index]
            point1=list()
            point2=list()
            for j in range(0,len(mainpointlist)):

                    if mainpointlist[j][1]==indextemplist_with_coords[l][1] and mainpointlist[j][3] in prior[k] and mainpointlist[j][8] in [0,1] :
                        point1.append([mainpointlist[j][5],j])
                        ounter=ounter+1
                        #if mainpointlist[j][3]==3: print "point1", mainpointlist[j]
                    elif mainpointlist[j][1]==indextemplist_with_coords[l+1][1] and mainpointlist[j][3] in prior[k]  and mainpointlist[j][8] in [0,2]:
                        point2.append([mainpointlist[j][5],j])
                        ounter2=ounter2+1
                        #if mainpointlist[j][3]==3: print "point2", mainpointlist[j]
            '''mainpolylist=[[index1,index2,[[priority_number , Type, poly1],[priority_number , Type, poly2]]],
            [bh2,bh3,[[priority_number , Type, poly1],[priority_number , Type, poly2]]]]

            prior = [prior 0:prioroty 1:[toplayer] 2:[bottomlayer] 3:type]'''

            if len(point1) > 0 and len(point2) > 0:

                for q,o in izip(point1,point2):

                    pointlist=[q[0],o[0]]
                    #polytemp=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlist]),"Unknown",True,False)
                    polytemp=None
                    #print 'polytemp successful'
                    #check for intersection

                    #polyline append:
                    tempeval = None
                    for cou in mainpolylist:
                        if cou[0]==indextemplist_with_coords[l][1] and cou[1]==indextemplist_with_coords[l+1][1]:
                            tempeval=False
                            polylisttemp=list()
                            pntsleft=list()
                            pntrsigh=list()
                            index=list()
                            for idx,hh in enumerate(cou[2]):
                                intersectt=segmentlineintersection3d([hh[3],hh[4]],pointlist)
                                if intersectt != False:
                                    #print "intersect definite true\n", intersectt,prior[k][0] , hh[0]
                                    if prior[k][0]<hh[0]: #if prio def less than prio old line
                                        tempeval=True
                                    elif prior[k][0]>hh[0]: #if prio def more than prio old line
                                        #correct the line
                                        pntsleft.append(hh[3])
                                        pntrsigh.append(hh[4])
                                        index.append(idx)
                            #delete the indexes in index list
                            index=sorted(index,reverse=True)
                            for ind in index:
                                cou[2].pop(ind)
                            #change sit:
                            for pnt in mainpointlist:
                                if pnt[5] in pntsleft:
                                    if pnt[8]==2:
                                        pnt[8]=0
                                    elif pnt[8]==3:
                                        pnt[8]=1
                                elif pnt[5] in pntrsigh:
                                    if pnt[8]==1:
                                        pnt[8]=0
                                    elif pnt[8]==3:
                                        pnt[8]=2
                            ###################################
                            #append the new line
                            if tempeval == False:
                                cou[2].append([ prior[k][0],prior[k][3] ,polytemp,pointlist[0],pointlist[1]])
                            #####################
                    '''change the points situation'''
                    #left
                    if tempeval == False:
                        if mainpointlist[q[1]][8] == 1:
                            mainpointlist[q[1]][8] = 3
                            #print('change sit from 1 to 3', mainpointlist[q[1]])
                        elif mainpointlist[q[1]][8] == 0:
                            mainpointlist[q[1]][8] = 2
                            #print('change sit from 0 to 2', mainpointlist[q[1]])

                        #right
                        if mainpointlist[o[1]][8] == 2:
                            mainpointlist[o[1]][8] = 3
                            #print('change sit from 2 to 3', mainpointlist[o[1]])
                        elif mainpointlist[o[1]][8] == 0:
                            mainpointlist[o[1]][8] = 1
                            #print('change sit from 0 to 1',mainpointlist[o[1]])

                    '''...........................'''
    ff = [ounter,ounter2]
    #print 'counter for defenite lines 2 list of points (definitelines.py)', prior, ounter, ounter2
    return [mainpointlist, mainpolylist, ff ]
