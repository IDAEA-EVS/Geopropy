from operator import itemgetter

def bhlinecreator(bhindex,indextemplist_with_coords,rawdata):
    bhlinelist=list()
    bhidpoints=list()
    for n in indextemplist_with_coords:
        if n[1]==bhindex:
            xt=n[2]
            yt=n[3]
    for i in rawdata:
        if i[0]==bhindex:
            bhidpoints.append(i)
    bhidpoints=sorted(bhidpoints,key=itemgetter(2),reverse=True) #sort by topcoord
    for j in bhidpoints:
        points=[[xt,yt,j[2]],[xt,yt,j[3]]]
        if points[0] != points[1]:
            polytemp=None
            bhlinelist.append([points,polytemp,j[4]])
    return bhlinelist #bhlinelist=[ [polytemp,lit] , [polytemp,lit], .... ]
