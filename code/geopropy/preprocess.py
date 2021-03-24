from os.path import expanduser
from os.path import join as joinadd
import shutil
#import arcpy
def delfiles():

        #delete old files if exist
        homeadd1 =joinadd(expanduser("~"),"arcgistemp")
        arcgistempdb=joinadd(homeadd1,"arcgistempdb.gdb")
        homeadd2 =joinadd(expanduser("~"),"arcgistemp_2d")
        arcgistempdb_2d=joinadd(homeadd2,"arcgistempdb_2d.gdb")
        polygon3dgdb=joinadd(homeadd2,"arcgistempdb_3d_polygons.gdb")
        try:
            shutil.rmtree(arcgistempdb,ignore_errors=True)
        except:
            pass
        '''try:
            arcpy.Delete_management (arcgistempdb)
        except:
            pass'''

        try:
            shutil.rmtree(arcgistempdb_2d,ignore_errors=True)
        except:
            pass
        '''try:
            arcpy.Delete_management (arcgistempdb_2d)
        except:
            pass'''

        try:
            shutil.rmtree(polygon3dgdb,ignore_errors=True)
        except:
            pass
        '''try:
            arcpy.Delete_management (polygon3dgdb)
        except:
            pass'''
        return

def preprocessing(boretemp):
    #delete files if exist
    delfiles()

    '''adding 2 virtual bhs to the first and the last of the borelist '''
    bore=list()
    bore.append(boretemp[0])
    bore.extend(boretemp)
    bore.append(boretemp[len(boretemp)-1])
    bore=[str(n) for n in bore]
    '''index creator '''
    t=0
    indextemplist=list()
    for h in bore:
        t=t+1
        indextemplist.append([h,t])
    indextemplist[0]=[-1,1]
    indextemplist[-1]=[0,t]

    '''making mainpolylist=[[index1,index2,[[priority_number , Type, poly1],[priority_number , Type, poly2]]],
    [bh2,bh3,[[priority_number , Type, poly1],[priority_number , Type, poly2]]]]'''
    mainpolylist=list()

    for z in range(0,len(indextemplist)-1):
        mainpolylist.append([indextemplist[z][1],indextemplist[z+1][1],[]])
    '''...........................................................'''

    return bore,indextemplist,mainpolylist