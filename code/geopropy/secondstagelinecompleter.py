from operator import itemgetter
import anglefinder
import connectleftandrightstage2_v2
#####################################################################################
def changesitsecondstage(newsitpoint,poi,mainpointlist,angles):  #function to change points situation

    poi[8]=3
    if len(newsitpoint) > 0:
        for gg in newsitpoint:
            preventer_temp=False
            for uy in mainpointlist:
                if gg[0][0]==uy[1] and gg[1]==uy[5]:
                    ########################################
                    #update angles
                    angles=anglefinder.angleupdater(gg,uy,angles)
                    preventer_temp=True
                    ########################################
                    if uy[8]==2:
                        uy[8]=0
                    elif uy[8]==3:
                        uy[8]=1
                elif gg[0][1]==uy[1] and gg[2]==uy[5]:
                    ########################################
                    #update angles
                    if preventer_temp==False:
                        angles=anglefinder.angleupdater(gg,uy,angles)
                    ########################################
                    if uy[8]==1:
                        uy[8]=0
                    elif uy[8]==3:
                        uy[8]=2
    return mainpointlist,angles,poi
#####################################################################################
def secondstagelinecompleter(mainpointlist,prior,mainpolylist,rawdata,angles,indextemplist_with_coords):
    alreadydonepolies=list()
    #exclude virtual bhs points
    for j in range(0,len(mainpointlist)):
        if mainpointlist[j][1] == indextemplist_with_coords[0][1] or mainpointlist[j][1] == indextemplist_with_coords[-1][1]:
            mainpointlist[j][8]=3
        elif mainpointlist[j][1] == indextemplist_with_coords[1][1]:
            if mainpointlist[j][8] not in [3,2]:
                mainpointlist[j][8]=0
                mainpointlist[j][7]="left_connected"
        elif mainpointlist[j][1] == indextemplist_with_coords[-2][1]:
            if mainpointlist[j][8] not in [3,1]:
                mainpointlist[j][8]=0
                mainpointlist[j][7]="right_connected"
    #####################################################################################
    #How the points that their line removed and their procedure changed recreate the new lines:
    #because the removed lines are always from lower priorities, when the loop in the next line
    #go to the next priority, they will detect by their new point situations and new lines will
    #be created for them.
    for i in prior:
        preferred_angle=i[4]
        notcompletedpoints=list()
        for ee in mainpointlist:
            if ee[8] != 3:
                notcompletedpoints.append(ee)
        notcompletedpoints=sorted(notcompletedpoints,key=itemgetter(0))
        samepriorpoints=list()
        for n in notcompletedpoints:
            if n[3]==i[0]:
                samepriorpoints.append(n)
        for u in range(0,len(indextemplist_with_coords)):
            for poi in samepriorpoints:
                if poi[1]==indextemplist_with_coords[u][1]:
                    if poi[8]==1: #left connected.
                        #alreadydonepolies, mainpolylist, poi ,newsitpoint = connectleftandrightstage2.connectrightstage2(preferred_angle,poi,mainpolylist,x,y,indextemplist,alreadydonepolies,rawdata,boidtable,angles,mainpointlist)
                        alreadydonepolies, mainpolylist, poi ,newsitpoint=connectleftandrightstage2_v2.sidesstage2(preferred_angle,poi,mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,"right",indextemplist_with_coords)
                        #change sit:
                        mainpointlist,angles,poi=changesitsecondstage(newsitpoint,poi,mainpointlist,angles)
                    elif poi[8]==2: #right connected
                        #alreadydonepolies, mainpolylist, poi, newsitpoint = connectleftandrightstage2.connectleftstage2(preferred_angle, poi,mainpolylist,x,y,indextemplist,alreadydonepolies,rawdata,boidtable,angles,mainpointlist)
                        alreadydonepolies, mainpolylist, poi ,newsitpoint=connectleftandrightstage2_v2.sidesstage2(preferred_angle,poi,mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,"left",indextemplist_with_coords)
                        #change sit:
                        mainpointlist,angles,poi=changesitsecondstage(newsitpoint,poi,mainpointlist,angles)
                    elif poi[8]==0: #both sides
                        alreadydonepolies, mainpolylist, poi,newsitpoint = connectleftandrightstage2_v2.connecbothsides(preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,indextemplist_with_coords)
                        #change sit:
                        mainpointlist,angles,poi=changesitsecondstage(newsitpoint,poi,mainpointlist,angles)
                    else:
                        print 'there is a point out of the right loop secondstagelinecompleter.py -> else', poi
    return mainpointlist, mainpolylist
