import math
import arcpy
import boundaryconditions
from operator import itemgetter
from os.path import expanduser,join as joinadd
##########################################################################################################################################################################
def two_d_min_max_finder(planenormalslist,minsfirst,maxfirst,minslast,maxlast):
    #this function replaced with cross_product_and_planenormalslist_maker (below) planenormallist 
    # now calculating sooner in the main function since it is needed for surface point projection
    '''determine the new coordinates
    find the max and min of x and y coords and substract it
    find the plane equation between every two bh
    finding the plane equation
    https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FEquationofaPlane3Points
    ab=[0,0,1] (vector parallel to borehole)
    ac=[x2-x1,y2-y1,0] (horizontal vector between bhs)'''
    minsfirst_2d=[minsfirst[0],[ 0,minsfirst[1][2] ],minsfirst[2]]
    maxfirst_2d=[ 0,maxfirst[2] ]
    #last bh min and max (needed for createpolyfeatureclass_2d)
    minslast_2d=[minslast[0],[ planenormalslist[-1][3]+planenormalslist[-1][4],minslast[1][2] ],minslast[2]]
    maxlast_2d=[ planenormalslist[-1][3]+planenormalslist[-1][4],maxlast[2] ]
    #############
    return minslast_2d,maxlast_2d,maxfirst_2d,minsfirst_2d
'''
def cross_product_and_planenormalslist_maker(minsfirst,maxfirst,minslast,maxlast,indextemplist,boidtable,x,y):
    """determine the new coordinates
    find the max and min of x and y coords and substract it
    find the plane equation between every two bh
    finding the plane equation
    https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FEquationofaPlane3Points
    ab=[0,0,1] ac=[x2-x1,y2-y1,0]"""
    planenormalslist=list()
    bhzero=0
    for bh in range(1,len(indextemplist)-2): #excluding first and last bh (virtual ones)
        #3 points coordinations
        n1=indextemplist[bh][0]
        n2=indextemplist[bh+1][0]
        xbh1=x[boidtable.index(n1)]
        ybh1=y[boidtable.index(n1)]
        xbh2=x[boidtable.index(n2)]
        ybh2=y[boidtable.index(n2)]
        cross=[ ybh2-ybh1 , xbh1-xbh2 ,0, ((xbh2*ybh1)-(xbh1*ybh2))]
        #cross=[a,b,c,d] ax+by+cz+d=0
        distt=math.sqrt( math.pow((xbh2-xbh1),2)   + math.pow((ybh2-ybh1),2) )
        planenormalslist.append([indextemplist[bh][1],indextemplist[bh+1][1],[xbh1,ybh1,xbh2,ybh2],bhzero, distt, cross])
        #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)], 3:newcoord index1(x), 4:distance , 5:cross],...]
        #for the last borehole
        if bh==len(indextemplist)-3:
            planenormalslist.append([indextemplist[bh+1][1],indextemplist[bh+1][1],[xbh1,ybh1,xbh2,ybh2],bhzero, distt, cross])
        if bh==1:
            #first borehole min and max (needed for createpolyfeatureclass_2d)
            minsfirst_2d=[minsfirst[0],[ bhzero,minsfirst[1][2] ],minsfirst[2]]
            maxfirst_2d=[ bhzero,maxfirst[2] ]
        bhzero=bhzero+distt
        if bh==len(indextemplist)-3:
            #last bh min and max (needed for createpolyfeatureclass_2d)
            minslast_2d=[minslast[0],[ bhzero,minslast[1][2] ],minslast[2]]
            maxlast_2d=[ bhzero,maxlast[2] ]
    #############
    return planenormalslist,minslast_2d,maxlast_2d,maxfirst_2d,minsfirst_2d
'''
#planenormalslist,minslast_2d,maxlast_2d,maxfirst_2d,minsfirst_2d=cross_product_and_planenormalslist_maker(minsfirst,maxfirst,minslast,maxlast,indextemplist,boidtable,x,y)    
##########################################################################################################################################################################
def make_mainpolylist_2d_and_postbottombox_2d(planenormalslist,mainpolylist,postbottomboxlist,indextemplist):
    #############
    postbottomboxlist_2d=list()
    #making mainpolylist_2d
    mainpolylist_2d=list()
    for z in range(1,len(indextemplist)-2):
        mainpolylist_2d.append([indextemplist[z][1],indextemplist[z+1][1],[]])
    ##############
    # mainpolylist from 3d to 2d
    for bhpairs in planenormalslist:
        for poliees in mainpolylist:
            if poliees[0]==bhpairs[0] and poliees[1]==bhpairs[1]:
                for polyy in poliees[2]:
                    if polyy[1] !="bottombox":
                        new_ysp=polyy[3][2]
                        new_yep=polyy[4][2]
                        #new_x
                        dis1=math.sqrt( math.pow((polyy[3][0]-bhpairs[2][0]),2)   + math.pow((polyy[3][1]-bhpairs[2][1]),2) )
                        dis2=math.sqrt( math.pow((polyy[4][0]-bhpairs[2][0]),2)   + math.pow((polyy[4][1]-bhpairs[2][1]),2) )
                        new_xsp=bhpairs[3]+dis1
                        new_xep=bhpairs[3]+dis2
                        pointlist=[ [new_xsp,new_ysp], [new_xep,new_yep] ]
                        #make the polylines
                        poly2d=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlist]),"Unknown",False,False)
                        #append
                        for cou in mainpolylist_2d:
                            if cou[0]==bhpairs[0] and cou[1]==bhpairs[1]:
                                cou[2].append([ polyy[0],polyy[1] ,poly2d, pointlist[0],pointlist[1]])
        # postbottombox from 3d to 2d
        #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)], 3:newcoord index1(x), 4:distance , 5:cross]]
        #postbottomboxlist=[ [point1coord,point2coord,point 1 borehole or mid (0 or 1) ,point 2 borehole or mid (0 or 1), polyline,bhindex] ,... ]
        for boxline in postbottomboxlist:
            if bhpairs[0]==boxline[5]:
                disp1box=math.sqrt( math.pow((boxline[2][0]-bhpairs[2][0]),2)   + math.pow((boxline[2][1]-bhpairs[2][1]),2) )
                disp2box=math.sqrt( math.pow((boxline[3][0]-bhpairs[2][0]),2)   + math.pow((boxline[3][1]-bhpairs[2][1]),2) )
                pointlistbox=[ [bhpairs[3]+disp1box, boxline[2][2]],[bhpairs[3]+disp2box, boxline[3][2]]]
                poly2d=arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pointlistbox]),"Unknown",False,False)
                postbottomboxlist_2d.append([pointlistbox[0],pointlistbox[1],boxline[2],boxline[3],poly2d,boxline[5]])
    
    return mainpolylist_2d,postbottomboxlist_2d
#mainpolylist_2d,postbottomboxlist_2d=make_mainpolylist_2d_and_postbottombox_2d(planenormalslist,mainpolylist,postbottomboxlist,indextemplist)    
##########################################################################################################################################################################
def read_polygons_2d(planenormalslist,epsbn_ratio,eps_ratio):
    #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)]
    # , 3:newcoord index1(x), 4:distance , 5:cross]]
    #sys.stdout = open('C:\Users\usuari\stdout.txt', 'w')
    #sys.stderr = open('C:\Users\usuari\stderr.txt', 'w')
    lastbhindex=planenormalslist[-1][1]

    direc =joinadd(expanduser("~"),"arcgistemp_2d\\arcgistempdb_2d.gdb\\mergedpolygonsfromlines_2d")
    #print "lastbhindex", lastbhindex
    polygons_2d_list=list()
    for row in arcpy.da.SearchCursor(direc, ["SHAPE@"]):
        pnts=list()
        cntr=0
        for rw in row[0]:
            for pnt in rw:
                #print 'pnt in threeD to 2d, read_polygons_2d'
                #print pnt
                if pnt !=None:
                    cntr=cntr+1
                    ccc=False
                    bhi=None
                    #point bh identifier
                    #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1)], 3:newcoord index1(x), 4:distance , 5:cross]]
                    for planes in range(0,len(planenormalslist)):
                        if ccc==False:
                            epsbn=epsbn_ratio*planenormalslist[planes][4]
                            eps=eps_ratio*planenormalslist[planes][4]
                            if planes==0:
                                if round(pnt.X, 2) >= planenormalslist[planes][3]-epsbn and round(pnt.X, 2) <= planenormalslist[planes][3]+eps:
                                    bhi=[planenormalslist[planes][0]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                elif round(pnt.X, 2) > planenormalslist[planes][3]+eps and round(pnt.X, 2) < planenormalslist[planes][3]+planenormalslist[planes][4]-eps:
                                    bhi=[planenormalslist[planes][0],planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                elif round(pnt.X, 2) >= planenormalslist[planes][3]+planenormalslist[planes][4]-eps and round(pnt.X, 2)<=planenormalslist[planes][3]+planenormalslist[planes][4]+eps:
                                    bhi=[planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True


                            elif planes==len(planenormalslist)-1:

                                if round(pnt.X, 2) >= planenormalslist[planes][3]-eps and round(pnt.X, 2) <= planenormalslist[planes][3]+eps:
                                    bhi=[planenormalslist[planes][0]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                if round(pnt.X, 2) > planenormalslist[planes][3]+eps and round(pnt.X, 2) < planenormalslist[planes][3]+planenormalslist[planes][4]-eps:
                                    bhi=[planenormalslist[planes][0],planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                elif round(pnt.X, 2) >= planenormalslist[planes][3]+planenormalslist[planes][4]-eps and round(pnt.X, 2)<=planenormalslist[planes][3]+planenormalslist[planes][4]+epsbn:
                                    bhi=[planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True

                            else:

                                if round(pnt.X, 2) >= planenormalslist[planes][3]-eps and round(pnt.X, 2) <= planenormalslist[planes][3]+eps:
                                    bhi=[planenormalslist[planes][0]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                elif round(pnt.X, 2) > planenormalslist[planes][3]+eps and round(pnt.X, 2) < planenormalslist[planes][3]+planenormalslist[planes][4]-eps:
                                    bhi=[planenormalslist[planes][0],planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
                                elif round(pnt.X, 2) >= planenormalslist[planes][3]+planenormalslist[planes][4]-eps and round(pnt.X, 2)<=planenormalslist[planes][3]+planenormalslist[planes][4]+eps:
                                    bhi=[planenormalslist[planes][1]]
                                    #polygon point coordination appending
                                    pnts.append([round(pnt.X, 2),pnt.Y,bhi])
                                    ccc=True
        polygons_2d_list.append([row[0],pnts,{}])
        #polygons_2d_list = [ [polygon,[ [polygon vertics points: x,y, [bhindex]],...] , dic lit ],... ]
    #######################################
    for i in polygons_2d_list:
        bhindexes=list()
        bhindexestemp=list()
        #making the index list
        for j in i[1]:
            if j[2][0] not in bhindexestemp:
                if j[2][0] != lastbhindex:
                    bhindexestemp.append(j[2][0])
        bhindexestemp=sorted(bhindexestemp)
        for y in range(0,len(bhindexestemp)):
            bhindexes.append([bhindexestemp[y],[]])
            #bhindexes=[ [bhindex, [[point_id,x,y],...] ],...   ]
        ###################
        #adding point index
        newvertlist=list()
        cnt=0
        for jj in i[1]:
            cnt=cnt+1
            newvertlist.append([cnt,jj[0],jj[1],jj[2]])
        #newvertlist=[ [point_id,x,y,bhindex],...]
        #####################
        #extracting the point based on the bhindexes
        for bhin in bhindexes:
            for vert in newvertlist:
                if bhin[0] in vert[3]:
                    if bhin[0]-1 not in vert[3]:
                        bhin[1].append(vert)
                elif vert[3]== [bhin[0]+1 ]:
                    bhin[1].append(vert)
        bhindexes_new=list()
        for bhinn in bhindexes:
            allthesame=True
            for poit in bhinn[1]:
                if poit[3]!=[bhinn[0]]:
                    allthesame=False
            if allthesame==False:
                bhindexes_new.append(bhinn)
        #adding the first point to the list if it is not existed
        for inds in bhindexes_new:
            if [inds[1][0][1],inds[1][0][2],inds[1][0][3]] != [inds[1][-1][1],inds[1][-1][2],inds[1][-1][3]]:

                inds[1].append([ inds[1][-1][0]+1,inds[1][0][1] ,inds[1][0][2] ,inds[1][0][3] ])
        i[1]=bhindexes_new

    return polygons_2d_list
#polygons_2d_list=read_polygons_2d(planenormalslist,epsbn_ratio,eps_ratio)
##########################################################################################################################################################################
def rawdata_2d_preparation(planenormalslist,rawdata):
    #preparing the rawdata
    rawdata_2d=list()
    for planess in range(0,len(planenormalslist)):
        for data in rawdata:
            if data[0]== planenormalslist[planess][0]:
                rawdata_2d.append([data[0],planenormalslist[planess][3],((data[2]+data[3])/2),data[4]])
            if planess==len(planenormalslist)-1:
                if data[0]== planenormalslist[planess][1]:
                    rawdata_2d.append([data[0],planenormalslist[planess][3]+planenormalslist[planess][4],((data[2]+data[3])/2),data[4]])
                #rawdata_2d=[bhindex,x,y,lit]
    return rawdata_2d
#rawdata_2d=rawdata_2d_preparation(planenormalslist,rawdata)
##########################################################################################################################################################################
def polygon_identifier(rawdata_2d,polygons_2d_list):
    for rawd in rawdata_2d:
        pnt = arcpy.Point(rawd[1],rawd[2])
        if rawd[3] not in ["bottombox", "fault","Fault", 63]:
            for polygonss in polygons_2d_list:
                if pnt.within(polygonss[0],"BOUNDARY")==True:
                    polygonss[2][rawd[3]]=polygonss[2].get(rawd[3],0)+1
    return polygons_2d_list
#polygons_2d_list=polygon_identifier(rawdata_2d,polygons_2d_list)
##########################################################################################################################################################################
def points_2d_to_3d_transfer(polygons_2d_list,planenormalslist,epsbn_ratio,eps_ratio):
    #transfering 2d points to 3d points:
    #polygons_2d_list = [
        #polgonss: [
            # polygon,
                     #[  vert: [polygon vertics points: x,y, bhindex,...] ,
                         # dic lit
                             #]
                                #,...                    ]
    #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)], 3:newcoord index1(x), 4:distance , 5:cross]]
    polygns_3d=list()
    for polgonss in polygons_2d_list:
        for vert in polgonss[1]:
            #polgonss[1]=[  **vert=[bhindex, [[point_id,x,y] ,...]** ],...   ]
            polygons_3d_point_list2=list()
            for plns in range(0,len(planenormalslist)):
                if planenormalslist[plns][0]==vert[0]:
                    for pont in vert[1]:
                        ###########
                        a=planenormalslist[plns][5][0]
                        b=planenormalslist[plns][5][1]
                        d=planenormalslist[plns][5][3]
                        m=pont[1]-planenormalslist[plns][3]
                        if round(m,2)==0.00 or round(m,2)==-0.00:
                            m=0
                        z=pont[2]
                        ybh1=planenormalslist[plns][2][1]
                        xbh1=planenormalslist[plns][2][0]
                        ybh2=planenormalslist[plns][2][3]
                        xbh2=planenormalslist[plns][2][2]
                        #defining parameters
                        A=1+math.pow(float(a)/b,2)
                        B=(float(2*a*ybh1)/b)-2*xbh1+(float(2*a*d)/math.pow(b,2))
                        C=math.pow(xbh1,2)+math.pow(ybh1,2)-math.pow(m,2)+math.pow(float(d)/b,2) + float(2*ybh1*d)/b
                        inside_sqrt=math.pow(B,2)-4*A*C
                        if round(inside_sqrt,1)==-0.0:
                            inside_sqrt=0
                        whole_sqrt=math.sqrt(inside_sqrt)
                        ###########
                        #finding x and y
                        x1=float(-B+whole_sqrt)/(2*A)
                        x2=float(-B-whole_sqrt)/(2*A)
                        y1=(float(-d-(a*x1))/b)
                        y2=(float(-d-(a*x2))/b)
                        #x1=round(x1,1)
                        #x2=round(x2,1)
                        ################
                        #applying boundary conditions
                        epsbn_ratio_3d=epsbn_ratio*1.4142*planenormalslist[plns][4]
                        eps_ratio_3d=eps_ratio*1.4142*planenormalslist[plns][4]
                        len_planenormallist= len(planenormalslist)
                        x,y = boundaryconditions.boundaryconditions(x1,x2,y1,y2,xbh1,xbh2,ybh1,ybh2,len_planenormallist,plns,epsbn_ratio_3d,eps_ratio_3d)
                        ############
                        #append
                        polygons_3d_point_list2.append([[x,y,z],pont[0]])
                    ###############################################
                    #ArcGIS bugs:
                    polygons_3d_point_list2=arcgis_problems(polygons_3d_point_list2)
                    #makepolygons
                    polygons_3d_point_list=list()
                    for tt in polygons_3d_point_list2:
                        polygons_3d_point_list.append(tt[0])
                    polygontemp=arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in polygons_3d_point_list]),"Unknown",True,False)
                    #print "polygontemp.pointCount", polygontemp.pointCount
                    #Lithology dictionary max
                    max_list=list({key for key, value in polgonss[2].items() if value == max(polgonss[2].values())})
                    if len(max_list)==0:
                        print "##################"
                        print "Lithology not found!!"
                        print "##################"
                        lit="Not_Found"
                    elif len(max_list)>1:
                        print "##################"
                        print "More than 1 Lithology found!!", max_list
                        print "##################"
                        lit=str()
                        for bgg in max_list:
                            lit=lit+str(bgg)+"_"
                    else:
                        lit=max_list[0]
                    #################################################
                    polygns_3d.append([lit,polygons_3d_point_list,polygontemp])
                    #polygns_3d=[[0:lit ,1:polygonpoints, 2: 3dpolygon],.....]
    # 2021 matplotlib presentation:
    import mpl_toolkits.mplot3d as a3
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    import numpy as np
    #find xyz minmax
    x_min=None
    x_max=None
    y_min=None
    y_max=None
    z_min=None
    z_max=None
    col_dic=dict()
    for i in polygns_3d:
        for p in i[1]:
            if x_min==None: x_min=p[0]
            elif p[0]<  x_min: x_min=  p[0]
            if x_max==None: x_max=p[0]    
            elif p[0]>  x_max: x_max=  p[0]

            if y_min==None:y_min=p[1]
            elif p[1]<  y_min: y_min=  p[1]
            if y_max==None:y_max=p[1] 
            elif p[1]>  y_max: y_max=  p[1]

            if z_min==None:z_min=p[2]
            elif p[2]<  z_min: z_min=  p[2]
            if z_max==None:z_max=p[2]   
            elif p[2]>  z_max: z_max=  p[2]
        #color dict
        col_dic[i[0]]=col_dic.get(i[0],colors.rgb2hex(np.random.rand(3)))

    fig = plt.figure()
    ax = a3.Axes3D(fig)
    for i in polygns_3d:
        polis=[tuple(n) for n in i[1]]
        tri=a3.art3d.Poly3DCollection([polis])
        tri.set_color(col_dic[i[0]])
        tri.set_edgecolor('k')
        ax.add_collection3d(tri)
    ax.set_xlim3d(left=x_min,right=x_max)
    ax.set_ylim3d(bottom=y_min, top=y_max)
    ax.set_zlim3d(bottom=z_min, top=z_max)
    ax.set_xlabel('X (EAST)')
    ax.set_ylabel('Y (NORTH)')
    ax.set_zlabel('Z')
    plt.show()                
    return polygns_3d
#polygns_3d=points_2d_to_3d_transfer(polygons_2d_list,planenormalslist,epsbn_ratio,eps_ratio)
##########################################################################################################################################################################
def arcgis_problems(polygons_3d_point_list2):
    #ArcGIS have problem with completly vertical boreholes, so we add a
    #small amount added to the x and y  of the borehole with the same coordination
    '''poltemp=list()
    for pol1 in range (0,len(polygons_3d_point_list2)):
        epsil=0
        for pol2 in range (0,len(polygons_3d_point_list2)):
            if pol1 != pol2:
                if polygons_3d_point_list2[pol1][0][0]==polygons_3d_point_list2[pol2][0][0] and polygons_3d_point_list2[pol1][0][1]==polygons_3d_point_list2[pol2][0][1]:
                    epsil=epsil+0.01
                    polygons_3d_point_list2[pol2][0][0]=polygons_3d_point_list2[pol2][0][0]+epsil
                    polygons_3d_point_list2[pol2][0][1]=polygons_3d_point_list2[pol2][0][1]+epsil
    #############################################
    #ArcGIS bug related to the same distance between Xs and Ys
    #if dist x1,x2 = dist y1,y2,  it can not make the line properly.
    #So we check in BHs, and in case they are the same, we add an epsilon
    for pol3 in range (0,len(polygons_3d_point_list2)-1):
        if round(polygons_3d_point_list2[pol3+1][0][0] - polygons_3d_point_list2[pol3][0][0],2)==round(polygons_3d_point_list2[pol3+1][0][1] - polygons_3d_point_list2[pol3][0][1],2):
            polygons_3d_point_list2[pol3+1][0][1]=polygons_3d_point_list2[pol3+1][0][1]+0.01'''
    zmin=None
    zmax=None
    for pol1 in range (0,len(polygons_3d_point_list2)):
        if zmin==None or zmin > polygons_3d_point_list2[pol1][0][2]:
            zmin=polygons_3d_point_list2[pol1][0][2]
        if zmax==None or zmax < polygons_3d_point_list2[pol1][0][2]:
            zmax=polygons_3d_point_list2[pol1][0][2]
    #if zmin !=zmax:
    for pol2 in range (0,len(polygons_3d_point_list2)):
        #print polygons_3d_point_list2[pol2][0][0],float(polygons_3d_point_list2[pol2][0][2]-zmax),(zmin-zmax)
        polygons_3d_point_list2[pol2][0][0]=polygons_3d_point_list2[pol2][0][0]+(float(polygons_3d_point_list2[pol2][0][2]-zmax)/(zmin-zmax))*0.01
    #############################################
    #the first and last point have to be the same
    #polygons_3d_point_list2[0][0]=polygons_3d_point_list2[-1][0]
    polygons_3d_point_list2=polygons_3d_point_list2[:len(polygons_3d_point_list2)-1]
    #sort by pointid
    #print "polygons_3d_point_list2\n"
    #for i in polygons_3d_point_list2: print i
    polygons_3d_point_list2=sorted(polygons_3d_point_list2,key=itemgetter(1))
    #print "polygons_3d_point_list2 after sort\n"
    #for i in polygons_3d_point_list2: print i
    return polygons_3d_point_list2
    #polygons_3d_point_list2=arcgis_problems(polygons_3d_point_list2)
    ##########################################################################################################################################################################
    
