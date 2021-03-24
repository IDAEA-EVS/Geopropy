def layermerge(boid,top,bot,lit,indextemplist_with_coords,bore,Merge_Layers=False):

    if Merge_Layers=='True':
        newtop=list()
        newbot=list()
        newboid=list()
        newlit=list()
        toplist=list()

        for a in range(0,len(boid)):
            try:
                if boid[a] == boid[a+1]:

                    if lit[a] == lit[a+1]:

                        toplist.append(top[a])

                    else:

                        try:
                            newtop.append(min(toplist))

                        except:
                            newtop.append(top[a])

                        newbot.append(bot[a])
                        newboid.append(boid[a])
                        newlit.append(lit[a])
                        toplist=list()
                else:
                    try:
                        newtop.append(min(toplist))

                    except:
                        newtop.append(top[a])

                    newbot.append(bot[a])
                    newboid.append(boid[a])
                    newlit.append(lit[a])
                    toplist=list()
            except:
                print('layer merging finished')


        del toplist
        del top
        del bot
        del boid
        del lit
    else:
        newboid=boid
        newtop=top
        newbot=bot
        newlit=lit
    '''change the raw data structure  '''
    rawdata=list()
    for j in range(0,len(newbot)):

        rawdata.append([newboid[j],newtop[j],newbot[j],newlit[j]])

    tempvirt0=list()
    tempvirtn=list()
    #change rawdata format and add rawdata for virtual boreholes

    for yy in range(0,len(rawdata)):

        for xx in indextemplist_with_coords:

            if rawdata[yy][0]==xx[0]:

                rawdata[yy]=[xx[1],xx[0],rawdata[yy][1],rawdata[yy][2],rawdata[yy][3]]
                #indextemplist_with_coords=[ 0=id, 1=index]


        if rawdata[yy][1]==bore[0]:


            tempvirt0.append([1,-1,rawdata[yy][2],rawdata[yy][3],rawdata[yy][4]])

        elif rawdata[yy][1]==bore[len(bore)-1]:

            tempvirtn.append([len(bore),0,rawdata[yy][2],rawdata[yy][3],rawdata[yy][4]])

    rawdata = tempvirt0 + rawdata + tempvirtn
    return rawdata
