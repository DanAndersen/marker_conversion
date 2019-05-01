# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:09:38 2019

@author: andersed
"""

in_filename = "in_positions_dodec.csv"
marker_size_mm = 16.0 # only the size of the black portion not including the white border

out_filename = "ultrasound_dodec.dat"

import csv
import numpy as np

ids_to_exclude = [1, 12]

marker_ids = []
mats = []

# coordinate system info http://www.hitl.washington.edu/artoolkit/documentation/cs.htm

with open(in_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        
        row_vals = np.array(row, dtype=np.float)
        
        marker_id = int(row_vals[0])
        
        if marker_id not in ids_to_exclude:
            
            center = row_vals[1:4]
            c1 = row_vals[4:7]
            c2 = row_vals[7:10]
            c3 = row_vals[10:13]
            c4 = row_vals[13:16]
            
            x_axis = c2 - c1
            x_axis = x_axis / np.linalg.norm(x_axis)
            
            y_axis = c1 - c3
            y_axis = y_axis / np.linalg.norm(y_axis)
            
            z_axis = np.cross(x_axis, y_axis)
            
            mat = np.eye(4)
            mat[0:3,0] = x_axis
            mat[0:3,1] = y_axis
            mat[0:3,2] = z_axis
            mat[0:3,3] = center
            
            marker_ids.append(marker_id)
            mats.append(mat)
            
with open(out_filename, "w") as out_file:
    out_writer = csv.writer(out_file, delimiter=' ')
    
    out_writer.writerow([len(marker_ids)])
    for i in range(len(marker_ids)):
        marker_id = marker_ids[i]
        mat = mats[i]
        
        out_writer.writerow([marker_id])
        out_writer.writerow([marker_size_mm])
        
        out_writer.writerow(mat[0])
        out_writer.writerow(mat[1])
        out_writer.writerow(mat[2])
        