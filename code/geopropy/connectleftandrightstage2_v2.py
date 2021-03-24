#########################################################################################################################################
def pointlistmaker(pnts):
    if pnts[0][0]<pnts[1][0]:
        despoint=[pnts[0],pnts[1]]
    else:
        despoint=[pnts[1],pnts[0]]
    return despoint
#########################################################################################################################################            
import continuedlinecreator
import bhlinecreator
from operator import itemgetter
from math import sqrt, pow, tan, radians
import anglefinder
import math
from segmentlineintersection3d import segmentlineintersection3d
import deleteexistedline
def bh_dist(indextemplist_with_coords,firstbh,side,secondbh):
    for n in indextemplist_with_coords:
        if n[1]==firstbh and side=="right" or n[1]==secondbh and side=="left":
            xcen = n[2]
            ycen = n[3]
        elif n[1]==secondbh and side=="right" or n[1]==firstbh and side=="left":
            bhidbothside=n[0]    
            xbothside = n[2]
            ybothside = n[3]
    #2 bh distance
    distbh=sqrt( pow((xcen-xbothside),2)   + pow((ycen-ybothside),2) )
    return distbh,ybothside,xbothside

#distbh,ybothside,xbothside=bh_dist(indextemplist_with_coords,firstbh,side,secondbh)
#########################################################################################################################################
def sidesstage2(preferred_angle,poi,mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,side,indextemplist_with_coords):
    newsitpoint=list()
    conti_temp=False
    if side=='left':
        firstbh=poi[1]-1
        secondbh=poi[1]
    else:
        firstbh=poi[1]
        secondbh=poi[1]+1
    ########################################################
    #Here, the algorithm for line by preferred angle introduced by user in chronopriority table will be considered.
    if preferred_angle !=None: #this is the angle in access database
        tan_angle=math.tan(math.radians(preferred_angle))

        distbh,ybothside,xbothside=bh_dist(indextemplist_with_coords,firstbh,side,secondbh)

        zdif=abs(tan_angle * distbh)
        if (preferred_angle>0 and side=='right') or (preferred_angle<0 and side=='left'): #this pointlist is from the output of continuedLineCreator
            znew=poi[5][2]-zdif
        else:
            znew=poi[5][2]+zdif
        if poi[4] !="fault":
            pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
            polytemp22=None
            nexts22=True
        elif poi[4] =="fault":  #preferred angle defined in database, but the layer is a fault                        
            if side=='right':
                alreadydonepoliestmep=list()
                polytemp22, pointlist21, alreadydonepolies21 = continuedlinecreator.continuedLineCreator(poi[5][2],poi[1]-1,poi[1],poi[1]+1,poi[3],mainpolylist,side,poi[2],indextemplist_with_coords,alreadydonepoliestmep)
                if (pointlist21[1][2] <= pointlist21[0][2] and preferred_angle<0) or (pointlist21[1][2] >= pointlist21[0][2] and  preferred_angle>0):
                    pointlist22=pointlistmaker([poi[5],[xbothside,ybothside,znew]])
                    polytemp22=None
                    nexts22=True
                else:
                    nexts22=False

            elif side=='left':
                alreadydonepoliestmep=list()
                polytemp22, pointlist21, alreadydonepolies21 = continuedlinecreator.continuedLineCreator(poi[5][2],poi[1],poi[1]+1,poi[1]-1,poi[3],mainpolylist,side,poi[2],indextemplist_with_coords,alreadydonepoliestmep)
                if (pointlist21[0][2] <= pointlist21[1][2] and preferred_angle<0) or (pointlist21[0][2] >= pointlist21[1][2] and preferred_angle>0):
                    pointlist22=pointlistmaker([poi[5],[xbothside,ybothside,znew]])
                    polytemp22=None
                    nexts22=True
                else:
                    nexts22=False
        #check for intersection with higher priority line or bottom box
        if nexts22==True:
            polylisttemp=list()
            for v in mainpolylist: #temporary polylist of the one with disjoint=False
                if v[0]==firstbh and v[1]==secondbh:
                    bh1temp=v[0]
                    bh2temp=v[1]
                    for vv in v[2]:
                            if vv[0]>poi[3] or vv[1]=="bottombox":
                                inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                if  inters!= False:
                                    conti_temp=True
            if conti_temp==True:
                polytemp=polytemp22
                pointlist=pointlist22
    ########################################################
    if conti_temp==False:
        if side=='right':
            polytemp, pointlist, alreadydonepolies = continuedlinecreator.continuedLineCreator(poi[5][2],poi[1]-1,poi[1],poi[1]+1,poi[3],mainpolylist,side,poi[2],indextemplist_with_coords,alreadydonepolies)
        elif side=='left':
            polytemp, pointlist, alreadydonepolies = continuedlinecreator.continuedLineCreator(poi[5][2],poi[1],poi[1]+1,poi[1]-1,poi[3],mainpolylist,side,poi[2],indextemplist_with_coords,alreadydonepolies)        
        polylisttemp=list()
        conti_temp=False
        for v in mainpolylist: #temporary polylist of the one with disjoint=False
            if v[0]==firstbh and v[1]==secondbh:
                bh1temp=v[0]
                bh2temp=v[1]
                ##############################################################################################################
                #intrusion:
                #if the continue line in intrusion priority goes in the direction of the bottom of the cross section, do it
                #if not, middle of the bottom box
                if poi[4]=="intrusion":
                    if (pointlist[0][2]>pointlist[1][2] and side=='right') or (pointlist[0][2]<pointlist[1][2] and side=='left') :
                        for vv in v[2]:
                            inters=segmentlineintersection3d(pointlist,[vv[3],vv[4]])
                            if  inters!= False:
                                if vv[0]> poi[3] or vv[1]=="bottombox":
                                    conti_temp=True
                    if  (pointlist[0][2] <= pointlist[1][2] and side=='right') or (pointlist[0][2]>pointlist[1][2] and side=='left') or conti_temp==False:  #go to the middle of the bottom box
                        for vv in v[2]:
                            if vv[1]=="bottombox":
                                Midpoint = [float( vv[3][0]+ vv[4][0])/2,float( vv[3][1]+ vv[4][1])/2,float( vv[3][2]+ vv[4][2])/2]
                        pointlist=pointlistmaker([poi[5],Midpoint])
                        polytemp=None
                        conti_temp=True
                #################################################################################################################
                else:
                    for vv in v[2]:
                        if vv[0]> poi[3] or vv[1]=="bottombox": #polytemp.disjoint(vv[2])==False:
                            inters=segmentlineintersection3d(pointlist,[vv[3],vv[4]])
                            if  inters!= False:
                                conti_temp=True
    if conti_temp==False: #intersection with the next bh
        #angle
        #angles= [ [0:prio_num, 1:type, 2:tan_angle, 3:quantity, 4:from left (up or down) ,5:[ [index1,index2,startpoint,endpoint] ]   ] ,...]
        tan_angle=None
        for tempang in angles:
            if tempang[0]==poi[3] and tempang[2] != None:
                tan_angle=tempang[2]
        inters_temp=False
        distbh,ybothside,xbothside=bh_dist(indextemplist_with_coords,firstbh,side,secondbh)
        #############################
        if tan_angle == None: #if the data for angle is not available
            tan_angle, upordown_temp = anglefinder.angleestimator( poi, mainpointlist, mainpolylist,side)
        #############################
        if tan_angle != None: #there is an angle (in angles or using angle estimator function)
            #elevation difference (zdif)
            zdif=tan_angle * distbh
            if (pointlist[0][2]>pointlist[1][2] and side=='right' and tan_angle>0) or (pointlist[0][2]<pointlist[1][2] and side=='left' and tan_angle>0) or (pointlist[1][2]>pointlist[0][2] and side=='right' and tan_angle<0) or (pointlist[1][2]<pointlist[0][2] and side=='left' and tan_angle<0) : #this pointlist is from the output of continuedLineCreator
                znew=poi[5][2]-zdif
            else:
                znew=poi[5][2]+zdif
            pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
            polytemp22=None
            #check for intersection with higher priority line or bottom box
            polylisttemp=list()
            for v in mainpolylist: #temporary polylist of the one with disjoint=False
                if v[0]==firstbh and v[1]==secondbh:
                    bh1temp=v[0]
                    bh2temp=v[1]
                    for vv in v[2]:
                            if vv[0]>poi[3] or vv[1]=="bottombox":
                                inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                if  inters!= False:
                                    inters_temp=True
            if inters_temp==True:
                polytemp=polytemp22
                pointlist=pointlist22
        ########################################################################
        if (tan_angle ==None or inters_temp==False) and poi[4] !="fault": #no information or without valid intersection - try parallel line
            tan_angle=math.tan(math.radians(0.01))
            #elevation difference (zdif)
            zdif=tan_angle * distbh
            if (pointlist[0][2]>pointlist[1][2] and side=='right') or (pointlist[0][2]<pointlist[1][2] and side=='left') : #this pointlist is from the output of continuedLineCreator
                znew=poi[5][2]-zdif
            else:
                znew=poi[5][2]+zdif
            pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
            polytemp22=None
            #check for intersection with higher priority line or bottom box
            polylisttemp=list()
            for v in mainpolylist: #temporary polylist of the one with disjoint=False
                if v[0]==firstbh and v[1]==secondbh:
                    bh1temp=v[0]
                    bh2temp=v[1]
                    for vv in v[2]:
                            if vv[0]>poi[3] or vv[1]=="bottombox":
                                inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                if  inters!= False:
                                    inters_temp=True
            if inters_temp==True:
                polytemp=polytemp22
                pointlist=pointlist22
        ########################################################################
        if tan_angle ==None or inters_temp==False: #if no information or without valid intersection
            ########################################################################
            #finding the next bh Lithology
            if side=='right':
                bhlinelist = bhlinecreator.bhlinecreator(secondbh,indextemplist_with_coords,rawdata) #return bhlinelist
            elif side == 'left':
                bhlinelist = bhlinecreator.bhlinecreator(firstbh,indextemplist_with_coords,rawdata) #return bhlinelist
            litOtherBh = False
            for qq in bhlinelist: #bhlinelist=[ [polytemp,lit] , [polytemp,lit], .... ]
                #print "pointlist,qq[0]",pointlist,qq[0]
                if segmentlineintersection3d(pointlist,qq[0]) != False: #polytemp.disjoint(qq[0])==False:
                    litOtherBh=qq[2]
            #finding the lithology in the borehole
            rawdatainpointbh=list()
            for r in rawdata:
                if r[0]==poi[1] and r[2]!=r[3]:
                    rawdatainpointbh.append(r)
            rawdatainpointbh=sorted(rawdatainpointbh,key=itemgetter(2),reverse=True)
            litTop=False
            for kk in range(0,len(rawdatainpointbh)-1):
                if  rawdatainpointbh[kk+1][2] <= poi[5][2] and poi[5][2]  <= rawdatainpointbh[kk][3]:
                    litTop=rawdatainpointbh[kk][4]
            ##########################################################################
            if poi[4]=='fault':
                for i in mainpolylist:
                    if i[0]==bh1temp and i[1]==bh2temp:
                        templineslist1=list()
                        templineslist2=list()
                        for ii in i[2]:
                            if ii[0]<poi[3]:
                                templineslist1.append(ii)
                            else:
                                templineslist2.append(ii)
                        templineslist1=sorted(templineslist1,key=itemgetter(0))
                        templineslist2=sorted(templineslist2,key=itemgetter(0)) #this is not reverse=True because it will correct in delete existed line
                        Midpoint1 = [float( templineslist1[0][3][0]+ templineslist1[0][4][0])/2,float( templineslist1[0][3][1]+ templineslist1[0][4][1])/2,float( templineslist1[0][3][2]+ templineslist1[0][4][2])/2]
                        Midpoint2 = [float( templineslist2[0][3][0]+ templineslist2[0][4][0])/2,float( templineslist2[0][3][1]+ templineslist2[0][4][1])/2,float( templineslist2[0][3][2]+ templineslist2[0][4][2])/2]
                '''if litTop==litOtherBh or litOtherBh=='bottombox' : #go to the middle of lower priority line
                    if side=="right":
                        if (pointlist[1][2]-pointlist[0][2] <= 0 and poi[5][2]-Midpoint1[2] <= 0) or (pointlist[1][2]-pointlist[0][2] >=0 and poi[5][2]-Midpoint1[2] >=0):
                            pointlist=pointlistmaker([poi[5],Midpoint1])
                            polytemp=None
                        else:
                            pointlist=pointlistmaker([poi[5],Midpoint2])
                            polytemp=None

                    elif side=="left":
                        if (pointlist[0][2]-pointlist[1][2] <= 0 and poi[5][2]-Midpoint1[2] <= 0) or (pointlist[0][2]-pointlist[1][2] >=0 and poi[5][2]-Midpoint1[2] >=0):
                            pointlist=pointlistmaker([poi[5],Midpoint1])
                            polytemp=None
                        else:
                            pointlist=pointlistmaker([poi[5],Midpoint2])
                            polytemp=None
                else:
                    if side=="right":
                        if (pointlist[1][2]-pointlist[0][2] <= 0 and Midpoint2[2]-poi[5][2] <= 0) or (pointlist[1][2]-pointlist[0][2] >=0 and Midpoint2[2]-poi[5][2] >=0):
                            pointlist=pointlistmaker([poi[5],Midpoint2])
                            polytemp=None
                        else:
                            pointlist=pointlistmaker([poi[5],Midpoint1])
                            polytemp=None    
                    elif side=="left":
                        if (pointlist[0][2]-pointlist[1][2] <= 0 and Midpoint2[2]-poi[5][2] <= 0) or (pointlist[0][2]-pointlist[1][2] >=0 and Midpoint2[2]-poi[5][2] >=0):
                            pointlist=pointlistmaker([poi[5],Midpoint2])
                            polytemp=None
                        else:
                            pointlist=pointlistmaker([poi[5],Midpoint1])
                            polytemp=None'''
                #NEW ALG FOR FAULTS:
                if pointlist[1][2]-pointlist[0][2]<=0: p1p0="pos"
                else: p1p0="neg"
                if Midpoint1[2]-poi[5][2]>=0: poim1="pos"
                else: poim1="neg"
                ######
                if p1p0==poim1:
                    pointlist=pointlistmaker([poi[5],Midpoint1])
                    polytemp=None
                else:
                    pointlist=pointlistmaker([poi[5],Midpoint2])
                    polytemp=None


            else:
                if litTop==litOtherBh or litOtherBh=='bottombox' : #go to the middle of lower priority line
                    for i in mainpolylist:
                        if i[0]==bh1temp and i[1]==bh2temp:
                            templineslist=list()
                            for ii in i[2]:
                                if ii[0]<poi[3]:
                                    templineslist.append(ii)
                            templineslist=sorted(templineslist,key=itemgetter(0))
                            Midpoint = [float( templineslist[0][3][0]+ templineslist[0][4][0])/2,float( templineslist[0][3][1]+ templineslist[0][4][1])/2,float( templineslist[0][3][2]+ templineslist[0][4][2])/2]
                            pointlist=pointlistmaker([poi[5],Midpoint])
                            polytemp=None
                else: #higher priority
                    for i in mainpolylist:
                        if i[0]==bh1temp and i[1]==bh2temp:
                            templineslist=list()
                            for ii in i[2]:
                                if ii[0]>poi[3]:
                                    templineslist.append(ii)
                            templineslist=sorted(templineslist,key=itemgetter(0))
                            Midpoint = [float( templineslist[0][3][0]+ templineslist[0][4][0])/2,float( templineslist[0][3][1]+ templineslist[0][4][1])/2,float( templineslist[0][3][2]+ templineslist[0][4][2])/2]
                            pointlist=pointlistmaker([poi[5],Midpoint])
                            polytemp=None
            ##########################################################################
    #correct the line
    for v in mainpolylist: #temporary polylist of the one with disjoint=False
        if v[0]==firstbh and v[1]==secondbh:
            bh1temp=v[0]
            bh2temp=v[1]
            for vv in v[2]:
                inters=segmentlineintersection3d(pointlist,[vv[3],vv[4]])
                if  inters!= False:
                    if side=="right":
                        dist=sqrt((inters[0]-pointlist[0][0])**2+(inters[1]-pointlist[0][1])**2+(inters[2]-pointlist[0][2])**2)
                    elif side=="left":
                        dist=sqrt((inters[0]-pointlist[1][0])**2+(inters[1]-pointlist[1][1])**2+(inters[2]-pointlist[1][2])**2)
                    polylisttemp.append([vv,dist])
    if len(polylisttemp)>0:
        ##################################
        newsitpoint, mainpolylist, polytemp, pointlist = deleteexistedline.deleteexistedline_fun(pointlist,polytemp,polylisttemp,poi[3],mainpolylist,bh1temp,bh2temp,side)
        
        ##################################
    try:
        for cou in mainpolylist:
            if cou[0]==bh1temp and cou[1]==bh2temp:
                cou[2].append([ poi[3],poi[4] ,polytemp,pointlist[0],pointlist[1]])
    except:
        print 'polyline not appended connectleftandrightstage2.py'
        pass
    return alreadydonepolies,mainpolylist,poi,newsitpoint
#########################################################################################################################################    
def connecbothsides(preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,indextemplist_with_coords):
    ###################################################################################
    #Function to connect left and right of the points that are not connected      
    def bothsidesconnector(newsitpoint2,licou2,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,side,indextemplist_with_coords):
        if side=='left':
            firstbh=poi[1]-1
            secondbh=poi[1]
        else:
            firstbh=poi[1]
            secondbh=poi[1]+1
        #angle
        #angles= [ [0:prio_num, 1:type, 2:tan_angle, 3:quantity, 4:from left (up or down) ,5:[ [index1,index2,startpoint,endpoint] ]   ] ,...]
        tan_angle=None
        upordown=None
        inters_temp=False
        distbh,ybothside,xbothside=bh_dist(indextemplist_with_coords,firstbh,side,secondbh)
        ############################################################
        #preferred_angle code
        if preferred_angle !=None:
            tan_angle=math.tan(math.radians(preferred_angle))
            zdif=tan_angle * distbh
            if side=='right':
                znew=poi[5][2]+zdif
            else:
                znew=poi[5][2]-zdif   
            pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
            polytemp22=None
            polylisttemp=list()
            for v in mainpolylist: #temporary polylist of the one with disjoint=False
                if v[0]==firstbh and v[1]==secondbh:
                    bh1temp=v[0]
                    bh2temp=v[1]
                    for vv in v[2]:
                            if vv[0]>poi[3] or vv[1]=="bottombox":
                                inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                if  inters!= False:
                                    inters_temp=True
            if inters_temp==True:
                polytemp=polytemp22
                pointlist=pointlist22
        ############################################################
        if inters_temp==False:
            for tempang in angles:
                if tempang[0]==poi[3] and tempang[2] != None:
                    tan_angle=tempang[2]
                    upordown=tempang[4]
            ##################################
            if tan_angle == None and upordown == None:
                tan_angle, upordown = anglefinder.angleestimator( poi, mainpointlist, mainpolylist,side)
                '''if side=="left":
                    if upordown=="down":
                        upordown="up"
                    elif upordown=="up":
                        upordown="down"'''
            else:
                pass
            ###################################
            if tan_angle != None and upordown != None:
                #elevation difference (zdif)
                zdif=tan_angle * distbh
                '''if upordown=="down" and side=="right" or upordown=="up" and side=="left" : #this pointlist is from the output of continuedLineCreator
                    znew=poi[5][2]-zdif
                elif upordown=="up" and side=="right" or upordown=="down" and side=="left":
                    znew=poi[5][2]+zdif'''
                if upordown=="down":
                    znew=poi[5][2]-zdif
                elif upordown=="up":
                    znew=poi[5][2]+zdif
                pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
                polytemp22=None
                #check for intersection with higher priority line or bottom box
                polylisttemp=list()
                for v in mainpolylist: #temporary polylist of the one with disjoint=False
                    if v[0]==firstbh and v[1]==secondbh:
                        bh1temp=v[0]
                        bh2temp=v[1]
                        for vv in v[2]:
                                if vv[0]>poi[3] or vv[1]=="bottombox":
                                    inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                    if  inters!= False:
                                        inters_temp=True
                if inters_temp==True:
                    polytemp=polytemp22
                    pointlist=pointlist22
            ########################################################################
            if tan_angle ==None or inters_temp==False or upordown == None: #if no information or without valid intersection- try parallel
                tan_angle=math.tan(math.radians(0.01))
                upordown="up"
                #elevation difference (zdif)
                zdif=tan_angle * distbh
                if side=='right':
                    znew=poi[5][2]+zdif
                else:
                    znew=poi[5][2]-zdif
                pointlist22=pointlistmaker([  poi[5] , [xbothside,ybothside,znew] ])
                polytemp22=None
                #check for intersection with higher priority line or bottom box
                polylisttemp=list()
                for v in mainpolylist: #temporary polylist of the one with disjoint=False
                    if v[0]==firstbh and v[1]==secondbh:
                        bh1temp=v[0]
                        bh2temp=v[1]
                        for vv in v[2]:
                                if vv[0]>poi[3] or vv[1]=="bottombox":
                                    inters=segmentlineintersection3d(pointlist22,[vv[3],vv[4]])
                                    if  inters!= False:
                                        inters_temp=True
                if inters_temp==True:
                    polytemp=polytemp22
                    pointlist=pointlist22
            #############################################################################
            if tan_angle ==None or inters_temp==False or upordown == None: #if no information or without valid intersection
                #parallel line to identify the lithology in the other BH
                for n in indextemplist_with_coords:
                    if (side=='right' and n[1]==poi[1]+1) or (side=='left' and n[1]==poi[1]-1):
                        xt=n[2]
                        yt=n[3]
                pointtemlist=pointlistmaker([poi[5],[ xt,yt,poi[5][2] ] ])
                polytemptemp=None
                #finding the next bh Lithology in the intersection with parallel line
                if side=='right':
                    bh2temp=firstbh+1
                else:
                    bh2temp=poi[1]-1    
                bhlinelist = bhlinecreator.bhlinecreator(bh2temp,indextemplist_with_coords,rawdata) #return bhlinelist
                litOtherBh=False
                for qq in bhlinelist: #bhlinelist=[ [polytemp,lit] , [polytemp,lit], .... ]
                    if segmentlineintersection3d(pointtemlist,qq[0]) != False:
                        licou2=licou2+1
                        litOtherBh=qq[2]
                ################################################################
                if litTop==litOtherBh or litOtherBh==False or litOtherBh=='bottombox' : #go to the middle of lower priority line
                    for i in mainpolylist:
                        if i[0]==firstbh and i[1]==secondbh:
                            templineslist=list()
                            for ii in i[2]:
                                if ii[0]<poi[3]:
                                    templineslist.append(ii)
                            templineslist=sorted(templineslist,key=itemgetter(0))
                            #the ''checkk'' procedure is for checking the intersection of the new line with the other line with lower priority
                            checkk=False
                            for temp in range(0,len(templineslist)):
                                if checkk==False:
                                    Midpoint = [float( templineslist[temp][3][0]+ templineslist[temp][4][0])/2,float( templineslist[temp][3][1]+ templineslist[temp][4][1])/2,float( templineslist[temp][3][2]+ templineslist[temp][4][2])/2]
                                    pointlist=pointlistmaker([poi[5],Midpoint])
                                    polytemp=None
                                    checkk=True
                                    temptwo = [n for n in templineslist if n != templineslist[temp]]
                                    for eeee in temptwo:
                                        if segmentlineintersection3d([eeee[3],eeee[4]],pointlist) != False:
                                            checkk=False
                else: #go to the middle of higher priority line
                    for i in mainpolylist:
                        if i[0]==firstbh and i[1]==secondbh:
                            templineslist=list()
                            for ii in i[2]:
                                if ii[0]>poi[3]:
                                    templineslist.append(ii)
                            templineslist=sorted(templineslist,key=itemgetter(0))
                            checkk=False
                            for temp in range(0,len(templineslist)):
                                if checkk==False:
                                    Midpoint = [float( templineslist[temp][3][0]+ templineslist[temp][4][0])/2,float( templineslist[temp][3][1]+ templineslist[temp][4][1])/2,float( templineslist[temp][3][2]+ templineslist[temp][4][2])/2]
                                    pointlist=pointlistmaker([poi[5],Midpoint])
                                    polytemp=None
                                    checkk=True
                                    temptwo = [n for n in templineslist if n != templineslist[temp]]
                                    for eeee in temptwo:
                                        if segmentlineintersection3d([eeee[3],eeee[4]],pointlist) != False:
                                            checkk=False
            ########################################################################
        #removing the old lines in case of intersection
        bh1temp=firstbh
        bh2temp=secondbh
        polylisttemp=list()
        for v in mainpolylist: #temporary polylist of the one with disjoint=False
            if v[0]==bh1temp and v[1]==bh2temp:
                for vv in v[2]:
                    inters=segmentlineintersection3d(pointlist,[vv[3],vv[4]])
                    if  inters!= False:
                        if side=="right":
                            dist=sqrt((inters[0]-pointlist[0][0])**2+(inters[1]-pointlist[0][1])**2+(inters[2]-pointlist[0][2])**2)
                        else:
                            dist=sqrt((inters[0]-pointlist[1][0])**2+(inters[1]-pointlist[1][1])**2+(inters[2]-pointlist[1][2])**2)
                        polylisttemp.append([vv,dist])
        newsitpoint2, mainpolylist, polytemp, pointlist=deleteexistedline.deleteexistedline_fun(pointlist,polytemp,polylisttemp,poi[3],mainpolylist,bh1temp,bh2temp,side)
        #####################################
        #append
        try: 
            for cou in mainpolylist:
                if cou[0]==firstbh and cou[1]==secondbh:
                    cou[2].append([ poi[3],poi[4] ,polytemp,pointlist[0],pointlist[1]])
        except:
            pass
        return newsitpoint2,licou2,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist    
    ###################################################################################
    licou=0
    licou2=0
    ################################################################
    #finding the top lithology in the borehole
    rawdatainpointbh=list()
    for r in rawdata:
        if r[0]==poi[1]:
            rawdatainpointbh.append(r)
    rawdatainpointbh = sorted(rawdatainpointbh,key=itemgetter(2),reverse=True)
    litTop=False
    for kk in range(0,len(rawdatainpointbh)-1):
        if  rawdatainpointbh[kk+1][2] <= poi[5][2] and  poi[5][2] <= rawdatainpointbh[kk][3]:
            licou=licou+1
            litTop=rawdatainpointbh[kk][4]
    newsitpoint1=list()
    newsitpoint2=list()
    ###############################################################################
    '''left:'''
    #the following line added to filter the first real borehole from doing the procedure again
    if poi[7] != "left_connected":
        newsitpoint1,licou,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist=bothsidesconnector(newsitpoint1,licou,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,'left',indextemplist_with_coords)
    ################################################################################    
    '''right:'''
    #the following line added to filter the last real borehole from doing the procedure again
    if poi[7]!= "right_connected":
       newsitpoint2,licou2,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist=bothsidesconnector(newsitpoint2,licou2,preferred_angle, poi, mainpolylist,alreadydonepolies,rawdata,angles,mainpointlist,'right',indextemplist_with_coords) 
    #integrating newsitpoint from left and right
    newsitpoint=newsitpoint1+newsitpoint2
    return alreadydonepolies,mainpolylist,poi,newsitpoint
   