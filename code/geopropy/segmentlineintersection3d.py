
from math import sqrt
################################################################################
class Point:
    def __init__(self, px,py,pz):

        self.x = px
        self.y=py
        self.z=pz

        #self=(px,py,pz)

    def dist(self, other):
        #print "other.x, other.y, other.z, self.x, self.y, self.z", other.x, other.y, other.z, self.x, self.y, self.z
        #print "(self.x-other.x)**2",(self.x-other.x)**2,(self.y-other.y)**2,(self.z-other.z)**2
        #print sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)
        return sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)

    def __add__(self, other):
        return Point(self.x+other.x,self.y+other.y,self.z+other.z)

    def __sub__(self, other):
        return Point(self.x-other.x,self.y-other.y,self.z-other.z)
######################
def cross_product(p1, p2):
    return Point(p1.y*p2.z - p1.z*p2.y, p1.z*p2.x - p1.x*p2.z, p1.x*p2.y - p1.y*p2.x)

def dot_product(p1, p2):
    return (p1.x*p2.x + p1.y*p2.y + p1.z*p2.z)

def mag(p):
    return sqrt(p.x**2 + p.y**2 + p.z**2)

def normalise(p1, p2):
    p=p2-p1
    #p = tuple(numpy.subtract(p2, p1))
    m = mag(p)
    if m == 0:
        return Point(0.0, 0.0, 0.0)
    else:
        return Point(p.x/m, p.y/m, p.z/m)

def ptFactor(p, f):
    return Point(p.x*f, p.y*f, p.z*f)

########################

def segmentlineintersection3d(polyline1,polyline2):
    #test:
    #polyline1=arcpy.Polyline(arcpy.Array([arcpy.Point(1,0,1),arcpy.Point(10,0,10)]),"Unknown",True,False)
    #polyline2=arcpy.Polyline(arcpy.Array([arcpy.Point(1,1,2),arcpy.Point(1,1,3)]),"Unknown",True,False)

    '''
    p1xx=polyline1.firstPoint.X
    p1yy=polyline1.firstPoint.Y
    p1zz=polyline1.firstPoint.Z
    p2xx=polyline1.lastPoint.X
    p2yy=polyline1.lastPoint.Y
    p2zz=polyline1.lastPoint.Z
    p3xx=polyline2.firstPoint.X
    p3yy=polyline2.firstPoint.Y
    p3zz=polyline2.firstPoint.Z
    p4xx=polyline2.lastPoint.X
    p4yy=polyline2.lastPoint.Y
    p4zz=polyline2.lastPoint.Z

    p1=Point(p1xx, p1yy, p1zz)
    p2=Point(p2xx, p2yy, p2zz)
    p3=Point(p3xx, p3yy, p3zz)
    p4=Point(p4xx, p4yy, p4zz)'''

    p1=Point(polyline1[0][0], polyline1[0][1], polyline1[0][2])
    p2=Point(polyline1[1][0], polyline1[1][1], polyline1[1][2])
    p3=Point(polyline2[0][0], polyline2[0][1], polyline2[0][2])
    p4=Point(polyline2[1][0], polyline2[1][1], polyline2[1][2])

    """
    Reference 'The Shortest Line Between Two Lines in 3D' - Paul Bourke
    """

    A=p1-p3
    B=p2-p1
    C=p4-p3

    # Line p1p2 and p3p4 unit vectors
    uv1 = normalise(p1, p2)
    uv2 = normalise(p3, p4)

    # Check for parallel lines
    cp12 = cross_product(uv1, uv2)
    _cp12_ = mag(cp12)
    #print ' _cp12_ = mag(cp12)', round(_cp12_, 5)
    #if round(_cp12_, 6) != 0.0:
    if round(_cp12_, 6) != 0.0:

        ma = ((dot_product(A, C)*dot_product(C, B)) - (dot_product(A, B)*dot_product(C, C)))/  ((dot_product(B, B)*dot_product(C, C)) - (dot_product(C, B)*dot_product(C, B)))
        mb = (ma*dot_product(C, B) + dot_product(A, C))/ dot_product(C, C)
        #print "ma,mb", ma, mb
        # Calculate the point on line 1 that is the closest point to line 2
        Pa = p1 + ptFactor(B, ma)
        #print "Pa",Pa.x, Pa.y, Pa.z

        # Calculate the point on line 2 that is the closest point to line 1
        Pb = p3 + ptFactor(C, mb)
        #print "Pb",Pb.x, Pb.y,  Pb.z

        # Distance between lines
        dista = Pa.dist(Pb)
        #print "distance of the LINES is:" , dista
        #print 'round(p1.dist(p2),2) == round(p1.dist(Pa)+p2.dist(Pa),2) and round(p3.dist(p4),2) == round(p3.dist(Pa)+p4.dist(Pa),2)'
        #print '[p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],[p3.x,p3.y,p3.z] , [p4.x,p4.y,p4.z]',[p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],[p3.x,p3.y,p3.z] , [p4.x,p4.y,p4.z]
        #print round(p1.dist(p2),2), round(p1.dist(Pa)+p2.dist(Pa),2) , round(p3.dist(p4),2) ,round(p3.dist(Pa)+p4.dist(Pa),2)
        if round(dista, 3) != 0.0:
            #print 'round(dista, 3) != 0.0, no intersection'
            intersection=False

        elif [p2.x,p2.y,p2.z]==[p3.x,p3.y,p3.z]:
            #intersection=[p2.x,p2.y,p2.z]
            intersection=False
        elif [p1.x,p1.y,p1.z]==[p3.x,p3.y,p3.z]:
            #intersection=[p1.x,p1.y,p1.z]
            intersection=False
        elif [p2.x,p2.y,p2.z]==[p4.x,p4.y,p4.z]:
            #intersection=[p2.x,p2.y,p2.z]
            intersection=False
        elif [p1.x,p1.y,p1.z]==[p4.x,p4.y,p4.z]:
            #intersection=[p1.x,p1.y,p1.z]
            intersection=False

        elif round(p1.dist(p2),2) == round(p1.dist(Pa)+p2.dist(Pa),2) and round(p3.dist(p4),2) == round(p3.dist(Pa)+p4.dist(Pa),2):
            #print 'round(p1.dist(p2),2) == round(p1.dist(Pa)+p2.dist(Pa),2) and round(p3.dist(p4),2) == round(p3.dist(Pa)+p4.dist(Pa),2)'
            #print round(p1.dist(p2),2), round(p1.dist(Pa)+p2.dist(Pa),2) , round(p3.dist(p4),2) ,round(p3.dist(Pa)+p4.dist(Pa),2)
            intersection= [Pa.x,Pa.y,Pa.z]

        else:
            #print 'else:'
            intersection=False

    # Lines are parallel
    elif [p2.x,p2.y,p2.z]==[p3.x,p3.y,p3.z] and [p1.x,p1.y,p1.z]==[p4.x,p4.y,p4.z]:
        #print '2 lines are the same!! intersection set to false'
        intersection=False
    elif [p2.x,p2.y,p2.z]==[p4.x,p4.y,p4.z] and [p1.x,p1.y,p1.z]==[p3.x,p3.y,p3.z]:
        #print '2 lines are the same!! intersection set to false'
        intersection=False


    #elif [p2.x,p2.y,p2.z]==[p3.x,p3.y,p3.z]:
    #    intersection=[p2.x,p2.y,p2.z]
    #elif [p1.x,p1.y,p1.z]==[p3.x,p3.y,p3.z]:
    #    intersection=[p1.x,p1.y,p1.z]
    #elif [p2.x,p2.y,p2.z]==[p4.x,p4.y,p4.z]:
    #    intersection=[p2.x,p2.y,p2.z]
    #elif [p1.x,p1.y,p1.z]==[p4.x,p4.y,p4.z]:
    #    intersection=[p1.x,p1.y,p1.z]

    else:

        #print 'else parallel'
        intersection = False

    #print "INTERSECTION IS:", intersection
    return intersection

########################
def intersection3dtouch(polyline1,polyline2):
    #test:
    #polyline1=arcpy.Polyline(arcpy.Array([arcpy.Point(1,0,1),arcpy.Point(10,0,10)]),"Unknown",True,False)
    #polyline2=arcpy.Polyline(arcpy.Array([arcpy.Point(1,1,2),arcpy.Point(1,1,3)]),"Unknown",True,False)
    '''
    p1xx=polyline1.firstPoint.X
    p1yy=polyline1.firstPoint.Y
    p1zz=polyline1.firstPoint.Z
    p2xx=polyline1.lastPoint.X
    p2yy=polyline1.lastPoint.Y
    p2zz=polyline1.lastPoint.Z
    p3xx=polyline2.firstPoint.X
    p3yy=polyline2.firstPoint.Y
    p3zz=polyline2.firstPoint.Z
    p4xx=polyline2.lastPoint.X
    p4yy=polyline2.lastPoint.Y
    p4zz=polyline2.lastPoint.Z

    p1=Point(p1xx, p1yy, p1zz)
    p2=Point(p2xx, p2yy, p2zz)
    p3=Point(p3xx, p3yy, p3zz)
    p4=Point(p4xx, p4yy, p4zz)'''

    p1=Point(polyline1[0][0], polyline1[0][1], polyline1[0][2])
    p2=Point(polyline1[1][0], polyline1[1][1], polyline1[1][2])
    p3=Point(polyline2[0][0], polyline2[0][1], polyline2[0][2])
    p4=Point(polyline2[1][0], polyline2[1][1], polyline2[1][2])


    """
    Reference 'The Shortest Line Between Two Lines in 3D' - Paul Bourke
    """

    A=p1-p3
    B=p2-p1
    C=p4-p3

    # Line p1p2 and p3p4 unit vectors
    uv1 = normalise(p1, p2)
    uv2 = normalise(p3, p4)

    # Check for parallel lines
    cp12 = cross_product(uv1, uv2)
    _cp12_ = mag(cp12)
    #print ' _cp12_ = mag(cp12)', round(_cp12_, 5)
    #if round(_cp12_, 6) != 0.0:
    if round(_cp12_, 6) != 0.0:

        ma = ((dot_product(A, C)*dot_product(C, B)) - (dot_product(A, B)*dot_product(C, C)))/  ((dot_product(B, B)*dot_product(C, C)) - (dot_product(C, B)*dot_product(C, B)))
        mb = (ma*dot_product(C, B) + dot_product(A, C))/ dot_product(C, C)
        #print "ma,mb", ma, mb
        # Calculate the point on line 1 that is the closest point to line 2
        Pa = p1 + ptFactor(B, ma)
        #print "Pa",Pa.x, Pa.y, Pa.z

        # Calculate the point on line 2 that is the closest point to line 1
        Pb = p3 + ptFactor(C, mb)
        #print "Pb",Pb.x, Pb.y,  Pb.z

        # Distance between lines
        #print "distance of the LINES is:" , dista
        #print 'round(p1.dist(p2),2) == round(p1.dist(Pa)+p2.dist(Pa),2) and round(p3.dist(p4),2) == round(p3.dist(Pa)+p4.dist(Pa),2)'
        #print '[p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],[p3.x,p3.y,p3.z] , [p4.x,p4.y,p4.z]',[p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],[p3.x,p3.y,p3.z] , [p4.x,p4.y,p4.z]
        #print round(p1.dist(p2),2), round(p1.dist(Pa)+p2.dist(Pa),2) , round(p3.dist(p4),2) ,round(p3.dist(Pa)+p4.dist(Pa),2)
        if round(Pa.dist(Pb), 3) != 0.0:
            #print 'round(dista, 3) != 0.0, no intersection'
            intersection=False
            type=False
        elif [p2.x,p2.y,p2.z]==[p3.x,p3.y,p3.z]:
            type='edge'
            intersection=[p2.x,p2.y,p2.z]
            type='edge'
        elif [p1.x,p1.y,p1.z]==[p3.x,p3.y,p3.z]:
            intersection=[p1.x,p1.y,p1.z]
            type='edge'
        elif [p2.x,p2.y,p2.z]==[p4.x,p4.y,p4.z]:
            intersection=[p2.x,p2.y,p2.z]
            type='edge'
        elif [p1.x,p1.y,p1.z]==[p4.x,p4.y,p4.z]:
            intersection=[p1.x,p1.y,p1.z]
            type='edge'
        elif 0 in [round(Pa.dist(p1), 1), round(Pa.dist(p2), 1) ,round(Pa.dist(p3), 1),round(Pa.dist(p4), 1)] :
            #print 'touchdist', [round(Pa.dist(p1), 1), round(Pa.dist(p2), 1) ,round(Pa.dist(p3), 1),round(Pa.dist(p4), 1)]
            intersection=[Pa.x,Pa.y,Pa.z]
            type='touch'
        else:
            #print 'else:'
            intersection=False
            type=False
    # Lines are parallel
    #elif [p2.x,p2.y,p2.z]==[p3.x,p3.y,p3.z] and [p1.x,p1.y,p1.z]==[p4.x,p4.y,p4.z]:
        #print '2 lines are the same!! intersection set to false'
    #    intersection=False
    #    type=False'''
    #elif [p2.x,p2.y,p2.z]==[p4.x,p4.y,p4.z] and [p1.x,p1.y,p1.z]==[p3.x,p3.y,p3.z]:
        #print '2 lines are the same!! intersection set to false'
    #    intersection=False
    #    type=False'''

    else:

        #print 'else parallel'
        intersection = False
        type=False
    #print "INTERSECTION and type IS:", intersection, type
    return intersection, type
