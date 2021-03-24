import math
from connectleftandrightstage2_v2 import pointlistmaker

def continuedLineCreator(pointz,ind1,ind2,ind3,prio_num,mainpolylist,LeftOrRight,bhid,indextemplist_with_coords,alreadydonepolies):
    #index1=leftbh index2=otherbh index3=the bh that we want the new line in between
    #print 'continuedLineCreator function used'
    for n in mainpolylist:
        if n[0]==ind1 and n[1]==ind2:
            for t in n[2]:

                if (t[0]==prio_num and pointz==t[4][2] and LeftOrRight=="right") or (t[0]==prio_num and pointz==t[3][2] and LeftOrRight=="left") :
                    if [ind1, ind2, t,LeftOrRight,pointz] not in alreadydonepolies and LeftOrRight=='right'  :
                        alreadydonepolies.append([ind1, ind2, t,LeftOrRight,pointz])
                        #parallel to the next bh coordination
                        for gg in indextemplist_with_coords:
                            if gg[1] == ind3:
                                xt = gg[2]
                                yt = gg[3]
                        #t[3]=startpoint
                        #t[4]=endpoint
                        len3=math.sqrt(math.pow(t[4][0]-t[3][0],2)+math.pow(t[4][1]-t[3][1],2)+math.pow(t[4][2]-t[3][2],2))
                        sinalpha=float(abs(t[4][2]-t[3][2]))/(len3)
                        cosalpha=math.sqrt(1-math.pow(sinalpha,2))
                        tanalpha=sinalpha/cosalpha
                        distparallel = math.sqrt( math.pow((t[4][0]-xt),2)   + math.pow((t[4][1]-yt),2) )
                        difelev = tanalpha * distparallel
                        if t[3][2] < t[4][2]:
                            zt = t[4][2] + difelev
                        else:
                            zt = t[4][2] - difelev
                        pointlist=pointlistmaker([t[4],[xt,yt,zt]])
                        polytemp=None
                    elif [ind1, ind2, t,LeftOrRight,pointz] not in alreadydonepolies and LeftOrRight=='left':
                        alreadydonepolies.append([ind1, ind2, t,LeftOrRight,pointz])
                        #parallel to the next bh coordination
                        for gg in indextemplist_with_coords:
                            if gg[1] == ind3:
                                xt = gg[2]
                                yt = gg[3]
                        #t[3]=endpoint
                        #t[4]=startpoint
                        len3=math.sqrt(math.pow(t[4][0]-t[3][0],2)+math.pow(t[4][1]-t[3][1],2)+math.pow(t[4][2]-t[3][2],2))
                        sinalpha=float(abs(t[4][2]-t[3][2]))/(len3)
                        cosalpha=math.sqrt(1-math.pow(sinalpha,2))
                        tanalpha=sinalpha/cosalpha
                        distparallel = math.sqrt( math.pow((t[3][0]-xt),2)   + math.pow((t[3][1]-yt),2))
                        difelev = tanalpha * distparallel
                        if t[4][2] < t[3][2]:
                            zt = t[3][2] + difelev
                        else:
                            zt = t[3][2] - difelev
                        pointlist=pointlistmaker([[xt,yt,zt],t[3]])
                        polytemp=None
    return polytemp, pointlist, alreadydonepolies