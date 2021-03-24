
#pre - processing priority table
def preproc_prioritytable(prior):

    if prior[0][3]=='discordancy':
        print('The highest priority can not be unconformity (discordancy)(preproc_prioritytable.py)')
        quit()

    layerTempListForDisc=list()



    for j in range(0,len(prior)):
        layerTempListForDisc2=list()
        if str(prior[j][3]) != 'discordancy':

            for v in prior[j][1]: #for every layer in top layer list
                if v not in layerTempListForDisc:
                    layerTempListForDisc.append(v)

            for v in prior[j][2]:
                if v not in layerTempListForDisc:
                    layerTempListForDisc.append(v)

        elif str(prior[j][3])=='discordancy':
            if prior[j][1][0] not in layerTempListForDisc:
                layerTempListForDisc.append(prior[j][1][0])

            for n in layerTempListForDisc:
                if n != prior[j][1][0]:
                    layerTempListForDisc2.append(n)

            prior[j][2]=layerTempListForDisc2

    return prior

    '''format = [prior 0:prioroty 1:[toplayer] 2:[bottomlayer] 3:type]
    -sorted by reverse priority
    top layer and bottom layer type is list'''
