from operator import itemgetter
def faultpointextraction(fault_table,boidtable,elev,x,y,mainpointlist,indextemplist_with_coords,point_id):
    #fault_table=[ [priority_number,  [ [bhid,elevation] , [bhid,elevation] , ...], optional angle, type]]


    for n in fault_table:
        '''change elev to z coords '''
        for itero in n[1]:
            try:
                nr = boidtable.index(itero[0])
                itero[1] = elev[nr] - itero[1]
                #print 111
                '''..................................'''
                '''mainpointlist=[0=point_id, 1=index, 2=bhid, 3=priority, 4=type, 5=coordinates,
                6=connectedleft point id, 7=connectedright point id, 8=pointcode ]
                pointcodes:
                0 = not connected
                1 = just left connected
                2 = just right connected
                3 = fully connected'''

                '''point id'''
                point_id=point_id+1
                #print 222
                '''index
                indextemplist_with_coords=[ 0=id, 1=index] '''
                for k in indextemplist_with_coords:
                    if itero[0]==k[0]:
                        ind=k[1]
                '''coordinates'''
                nrr=boidtable.index(itero[0])
                xtemp=x[nrr]
                ytemp=y[nrr]
                ztemp=itero[1]
                '''.......... '''
                mainpointlist.append([ point_id, ind, itero[0], n[0], n[3], [xtemp,ytemp,ztemp],0,0,0,"normal" ])
                point_id=point_id+1
                #to add faults in virtual BHs
                if ind==indextemplist_with_coords[1][1]:
                    mainpointlist.append([ point_id, indextemplist_with_coords[0][1], indextemplist_with_coords[0][0], n[0], n[3], [ x[boidtable.index(indextemplist_with_coords[0][0])] ,y[boidtable.index(indextemplist_with_coords[0][0])],ztemp],0,0,0,"normal" ])
                    point_id=point_id+1
                elif ind==indextemplist_with_coords[-2][1]:
                    mainpointlist.append([ point_id, indextemplist_with_coords[-1][1], indextemplist_with_coords[-1][0], n[0], n[3], [ x[boidtable.index(indextemplist_with_coords[-1][0])] ,y[boidtable.index(indextemplist_with_coords[-1][0])],ztemp],0,0,0,"normal" ])
                    point_id=point_id+1
            except:
                print "The point is in the fault table but not in specified borehole IDs"
    return mainpointlist
def pointextraction(rawdata,prior,indextemplist_with_coords,x,y,boidtable,fault_table,elev):
    rawdata.sort(key=itemgetter(2,3),reverse=True) #sort by top z
    rawdata.sort(key=itemgetter(0)) #sort by index
    #prior=[[0,[50],[54],['normal']],[1,[51],[50],'normal'],[2,[52],[51],'normal'],[3,[49],[],'discordancy'],[4,[],[],'fault'],[5,[53],[49],'normal'],[6,55,[],'discordancy']]
    mainpointlist=list()
    mainpointlistreverse=list()
    point_id=0
    #print 'rawdata2019', rawdata
    for i in range(0,len(rawdata)-1):

        for j in range(0,len(prior)):

            if rawdata[i][0]==rawdata[i+1][0]: #check to be in the same bh

                if  prior[j][3] != "intrusion":

                    countnormal=0
                    countreverse=0

                    if rawdata[i][4] in prior[j][1] and rawdata[i+1][4] in prior[j][2]:
                        countnormal=countnormal+1
                        point_id=point_id+1
                        '''coordinates'''
                        ztemp=(rawdata[i][3]+rawdata[i+1][2])/2
                        nr=boidtable.index(rawdata[i][1])
                        xtemp=x[nr]
                        ytemp=y[nr]
                        mainpointlist.append([point_id,rawdata[i][0],rawdata[i][1],
                        prior[j][0],prior[j][3],[xtemp, ytemp, ztemp],0,0,0,"normal"])
                        '''....................................'''
                    #This part of the code is for extracting the points with reverse polarity than normal
                    if rawdata[i][4] in prior[j][2] and rawdata[i+1][4] in prior[j][1]:
                        countreverse=countreverse+1
                        point_id=point_id+1
                        '''coordinates'''
                        ztemp=(rawdata[i][3]+rawdata[i+1][2])/2
                        nr=boidtable.index(rawdata[i][1])
                        xtemp=x[nr]
                        ytemp=y[nr]
                        mainpointlistreverse.append([point_id,rawdata[i][0],rawdata[i][1],
                        prior[j][0],prior[j][3],[xtemp, ytemp, ztemp],0,0,0,"reverse"])
                    ###########################################################
                elif prior[j][3] == "intrusion"  and rawdata[i][4] in prior[j][2]: #intrusion in the middle
                    point_id=point_id+1
                    nr=boidtable.index(rawdata[i][1])
                    xtemp=x[nr]
                    ytemp=y[nr]
                    mainpointlist.append([point_id,rawdata[i][0],rawdata[i][1],prior[j][0],prior[j][3],[xtemp, ytemp,rawdata[i][2]],0,0,0,"normal"])
                    if rawdata[i+1][4]!= "bottombox":
                        point_id=point_id+1
                        mainpointlist.append([point_id,rawdata[i][0],rawdata[i][1],prior[j][0],prior[j][3],[xtemp, ytemp,rawdata[i][3]],0,0,0,"normal"])
                if i==len(rawdata)-2 and prior[j][3] == "intrusion"  and rawdata[i+1][4] in prior[j][2]:
                    point_id=point_id+1
                    i=i+1
                    nr=boidtable.index(rawdata[i][1])
                    xtemp=x[nr]
                    ytemp=y[nr]
                    mainpointlist.append([point_id,rawdata[i][0],rawdata[i][1],
                    prior[j][0],prior[j][3],[xtemp, ytemp,rawdata[i][2]],0,0,0,"normal"])
                    if rawdata[i+1][4]!= "bottombox":
                        point_id=point_id+1
                        mainpointlist.append([point_id,rawdata[i][0],rawdata[i][1],
                        prior[j][0],prior[j][3],[xtemp, ytemp,rawdata[i][3]],0,0,0,"normal"])
    ###########################################################                    
    mainpointlist=faultpointextraction(fault_table,boidtable,elev,x,y,mainpointlist,indextemplist_with_coords,point_id)
    #print "mainpointlist2019", mainpointlist
    return mainpointlist,mainpointlistreverse,point_id