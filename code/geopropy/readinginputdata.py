#import arcpy
import preproc_prioritytable
from operator import itemgetter
import sys
import pypyodbc

def readBorehole_LithoTable(bore,boidtable,elev,Lithology_table,con_to_mdb):

    '''defining variables for Borehole_Litho table'''
    boid=list()
    top=list()
    bot=list()
    lit=list()
    fault_points_in_rawdata=list()
    '''the line below(borehole litho) is the main line, i changed it just because
     I wanted to use synthetic database that works with subunits'''
    #with arcpy.da.SearchCursor('Borehole_Litho', '*') as cursr:
    #2020 change from arcpy
    cursr = con_to_mdb.cursor()
    comnd='select BOREHOLE_ID, Top_Depth, Bottom_Depth, SubUnits from '+ Lithology_table
    cursr.execute(comnd)
    #with arcpy.da.SearchCursor(Lithology_table, ['OBJECTID','BOREHOLE_ID','Top_Depth','Bottom_Depth','SubUnits']) as cursr:
    for rw in cursr:
        if str(rw[0]) in bore:
            if None in filter(lambda x:x==None,rw):
                print "There is None (probably empty cells!) in Lithology_table in database, terminating!"
                sys.exit()

            boid.append(str(rw[0]))
            top.append(rw[1])
            bot.append(rw[2])
            lit.append(rw[3])

            if rw[3] in [63,'Fault','fault']:
                fault_points_in_rawdata.append([str(rw[0]),float(rw[1]+rw[2])/2])
    cursr.close() 
    #del cursr
    '''changing the data from top/bottom to coordinations(x,y,z)'''

    for iter in range(0,len(top)):
        nr = boidtable.index(boid[iter])
        top[iter] = elev[nr] - top[iter]
        bot[iter] = elev[nr]- bot[iter]

    for fpr in fault_points_in_rawdata:
        nr = boidtable.index(fpr[0])
        fpr[1]= elev[nr] - fpr[1]
    '''...........................................................'''
    return boid, top, bot, lit,fault_points_in_rawdata

    '''...........................................................'''

def readtopo_points(prior,indextemplist_with_coords,del_x,del_y,con_to_mdb):
    #make a primary list, reading the table
    temp_points=list()
    for i in prior:
        temp_points.append([   i[0], [] ])
    temp_points=temp_points+[["surface",[]]]
    # #2020 change to pypyodbc  
    cursr = con_to_mdb.cursor()
    comnd='select X, Y, Z,priority_num, Type, Polarity, Angle from Topo_points'
    cursr.execute(comnd)

    #with arcpy.da.SearchCursor(
    #'Topo_points',['X','Y','Z','priority_num','Type','Polarity',"Angle"]) as cursr:
    for rw in cursr:
        if None in filter(lambda x:x==None,rw[:3]):
            print "There is None (probably empty cell(s)!) in Topo_points table coordinaiton data in database, terminating!"
            sys.exit()
        for j in temp_points:
            if rw[3] == j[0] or j[0]=="surface":
                min_bh_ind_x=None
                max_bh_ind_x=None
                min_bh_ind_y=None
                max_bh_ind_y=None
                bp_list=list()
                for jj in indextemplist_with_coords: #range(0,len(indextemplist_with_coords)-1):
                    if jj[2]>rw[0]-del_x and (min_bh_ind_x==None or min_bh_ind_x>jj[1]-1):
                        min_bh_ind_x=jj[1]-1
                    if jj[2]>rw[0]+del_x and (max_bh_ind_x==None or max_bh_ind_x>jj[1]):
                        max_bh_ind_x=jj[1]    
                    if jj[3]>rw[1]-del_y and (min_bh_ind_y==None or min_bh_ind_y>jj[1]-1):
                        min_bh_ind_y=jj[1]-1
                    if jj[3]>rw[1]+del_y and (max_bh_ind_y==None or max_bh_ind_y>jj[1]):
                        max_bh_ind_y=jj[1]    

                    min_bh_ind=max(min_bh_ind_x,min_bh_ind_y)
                    max_bh_ind=min(max_bh_ind_x,max_bh_ind_y)
                        #bhind1=indextemplist_with_coords[jj][1]
                        #bhind2=indextemplist_with_coords[jj+1][1]
                if   min_bh_ind!= None and  max_bh_ind!=None: #if it is none, means that the surface points are out of range!     
                    for bp in range(min_bh_ind,max_bh_ind):
                        bp_list.append([bp,bp+1])

                    #topo_pnt_ind=( float(rw[0]-indextemplist_with_coords[jj][2]) / (indextemplist_with_coords[jj+1][2]-indextemplist_with_coords[jj][2]) )+ indextemplist_with_coords[jj][1]
                    j[1].append([bp_list,None,rw[0],rw[1],rw[2],rw[4],rw[5],rw[6],0,None])                            
    #del cursr
    cursr.close()
    temp_point=list()
    for j in temp_points:
        if len(j[1])!=0:
            temp_point.append(j)
    #########################################################
    return temp_point
def readBorehole_table(bore,xshifter,yshifter,indextemplist,con_to_mdb):
    'defining variables for Borehole_table and reading the table from .mdb file'
    boreholes=list()
    boidtable=list()
    x=list()
    y=list()
    elev=list()
    ##########################
    #2020_changing from arcpy to pypyodbc
    cursr = con_to_mdb.cursor()
    cursr.execute('select BOREHOLE_ID,X,Y,Elevation from Borehole_Table')
    #with arcpy.da.SearchCursor(
    #'Borehole_Table',['BOREHOLE_ID','X','Y','Elevation']) as cursr:
    for rw in cursr:
        if str(rw[0]) in bore:
            if None in filter(lambda x:x==None,rw):
                print "There is None (probably empty cell(s)!) in Borehole_Table table in database, terminating!"
                sys.exit()

            boreholes.append([str(rw[0]),rw[1],rw[2],rw[3]])
            #x.append(rw[1])
            #y.append(rw[2])
            #elev.append(rw[3])
    #del cursr
    cursr.close() 
    #sorting like the bore (user defined) list
    for br in bore:
        for boid in boreholes:
            if br == boid[0]:
                boidtable.append(boid[0])
                x.append(boid[1])
                y.append(boid[2])
                elev.append(boid[3])

    #check if there are equal Y's and equal consecutive X's, or not increasing X's, then do the action:
    for cnt in range(1,len(y)-2):
        if y[cnt]==y[cnt+1]:
            print 'Borehole Y coordination changed! 2 consecutive bh with the same Y coordination'
            y[cnt+1]=y[cnt+1]+xshifter
        if x[cnt+1] == x[cnt]:
            print 'Borehole X coordination changed! 2 consecutive bh with the same X coordination' 
            x[cnt+1]=x[cnt]+yshifter
        
        elif x[cnt+1] < x[cnt]:
            print 'X coordination of the boreholes have to increase!! Terminating'
            quit()
        else:
            pass
    
        

    '''adding virtual boreholes to x y elev boidtable'''
    ##################
    #Note: virtual boreholes in boidtable determine by -1 and 0 ids
    x1=x[boidtable.index(bore[1])]- abs(x[boidtable.index(bore[2])]-x[boidtable.index(bore[1])])
    y1=y[boidtable.index(bore[1])]- abs(y[boidtable.index(bore[2])]-y[boidtable.index(bore[1])])
    elev1=elev[boidtable.index(bore[1])]

    xn=x[boidtable.index(bore[-2])] + abs(x[boidtable.index(bore[-2])]-x[boidtable.index(bore[-3])])
    yn=y[boidtable.index(bore[-2])] + abs(y[boidtable.index(bore[-2])]-y[boidtable.index(bore[-3])])
    elevn=elev[boidtable.index(bore[-2])]
    x=[x1]+x+[xn]
    y=[y1]+y+[yn]
    elev=[elev1]+elev+[elevn]
    boidtable=[-1]+boidtable+[0]

    indextemplist_with_coords=list()
    ind_t=list()
    for i in indextemplist:
        for j in range(0,len(boidtable)):
            if boidtable[j]==i[0] and i[1] not in ind_t:
                ind_t.append(i[1])
                indextemplist_with_coords.append([i[0],i[1],x[j],y[j],elev[j]])
    return boidtable, x, y, elev,indextemplist_with_coords


    '''Read priority table (sort from new (high) to old)
    This table is a table that define priorities between two boreholes'''
def readpriority_table(con_to_mdb):
    prior=list()
    #2020 change from arcpy
    cursr = con_to_mdb.cursor()
    comnd='select Id, prority_number, top_layer, bottom_layer, type, preferred_angle from Borehole_ChronoPriority'
    cursr.execute(comnd)
    #with arcpy.da.SearchCursor('Borehole_ChronoPriority', ['Id','prority_number','top_layer','bottom_layer','type','preferred_angle']) as cursr:
    for rw in cursr:
        if str(rw[4]) in ['discordancy','unconformity','Discordancy','Unconformity']:
            if None in filter(lambda x:x==None,[rw[1],rw[2]]):
                print "There is None (probably empty cell(s)!) in Borehole_ChronoPriority table in database in 'prority_number'or 'top_layer' field for 'Discordancy' type, terminating!"
                sys.exit()
            prior.append([int(rw[1]),[int(rw[2])],[],"discordancy",rw[5]])

        elif str(rw[4]) in ['fault','Fault']:
            if None in filter(lambda x:x==None,[rw[1]]):
                print "There is None (probably empty cell(s)!) in Borehole_ChronoPriority table in database in 'prority_number' field for 'fault' type, terminating!"
                sys.exit()
            prior.append([int(rw[1]),[],[],"fault",rw[5]])

        elif str(rw[4]) in ['Intrusion','intrusion']:
            if None in filter(lambda x:x==None,[rw[1],rw[3]]):
                print "There is None (probably empty cell(s)!) in Borehole_ChronoPriority table in database in 'prority_number'or 'bottom_layer' field for 'Intrusion' type, terminating!"
                sys.exit()
            prior.append([int(rw[1]),[],[int(rw[3])],"intrusion",rw[5]])

        elif  str(rw[4]) not in ['fault','intrusion','discordancy', "Fault", "Intrusion", "unconformity","Unconformity","Discordancy"]:
            if str(rw[4]) not in ["Normal","normal"]: 
                print "type of unit contacts not defined correctly in Borehole_ChronoPriority table in database, terminating "
                sys.exit()
            else:
                if None in filter(lambda x:x==None,[rw[1],rw[2],rw[3]]):
                    print "There is None (probably empty cell(s)!) in Borehole_ChronoPriority table in database in 'prority_number','top_layer' or 'bottom_layer' field(s) for 'Normal' type, terminating!"
                    sys.exit()   
            prior.append([int(rw[1]),[int(rw[2])],[int(rw[3])],"normal",rw[5]])
    #del cursr
    cursr.close() 
    prior=sorted(prior,key=itemgetter(0))
    prior = preproc_prioritytable.preproc_prioritytable(prior)
    prior=sorted(prior,key=itemgetter(0),reverse=True)
    return prior
def readfault_table(prior,con_to_mdb):

    fault_table=list()

    '''fault_table=[ [priority_number,  [ [bhid,elevation] , [bhid,elevation] , ...], optional angle, type]
    , [priority_number,  [ [bhid,elevation] , [bhid,elevation] , ...], optional angle, type] , ...] '''
    for i in prior:
        if i[3] in ["fault","Fault"]:
            fault_table.append([i[0],[],0,0])
    #2020 change from arcpy
    cursr = con_to_mdb.cursor()
    comnd='select Priority_number, Borehole_ID, Elevation, Preferred_angle from fault_table'
    cursr.execute(comnd)        
    #with arcpy.da.SearchCursor('fault_table', ["Priority_number","Borehole_ID","Elevation","Preferred_angle"]) as cursr:
    for rw in cursr:
        for j in fault_table:
            if j[0]==rw[0]:
                if None in [rw[1],rw[2]]:
                    print "Borehole_ID and Elevation have to be specified in Fault_table"
                    sys.exit()
                j[1].append([rw[1],rw[2]])
                try:
                    j[2]=j[2]+float(rw[3])
                    j[3]=j[3]+1
                except:
                    pass  
    for i in fault_table:
        i[2]=float(i[2])/i[3]
        i[3]="fault"
    del cursr
    return fault_table
    #...........................................#

"""
def readfault_table():

    fault_table=list()

    '''fault_table=[ [priority_number,  [ [bhid,elevation] , [bhid,elevation] , ...], optional angle, type]
    , [priority_number,  [ [bhid,elevation] , [bhid,elevation] , ...], optional angle, type] , ...] '''

    with arcpy.da.SearchCursor('fault_table', '*') as cursr:
        for rw in cursr:

            cntr=0

            A=[float(x.strip()) for x in rw[1].split(',')]
            B=list()

            if len(A) % 2 != 0:
                print('Number of the inputs in the second coloumn of every row must be even, error in row:(readinginputdata.py)', rw[0] )
                quit()

            for a in range(0,len(A)):
                if a % 2 == 0:
                    B.append([A[a],A[a+1]])

            fault_table.append( [ rw[0] , B,rw[2],rw[3] ] )
    print "fault_table"                
    for i in fault_table:
        
        #i[2]=float(i[2])/i[3]
        #i[3]="fault"
        print i
    del cursr

return fault_table
    """