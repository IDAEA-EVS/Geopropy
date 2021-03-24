import math
from operator import itemgetter

def cross_product_and_planenormalslist_maker(indextemplist_with_coords):
    '''determine the new coordinates
    find the max and min of x and y coords and substract it
    find the plane equation between every two bh
    finding the plane equation
    https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FEquationofaPlane3Points
    ab=[0,0,1] (vector parallel to borehole)
    ac=[x2-x1,y2-y1,0] (horizontal vector between bhs)'''
    planenormalslist=list()
    bhzero=0
    for bh in range(1,len(indextemplist_with_coords)-2): #excluding first and last bh (virtual ones)
        #3 points coordinations
        xbh1=indextemplist_with_coords[bh][2]
        ybh1=indextemplist_with_coords[bh][3]
        xbh2=indextemplist_with_coords[bh+1][2]
        ybh2=indextemplist_with_coords[bh+1][3]
        cross=[ ybh2-ybh1 , xbh1-xbh2 ,0, ((xbh2*ybh1)-(xbh1*ybh2))]
        #cross=[a,b,c,d] ax+by+cz+d=0
        distt=math.sqrt( math.pow((xbh2-xbh1),2)   + math.pow((ybh2-ybh1),2) )

        planenormalslist.append([indextemplist_with_coords[bh][1],indextemplist_with_coords[bh+1][1],[xbh1,ybh1,xbh2,ybh2],bhzero, distt, cross])
        #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)], 3:newcoord index1(x), 4:distance , 5:cross],...]
        #for the last borehole
        if bh==len(indextemplist_with_coords)-3:
            planenormalslist.append([indextemplist_with_coords[bh+1][1],indextemplist_with_coords[bh+1][1],[xbh1,ybh1,xbh2,ybh2],bhzero, distt, cross])
        
        bhzero=bhzero+distt
    #############
    return planenormalslist

#########################################################
def surface_point_projector(planenormalslist,temp_points):
    #planenormalslist=[[0:index1,  1:index2, 2:[x,y (index1),x,y (index2)], 3:newcoord index1(x), 4:distance , 5:cross],...]
    #temp_points= prio,[bp_list,None,x,y,z,type,polaroty,angle,0,None]
    #####
    
    for each_p in temp_points:
        temp_point=list()
        for surf_pnt in each_p[1]:
            #print surf_pnt
            point_to_plane_dist__=None
            for bh_ind_pair in surf_pnt[0]: #for every bh pair
                for plane in planenormalslist:
                    #print "plane\n",plane
                    if bh_ind_pair[0]==plane[0] and bh_ind_pair[1]==plane[1]:
                        point_to_plane_dist_=point_to_plane_dist_function(plane[5],surf_pnt[2:5],plane[2])
                        #print plane[0],plane[1],"\n",surf_pnt[2:5],"\n",point_to_plane_dist_
                        cross_t=plane[5]
                        bhs_t=plane[2]
                        bhss=bh_ind_pair
                        if point_to_plane_dist__==None or point_to_plane_dist_<point_to_plane_dist__:
                            point_to_plane_dist__=point_to_plane_dist_
                            closest_bhpair=bhss
                            closest_cross=cross_t
                            bhs_coords=bhs_t
            #print "closest_bhpair\n",closest_bhpair
            x_new_bot=( float(closest_cross[1])/closest_cross[0] + float(closest_cross[0])/closest_cross[1] ) #b/a+a/b
            x_new=float(
                (float(closest_cross[1])/closest_cross[0]) * surf_pnt[2] #b/a *xn
                -surf_pnt[3] #-yn
                -float(closest_cross[3])/float(closest_cross[1]) #-d/b
            )/x_new_bot
            y_new=-(float(closest_cross[0])/closest_cross[1]) * x_new -float(closest_cross[3])/float(closest_cross[1]) #-a/b*xnew-d/b

            topo_pnt_ind=( float(x_new-bhs_coords[0]) / (bhs_coords[2]-bhs_coords[0]) )+ closest_bhpair[0]       
            temp_point.append([closest_bhpair[0],closest_bhpair[1],topo_pnt_ind,x_new,y_new,surf_pnt[4],surf_pnt[5],surf_pnt[6],surf_pnt[7],0,None])
        temp_point=sorted(temp_point,key=itemgetter(2))
        each_p[1]=temp_point
    #####
    return temp_points
    
##############################################################
def point_to_plane_dist_function(plane,pnt,bhcords):
    n = abs((plane[0] * pnt[0] + plane[1] * pnt[1] + plane[2] * pnt[2] + plane[3]))  
    e = (math.sqrt(plane[0] * plane[0] + plane[1] * plane[1] + plane[2] * plane[2])) 
    dist=float(n)/e

    if bhcords[0]<=pnt[0] and pnt[0]<=bhcords[2] and bhcords[1]<=pnt[1] and pnt[1]<=bhcords[3]:
        pass
    else: 
        dist_cal=lambda pnt,x,y: math.sqrt(math.pow(pnt[0]-x,2)+math.pow(pnt[1]-y,2))
        dist=min(
            dist_cal(pnt,bhcords[0],bhcords[1]),
            dist_cal(pnt,bhcords[2],bhcords[3])
        )
    return dist
