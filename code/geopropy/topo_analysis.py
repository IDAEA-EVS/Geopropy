from readinginputdata import readtopo_points
from operator import itemgetter
from math import pow,sqrt,tan, radians
from segmentlineintersection3d import segmentlineintersection3d
import copy

#the main surface points function
def surface_pnt_process(mainpointlist,mainpointlistreverse,mainpolylist,prior,rawdata,temp_points,indextemplist_with_coords):
    maintopolist=topo_pre_process(prior,indextemplist_with_coords,mainpointlist,mainpolylist,mainpointlistreverse,rawdata,temp_points)
    for prio in maintopolist:
        if prio[1]==True: #if topo point exists in this priority
            for boreholepair in prio[2]:
                if boreholepair[6][0] in ["no_topo_point","manual_topo_point"]:
                    pass
                elif boreholepair[6][0] in ["auto_topo_pair_complete", "exception_topo_algh"]:
                    for bhs_poly in mainpolylist:
                        if bhs_poly[0]==boreholepair[6][1][0] and bhs_poly[1]==boreholepair[6][1][1]:
                            for point_pairs in boreholepair[6][1][2]:
                                intersect_=False
                                for polyline in bhs_poly[2]:
                                    if polyline[0]>point_pairs[0]: #priority check
                                        intersect_=segmentlineintersection3d(polyline[3:],point_pairs[3:])
                                if intersect_==False: #append new automatic topo lines in case there is no intersection with the lines with higher priority
                                    for find_prio in prior:
                                        if find_prio[0]==point_pairs[0]:
                                            bhs_poly[2].append(
                                                [
                                                point_pairs[0],
                                                find_prio[3],
                                                None,
                                                point_pairs[3],
                                                point_pairs[4]
                                                ]
                                            )
                                    #change point sits        
                                    if point_pairs[1]=="topo_points_line_to_bh_left":
                                        for pnt_chng_sit in mainpointlist+mainpointlistreverse:
                                            if pnt_chng_sit[0]==boreholepair[6][2][0]:
                                                if pnt_chng_sit[8]==0:
                                                    pnt_chng_sit[8]=2
                                                elif pnt_chng_sit[8]==1:
                                                    pnt_chng_sit[8]=3
                                    elif point_pairs[1]=="topo_points_line_to_bh_right":                                
                                        for pnt_chng_sit in mainpointlist+mainpointlistreverse:
                                            if pnt_chng_sit[0]==boreholepair[6][2][1]:
                                                if pnt_chng_sit[8]==0:
                                                    pnt_chng_sit[8]=1
                                                elif pnt_chng_sit[8]==2:
                                                    pnt_chng_sit[8]=3
                                    
                                else:
                                    print "topoanalysis.py_func surface_pnt_process:\n automatic topo line not appended since there was an intersection!!"
                else:
                    raise Exception("!!!!!!!! THERE ARE SURFACE POINTS BETWEEN 2 BOREHOLES, BUT THE TYPE OF PROCESS IS NOT DEFINED BY THE PROGRAM!!!!!!!!!!!!!!!" )
    return mainpointlist,mainpointlistreverse,mainpolylist,maintopolist
####################################################################################
#pre processing stage: this function is used in surface_pnt_process    
def topo_pre_process(prior,indextemplist_with_coords,mainpointlist,mainpolylist,mainpointlistreverse,rawdata,temp_points):
    """
    This function uses the output of readtopo_points function, and generates maintopolist which will be use to analyze the surface points.
    function topo_pair_new_point used internally in this function

    maintopolist=[
        [0:priority_number,
        1: Is there a topo point in this priority number (True or False),
        2:[
            [
                0:BHindex1,
                1:BHindex2,
                2:num. of points in bhs,
                3:num. of points in surface between 2 bhs,
                4:[ #surface points
                    [
                        topo_pnt_ind,
                        'X',
                        'Y',
                        'Z',
                        'Type',
                        'polarity',
                        'Angle',
                        pointsit (0 for now),
                        reserved=None
                    ],[...],...
                ],

                5:[ #points in borehole
                    [highestbh1pnt=None, or:
                        bhind, 
                        X, 
                        Y, 
                        Z, 
                        "highestbh1pnt"
                        ,polarity
                        ,0
                        ,reserved=None,
                        mainpointlistid 
                    ],
                    [highestbh2pnt=None, or:
                        bhind, 
                        X, 
                        Y, 
                        Z, 
                        "highestbh2pnt"
                        ,polarity
                        ,0
                        ,reserved=None,
                        mainpointlistid 

                    ]
                ],
                6:[ #type of pocess between each two pair of point plus the info needed for analyzing in the next stage
                    0:string:{"manual_topo_point","no_topo_point","auto_topo_pair_complete","exception_topo_algh"},
                    1:[
                        0:bh ind,
                        1:bh ind+1,
                        2:[
                            [ #This almost has the same structure as mainpolylist
                                0:priority_number,
                                1:"topo_points_line",
                                2:None,
                                3:[left point coordination],
                                4:[right point coordination]
                            ],[...],...
                        ]
                    ],
                    2:[
                        pointid in bhind 1 or None,
                        pointid in bhind 2 or None,
                    ]
                ]
                7:reserved=None
            ],[...],...
        ]
    ]

    """
    ###################################################
    #prepare the main list of topography
    #temp_points= [ [ prior_num, [ [bhind1,bhind2,topo_pnt_ind,'X','Y','Z',     'Type','polarity','Angle',0, reserved=None],... ]  ],...   ]
    #                              [bhind1,bhind2,topo_pnt_ind,rw[0],rw[1],rw[2],rw[4], rw[5],    rw[6]  ,0, None]
    maintopolist=list()
    for each_prio in temp_points: #in every priority:
        if len(each_prio[1])==0:
            istopopnt=False
        else:
            istopopnt=True
        each_prio_temp=list()
        bhindexes=list()
        ############################################################
        for pairbhs in each_prio[1]: #between every 2 borehole:
            if [pairbhs[0],pairbhs[1]] not in bhindexes:
                bhindexes.append([pairbhs[0],pairbhs[1]])
                #find if there is points in bhs and the coordination of the closest ones
                highestbh1pnt=None
                highestbh2pnt=None
                for pnts in mainpointlist+mainpointlistreverse: 
                    if pnts[3]==each_prio[0]: #priority
                        if pnts[1]==pairbhs[0]: #point borehole index
                            if highestbh1pnt==None or highestbh1pnt[3]<pnts[5][2]:
                                highestbh1pnt=[pnts[1],pnts[5][0],pnts[5][1],pnts[5][2],"highestbh1pnt",pnts[9],0,None,pnts[0]] #same format as topo points in each prio temp
                                #highestbh1pnt=[bhind, X, Y, Z, "highestbh1pnt",polarity,0,reserved=None, mainpointlistid ]
                        elif pnts[1]==pairbhs[1]: #point borehole index
                            if highestbh2pnt==None or highestbh2pnt[3]<pnts[5][2]:
                                highestbh2pnt=[pnts[1],pnts[5][0],pnts[5][1],pnts[5][2],"highestbh2pnt",pnts[9],0,None,pnts[0]] #same format as topo points in each prio temp

                #calculate the number of boreholes containing points with the same priority
                bh_num=0
                if highestbh1pnt!= None:
                    bh_num=bh_num+1
                if highestbh2pnt!= None:
                    bh_num=bh_num+1


                #append
                each_prio_temp.append( [ pairbhs[0],pairbhs[1],1,bh_num,[ pairbhs[2:]  ],[highestbh1pnt,highestbh2pnt],None,None ])
                #pairbhs[2:]=topo_pnt_ind,'X','Y','Z',     'Type','polarity','Angle',0, reserved=None
            else:
                for tt in each_prio_temp:
                    if tt[0]==pairbhs[0] and tt[1]==pairbhs[1]:
                        tt[2]=tt[2]+1
                        tt[4].append(pairbhs[2:])
        ############################################################
        #topopoints=bhpairs[4]=topo_pnt_ind,'X','Y','Z','Type',polarity,angle,0,reserved=None
        #highestbh1pnt=pnts[0]
        #decide the procedure
        topo_process_type=None
        for bhpairs in each_prio_temp: #between every two borehole:
            bhpairs[4]=sorted(bhpairs[4],key=itemgetter(0))
            topopoints=copy.deepcopy(bhpairs[4])
            #topopoints=topo_pnt_ind,'X','Y','Z',     'Type','polarity','Angle',0, reserved=None
            #########################
            if istopopnt==False: #there is no topo point
                topo_pre_process=["no_topo_point" , [] ,[]]
            #########################
            elif bhpairs[3]==2 and bhpairs[2]==1: #if there is exception
                

                '''#complete pair list (ready for mainpolylist)
                topo_pre_process=[
                    "exception_topo_algh" , #0
                    
                    [ #1
                        bhpairs[5][0][0], #bh index
                        bhpairs[5][1][0], #bh index
                        [
                            [each_prio[0], "topo_points_line_to_bh_left", None, bhpairs[5][0][1:4], topopoints[0][1:4]  ],
                            [each_prio[0], "topo_points_line_to_bh_right", None, topopoints[0][1:4], bhpairs[5][1][1:4]  ]
                        ],
                    ],
   
                    [ #2
                    bhpairs[5][0][-1], #left point id in mainpointlist
                    bhpairs[5][1][-1] ##right point id in mainpointlist
                    ]
                ]'''

                topo_pre_process=["manual_topo_point", [],[] ]
            #########################
            elif bhpairs[3]==0 or (bhpairs[3]==2 and bhpairs[2]%2==1): #if no bh point or (2 bhpoint and odd number of topo points)
                topo_pre_process=["manual_topo_point", [],[] ]
            #########################
            elif (bhpairs[3]-bhpairs[2])%2==0: #if the bhpnt-topopnt=even (zoj)
                #complete pair list
                pairl=list()
                pnttlist=[None,None]
                #########################
                #polarity test
                Automatic_proc=True
                #bhpairs[5][0]=highestbh1pnt=[bhind, X, Y, Z, "highestbh1pnt",polarity,0,reserved=None, mainpointlistid ]
                #############
                leftpnts=[]
                rightpnts=[]
                #if bhpairs[5][0] !=None and topopoints[0][5]==bhpairs[5][0][5]: #left bh point exists and the polarity is the same with the first point
                if bhpairs[5][0] !=None: 
                    leftpnts=[bhpairs[5][0][:-1],topopoints[0]]
                    topopoints=topopoints[1:]
                    pnttlist[0]=bhpairs[5][0][-1]
                    #checking if the polarity is changed
                    '''if leftpnts[1][5]==topopoints[0][5]:
                        Automatic_proc=False'''
                '''else:
                    Automatic_proc=False'''
                #############
                #if bhpairs[5][1] !=None and topopoints[-1][5]==bhpairs[5][1][5] and Automatic_proc==True: #right bh point exists and the polarity is the same with the first point
                if bhpairs[5][1] !=None and Automatic_proc==True:
                    rightpnts= [topopoints[-1],bhpairs[5][1][:-1]]
                    topopoints=topopoints[:-1]
                    pnttlist[1]=bhpairs[5][1][-1]
                    #checking if the polarity is changed
                    '''if rightpnts[0][5]==topopoints[-1][5]:
                        Automatic_proc=False'''
                '''else:
                    Automatic_proc=False'''
                #############
                '''if Automatic_proc==True: #check for the correct polarity sequence in topo points  
                    for p in range(0,len(topopoints)/2): 
                        if topopoints[p*2][5]==topopoints[p*2+1][5]:
                            Automatic_proc=False'''
                #########################
                if Automatic_proc==True:

                    if len(leftpnts)!=0:
                        pairl.append(
                                [ each_prio[0], "topo_points_line_to_bh_left", None,leftpnts[0][1:4],leftpnts[1][1:4]]
                            )
                    ##################
                    #topo_pair_new_point function

                    pairl,Automatic_proc=topo_pair_new_point(topopoints,pairl,each_prio[0],Automatic_proc,rawdata,prior,indextemplist_with_coords)
                    ##################
                    if Automatic_proc ==False:
                        topo_pre_process=["manual_topo_point", [],[] ]
                    else:
                        if len(rightpnts) != 0:
                            pairl.append(
                                    [ each_prio[0], "topo_points_line_to_bh_right", None,rightpnts[0][1:4],rightpnts[1][1:4]]
                                )

                        pairlist=[ bhpairs[0] ,bhpairs[1]  , pairl]

                        topo_pre_process=["auto_topo_pair_complete",pairlist,pnttlist]
                else: #Automatic_proc==false , manual

                    topo_pre_process=["manual_topo_point", [],[] ]


            #########################
            else: #manual
                topo_pre_process=["manual_topo_point", [],[] ]
            bhpairs[6]=topo_pre_process
            #########################

        #append all to maintopolist
        maintopolist.append([each_prio[0],istopopnt,each_prio_temp])
        

    #topo_pre_process=["manual_topo_point",     [],         [] ]
    #                 ["no_topo_point",         [],         [] ]
    #                 ["auto_topo_pair_complete",pairlist,  pnttlist]
    #                 ["exception_topo_algh"    ,pairlist,  pnttlist]

    return maintopolist
####################################################################################
#to analyze and prepare automatic connecting of two pair of points in surface analysis
def topo_pair_new_point(topopoints,pairl,prio,Automatic_proc,rawdata,prior,indextemplist_with_coords):
    #topopoints=bhpairs[4]=topo_pnt_ind,'X','Y','Z','Type',polarity,angle,0,reserved=None

    for p in range(0,len(topopoints)/2):
        #dist ab (topo points)
        dist_=sqrt(
            pow(topopoints[2*p][1]-topopoints[2*p+1][1],2)+pow(topopoints[2*p][2]-topopoints[2*p+1][2],2)+pow(topopoints[2*p][3]-topopoints[2*p+1][3],2)
        )
        ######################################################

        
        ######################################################    
        if (None  not in [topopoints[2*p][6],topopoints[2*p+1][6]]) : #we have angles
            #delta_z_left_point
            new_z_left=topopoints[2*p+1][3]-(tan(radians(topopoints[2*p][6]))*dist_) #new_z_left=zright-tan*dist
            left_line=[
                topopoints[2*p][1:4] ,
                topopoints[2*p+1][1:3]+[new_z_left]
            ]
            #delta_z_right_point
            new_z_right=topopoints[2*p][3]+(tan(radians(abs(topopoints[2*p+1][6])))*dist_) #new_z_left=zright-tan*dist
            right_line=[
                topopoints[2*p][1:3]+[new_z_right],
                topopoints[2*p+1][1:4]
            ]
            #if intersection is false:
            inters=segmentlineintersection3d(left_line,right_line)

            if inters==False:
                Automatic_proc=False

            else: #we have new point!! append 2 lines

                #v shape lines (2 lines)

                pairl.append(
                    [ prio, "topo_points_line", None,
                    topopoints[2*p][1:4],
                    inters
                    ]
                
                )

                pairl.append(
                    [ prio, "topo_points_line", None,
                    inters,
                    topopoints[2*p+1][1:4]
                    ]
                
                )

        if None in [topopoints[2*p][6],topopoints[2*p+1][6]] or Automatic_proc==False : #if one is none (no angle data) or no intersection
            #or topopoints[2*p][6]<0 or topopoints[2*p+1][6]>0 
            #finding layers
            for pr in prior:
                if pr[0]==prio:
                    top_layers=pr[1]
                    bot_layers=pr[2]
            ###################
            #find average from raw data
            cntr=0
            for samples in rawdata:
                if (samples[0] in [int(topopoints[2*p][0]),int(topopoints[2*p][0])+1] ) and (samples[4] in top_layers or samples[4] in bot_layers):
                    cntr=cntr+1
                    len_val=abs(samples[3]-samples[2])
            len_val=float(len_val)/cntr
            ###################
            for bh in indextemplist_with_coords:
                if bh[1]==int(topopoints[2*p][0]):
                    leftbh=bh[2:]
                elif bh[1]==int(topopoints[2*p][0])+1:    
                    rightbh=bh[2:]
            #dist boreholes
            dist_bhs=sqrt(
                pow(leftbh[0]-rightbh[0],2)+pow(leftbh[1]-rightbh[1],2)+pow(leftbh[2]-rightbh[2],2)
            )
            #calculate the new Z:
            new_z_middle=float(topopoints[2*p][3]+topopoints[2*p+1][3])/2-( (float(dist_)/dist_bhs)* len_val  )
            new_x_middle=float(topopoints[2*p][1]+topopoints[2*p+1][1])/2
            new_y_middle=float(topopoints[2*p][2]+topopoints[2*p+1][2])/2
            Automatic_proc=True
            pairl.append(
                    [ prio, "topo_points_line", None,
                    topopoints[2*p][1:4],
                    [new_x_middle,new_y_middle,new_z_middle]
                    ]
                
                )

            pairl.append(
                [ prio, "topo_points_line", None,
                [new_x_middle,new_y_middle,new_z_middle],
                topopoints[2*p+1][1:4]
                ]
            
            )
    return pairl,Automatic_proc
####################################################################################