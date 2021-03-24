
from operator import itemgetter

def boundaryconditions(x1,x2,y1,y2,xbh1,xbh2,ybh1,ybh2,len_planenormallist,plns,epsbn_ratio_3d,eps_ratio_3d):
    #applying boundary conditions
    if plns != len_planenormallist-1 and plns!=0:
        if x1 >= xbh1-eps_ratio_3d and x1 <=xbh2+eps_ratio_3d:
            if ybh2 >= ybh1:
                if y1>=ybh1-eps_ratio_3d and y1<= ybh2+eps_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
            else:
                if y1>=ybh2-eps_ratio_3d and y1<= ybh1+eps_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
        else:
            if  x2 >= xbh1-eps_ratio_3d and x2 <=xbh2+eps_ratio_3d:
                if ybh2 >= ybh1:
                    if y2>=ybh1-eps_ratio_3d and y2<= ybh2+eps_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
                else:
                    if y2>=ybh2-eps_ratio_3d and y2<= ybh1+eps_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
            else:
                complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                complist=sorted(complist,key=itemgetter(1))
                if complist[0][0] in [1,2]:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
    elif plns==0 :
        if x1 >= xbh1-epsbn_ratio_3d and x1 <=xbh2+eps_ratio_3d:
            if ybh2 >= ybh1:
                if y1>= ybh1-epsbn_ratio_3d and y1 <= ybh2+eps_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
            else:
                if y1>=ybh2-eps_ratio_3d and y1<= ybh1+epsbn_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
        else:
            if  x2 >= xbh1-epsbn_ratio_3d and x2 <=xbh2+eps_ratio_3d:
                if ybh2 >= ybh1:
                    if y2>= ybh1-epsbn_ratio_3d and y2 <= ybh2+eps_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
                else:
                    if y2>=ybh2-eps_ratio_3d and y2<= ybh1+epsbn_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
            else:
                complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                complist=sorted(complist,key=itemgetter(1))
                if complist[0][0] in [1,2]:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
    else:
        if x1 >= xbh1-eps_ratio_3d and x1 <=xbh2+epsbn_ratio_3d:
            if ybh2 >= ybh1:
                if y1>= ybh1-eps_ratio_3d and y1 <= ybh2 + epsbn_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
            else:
                if y1>=ybh2-epsbn_ratio_3d and y1<= ybh1+eps_ratio_3d:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
        else:
            if  x2 >= xbh1-eps_ratio_3d and x2 <=xbh2+epsbn_ratio_3d:
                if ybh2 >= ybh1:
                    if y2>= ybh1-eps_ratio_3d and y2 <= ybh2 + epsbn_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
                else:
                    if y2>=ybh2-epsbn_ratio_3d and y2<= ybh1+eps_ratio_3d:
                        x=x2
                        y=y2
                    else:
                        complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                        complist=sorted(complist,key=itemgetter(1))
                        if complist[0][0] in [1,2]:
                            x=x1
                            y=y1
                        else:
                            x=x2
                            y=y2
            else:
                complist=[[1,abs(x1-xbh1)],[2,abs(x1-xbh2)],[3,abs(x2-xbh1)],[4,abs(x2-xbh2)]]
                complist=sorted(complist,key=itemgetter(1))
                if complist[0][0] in [1,2]:
                    x=x1
                    y=y1
                else:
                    x=x2
                    y=y2
    return x,y
