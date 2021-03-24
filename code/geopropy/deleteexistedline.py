from operator import itemgetter
from math import sqrt
from segmentlineintersection3d import segmentlineintersection3d
from connectleftandrightstage2_v2 import pointlistmaker

#This function recieves a polytemp with intersection as an input, correct the last new point to the nearest line with higher priority, and deletes the lines in between
def deleteexistedline_fun(pointlist,polytemp,polylisttemp,prior,mainpolylist,bh1temp,bh2temp,leftorright):
    if leftorright=="left":
        beginpoint=1
    elif leftorright=="right":
        beginpoint=0
    newsitpoint=list()
    polylisttemp=sorted(polylisttemp,key=itemgetter(1))
    thisvalue='boo'
    for u in polylisttemp:
        if thisvalue=='boo':
            if u[0][0]<prior:
                if u[0][1]=='bottombox':
                    #cut the new line
                    newpoint=segmentlineintersection3d(pointlist,[u[0][3],u[0][4]]) #main[2].intersect(polytemp,'point')
                    pointlist=pointlistmaker([pointlist[beginpoint],newpoint])
                    polytemp=None
                    thisvalue='notboo'
                else:
                    print "delete", bh1temp,bh2temp,u[0]
                    #print mainpolylist
                    #in bigger function, it old happeing, and the point is in pointlist,
                    #do the secondstagelinecompletor again rightaway
                    #delete the old line
                    for pp in range(0,len(mainpolylist)):
                        if mainpolylist[pp][0]== bh1temp and mainpolylist[pp][1] == bh2temp:
                            if u[0] in mainpolylist[pp][2]:
                                mainpolylist[pp][2][mainpolylist[pp][2].index(u[0])]=-11
                                newsitpoint.append([[mainpolylist[pp][0],mainpolylist[pp][1]],u[0][3],u[0][4]])
                                #newsitpoint=[ [ [index1,index2], startpoint,endpoint ] ,... ]
                            n2temp=list()
                            for p in mainpolylist[pp][2]:
                                if p != -11:
                                    n2temp.append(p)
                            mainpolylist[pp][2]=n2temp
                            #define a value for checking later (len newsitpoint)
            #cut the new line and thisvalue='notboo'
            elif u[0][0]>=prior:
                newpoint=segmentlineintersection3d(pointlist,[u[0][3],u[0][4]]) #main[2].intersect(polytemp,'point')
                pointlist=pointlistmaker([pointlist[beginpoint],newpoint])
                polytemp=None
                thisvalue='notboo'
            else:
                print 'polyline is the same as continuedlinecreator!! The line has intersection with another line with the same priority (deleteexistedline.py)'
            #Note that after completing this part, secondstagelinecompletor
            #have to change modify to: 1. if newsitpoints in pointlist, modify their situation
            #if situation changed, do the secondstagelinecompletor again
    return newsitpoint, mainpolylist, polytemp, pointlist
