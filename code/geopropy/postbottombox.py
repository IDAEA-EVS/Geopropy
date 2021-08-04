import segmentlineintersection3d
from operator import itemgetter
import arcpy

def postbottombox(mainpolylist,mainpointlist,indextemplist_with_coords,bottomlength):
    postbottomboxlist=list()
    ######################
    lastone=mainpolylist[-1][0]
    #finding intersection points
    bottomz=None
    intersectionpoints=list()
    for i in mainpolylist:
        pairchecker=list()
        if i[0] != 1 and i[0] !=lastone:
            for j in range(0,len(i[2])):
                if i[2][j][1]=='bottombox' and bottomz==None:
                    bottomz=i[2][j][3][2]
                for k in range(0,len(i[2])):
                    if k!=j:
                        if [[i[2][j][3],i[2][j][4]],[i[2][k][3],i[2][k][4]]] not in pairchecker and [[i[2][k][3],i[2][k][4]],[i[2][j][3],i[2][j][4]]] not in pairchecker:
                            #print 'postbottombox intersecttouch used'
                            intersection, typeintersection= segmentlineintersection3d.intersection3dtouch([i[2][j][3],i[2][j][4]],[i[2][k][3],i[2][k][4]])
                            pairchecker.append([[i[2][j][3],i[2][j][4]],[i[2][k][3],i[2][k][4]]])
                            if intersection != False:
                                #print 'postbottombox intersecttouch is not false', intersection, typeintersection
                                if 'bottombox' not in [i[2][j][1],i[2][k][1]]:
                                    intersectionpoints.append([ i[0],i[1] , i[2][j][0],i[2][k][0], intersection, typeintersection,None ])
                                    #intersectionpoints=[ [index1, index2,prio_num1, prio_num2,intersectioncoord, intersectiontype] ]
                                else:
                                    intersectionpoints.append([ i[0],i[1] , i[2][j][0],i[2][k][0], intersection, typeintersection,"bottombox" ])

    #print 'intersectionpoints list', intersectionpoints
    #########################
    #borehole minimums
    minslist=list()
    allpointsforbox=list()


    for i in range(1,len(indextemplist_with_coords)-1):
        bottombox = False
        mintemp=None
        mintempinter=None
        for j in mainpointlist:
            if j[1]==indextemplist_with_coords[i][1]:
                if mintemp==None or mintemp[2] > j[5][2]:
                    mintemp=j[5]
                else:
                    pass
        if mintemp==None:    
            mintemp=[indextemplist_with_coords[i][2],indextemplist_with_coords[i][3],bottomz]    
        if i==1:
            minsfirst=[indextemplist_with_coords[i][1],mintemp,2,None,indextemplist_with_coords[i][1]]
        if i==len(indextemplist_with_coords)-2:
            minslast=[indextemplist_with_coords[i][1],mintemp,2,None,indextemplist_with_coords[i][1]]
        for k in intersectionpoints:
            #intersectionpoints minimum
            if indextemplist_with_coords[i][1] == k[0]:
                if mintempinter==None or mintempinter[2] > k[4][2] :
                    mintempinter=k[4]
                    if k[6]=="bottombox":
                        bottombox=True
                else:
                    pass
        if mintempinter != None:

            #if mintemp==None:
            #    mintemp=mintempinter+[None] #in case there is no point in a bh (all the same material!)
                
            #print "mintempinter[2] <= mintemp[2]",mintempinter[2] , mintemp
            if mintempinter[2] <= mintemp[2]:
                #mintemp=[mintemp[0],mintemp[1],mintemp[2]]
                minslist.append([indextemplist_with_coords[i][1],mintemp,0,None,indextemplist_with_coords[i][1]])
                if bottombox !=True:
                    minslist.append([indextemplist_with_coords[i][1],mintempinter,1,None,indextemplist_with_coords[i][1]])
                else:
                    minslist.append([indextemplist_with_coords[i][1],mintempinter,1,"bottombox",indextemplist_with_coords[i][1]])
            else: #ok!
                minslist.append([indextemplist_with_coords[i][1],mintemp,0,None,indextemplist_with_coords[i][1]])
        else: #ok!
            minslist.append([indextemplist_with_coords[i][1],mintemp,0,None,indextemplist_with_coords[i][1]])

    minslist=sorted(minslist,key=itemgetter(0,2))
    if minslast not in minslist:
        minslist=minslist+[minslast]
    if minsfirst not in minslist:
        minslist= [minsfirst]+minslist

    #print 'minslist', minslist
    #########################
    #create the line
    for jj in range(0,len(minslist)-1):
        if minslist[jj][1] != minslist[jj+1][1]:
            if minslist[jj][3] != "bottombox": 
                if minslist[jj+1][3] != "bottombox":
                    points=[  [minslist[jj][1][0],minslist[jj][1][1], minslist[jj][1][2] - bottomlength] , [minslist[jj+1][1][0],minslist[jj+1][1][1],minslist[jj+1][1][2] - bottomlength]  ]
                else:
                    points=[  [minslist[jj][1][0],minslist[jj][1][1], minslist[jj][1][2] - bottomlength] , minslist[jj+1][1] ]

            else:
                if minslist[jj+1][3] != "bottombox":
                    points=[ minslist[jj][1]  ,[minslist[jj+1][1][0],minslist[jj+1][1][1],minslist[jj+1][1][2] - bottomlength] ]
                else:
                    points=[ minslist[jj][1]  ,minslist[jj+1][1] ]

            if points[0] != points[1]:
                polytemp=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in points]),"Unknown",True,False)
                postbottomboxlist.append([minslist[jj][0],minslist[jj+1][0],points[0],points[1],polytemp,minslist[jj][4]])
                #postbottomboxlist=[ [point1coord,point2coord,point 1 borehole or mid (0 or 1) ,point 2 borehole or mid (0 or 1), polyline,bhindex] ,... ]
                #intersectionpoints=[ [index1, index2,prio_num1, prio_num2,intersectioncoord, intersectiontype] ]

    minsfirst[1]=[minsfirst[1][0],minsfirst[1][1],minsfirst[1][2]- bottomlength]
    minslast[1]=[minslast[1][0],minslast[1][1],minslast[1][2]- bottomlength]
    return intersectionpoints, postbottomboxlist,minsfirst,minslast
