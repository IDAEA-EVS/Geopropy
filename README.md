***geopropy***

This repository contains Automatic 3D Geological Cross Section Generation.
For more info, refer to this [article](https://doi.org/10.1016/j.envsoft.2022.105309)

##############################


***Package information:***\
\
Name: geopropy

version: 0.1.alpha

Author: Ashkan Hassanzadeh   

Email: ashkan.hassanzadeh@gmail.com

python: 2.7.*

License: agpl-3.0

##############################

***Installation:***\
\
Since geopropy uses arcpy, Be sure to install an ArcGIS version that runs python 2.7 (such as 10.5).\
Download geopropy folder, place it directly with other libraries where you installed python, or add the folder directory to your Environment path.
Installation can be done by cloning the repository.

##############################


***Jupyter Notebook:***\
\
To reproduce the synthetic databases, there are Jupyter notebooks that can be found in 'Examples' repository. In case of problem in semi-automatic stage visualization, execute the commands in terminal. 

##############################

***Instruction manual to complete the new tables added to HYDOR Database:***
\
\
\
\
**change in Borehole_(Sub)Units/Lithology table**

    In points that there is a fault in a borehole, Top_Depth and Bottom_Depth have to be equal, and same as the depth of the fault point. the (Sub)Units field have to be chosen as 'fault'.

##############################

**Borehole_Chronopriority**

*prority_number*: (mandatory)

    The number that shows the chronological sequence on the geological structures in a way that prority_number equal to one is the oldest structure and the highest prority_number is the newest structure 

*type*: (mandatory)
	
    Structures compatible to process in this application are normal, intrusion, fault (diverse forms) and discordancy. For each one the mentioned structure, the table have to be complete in a specific way:

	-normal
		>top_layer: (mandatory)
		>bottom_layer: (mandatory)
			
	-intrusion
		>top_layer: leave empty (blank) - (mandatory)
		>bottom_layer: choose the unit name - (mandatory)
	-fault 
		(information have to be completed in fault_table and Borehole_(Sub)Units
		>top_layer: leave empty (blank) - (mandatory)
		>bottom_layer: leave empty (blank) - (mandatory)
	-discordancy
		>top_layer: (mandatory)
		>bottom_layer: leave empty (blank) - (mandatory)

*preferred_angle*: optional

    In case additional information about the angle of a layer needed, program will use this angle (in degree).

##############################

**fault_table**

*priority_number*:

	The priorities available to choose in this table, are marked as fault in Borehole_Chronopriority table. 	

*Borehole_ID*:

	Borehole ID of the fault point 

*Elevation*:  

        elevation of the fault point

*preferred_angle*: optional

    In case additional information about the angle of a layer needed, program will use this angle (in degrees).

*type*: 

        Have to be set to 'fault'

##############################

**Topo_points**

This table saves the available surface points information

*X*:

        x coordination of the surface point

*Y*:

        y coordination of the surface point

*Z*:

        z coordination of the surface point 

*priority_num*:  optional  

        If just the geolocation data of the point is available, this field have to be empty. If the point is a contact point between 2 geological structures, the priority number (indicated in Borehole_Chronopriority table) of geological layer have to be identified here.   

*Type*:

        Have to be set to 'Topography'

*Polarity*: optional

        In case the point has priority information, the polaroty of the point has be identified.

*Angle*: optional

        In case the point has priority information, if there is a preferred angle for the surface layers and the connection between them, it can be introduced here.
##############################

##############################

**geopropy help**

 **cross_section** method generates geological cross sections in 3D in 3 stages based on the available data
    the X coordination of boreholes have to be increasing.


*cross_section default variables*


*18 variables*


*Database_dir* 

        A string to define Hydor geodatabase direction (.mdb) 

*boretemp*

        A python list contains borehole ids

*Lithology_table*

        Table in database that corresponds to geological units in boreholes        

    
*box_bottom_rate*

        1.1 (default) optional

*bottomlength*

        15 (default) optional

*predefined_angle_degree*

        45 in degrees (default) optional

*Merge_Layers*

        {False(default),True} optional

*bottom_box_type*

        {'normalbottombox' (default),'ratiobottombox'} optional

*xshifter*

        0.5 (default) optional --Shift borehoel x coordination in case it is same as previous borehole by xshifter amount.

*yshifter*

        0.5 (default) optional --Shift borehoel y coordination in case it is same as previous borehole by yshifter amount.

*epsbn_ratio*

        0.05 (default) optional --A ratio based on borehole distance for 3D to 2D convertion of the points in boundary of the cross section.  

*eps_ratio*

        0.01 (default) optional --A ratio based on borehole distance for 3D to 2D convertion of the points everywhere except in boundary of the cross section.

*ExtendLine_edit_distance*

    5 (default) optional --The maximum distance a line segment can be extended to an intersecting feature.

    Refer to arcpy.ExtendLine_edit function for more info.

*TrimLine_edit_dangle_length*

    2 (default) optional --Line segments that are shorter than the specified Dangle Length and do not touch another line at both endpoints (dangles) will be trimmed.

    Refer to arcpy.TrimLine_edit function for more info.

*Integrate_management_distance*

    0.01 (default) optional --The distance that determines the range in which feature vertices are made coincident. To minimize undesired movement of vertices, the x,ytolerance should be fairly small.
    
    Refer to arcpy.Integrate_management function for more info

*del_x*

        10 (default) optional -- The radius in X axis to project surface point to 3D cross sections

*del_y*

        10 (default) optional -- The radius in Y axis to project surface point to 3D cross sections

*smooth_2d*

        False (default) optional --if true, a smoothed version of 2d cross section will be generated 

*gen_polygons*

        True (default) optional --if false, the procedure stops after generating 3d lines! This means 2D cross section is not gonna be generated.

*developer_mode*

        True (default) optional --if false, the error handling is more general and with less details        
        
