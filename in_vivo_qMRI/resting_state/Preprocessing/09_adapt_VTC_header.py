# This script adapts the header of the VTC by allowing to map to VMR with double res. 0.35 iso mm

import numpy as np
import os
import glob
import bvbabel

print("Hello.")

# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-04"]
SESS = ["sess-02"]
TASK = ["rest"]

for su in SUBJ:
    for se in SESS:
        print('Working on {}, {}'.format(su, se))
        PATH_VTC = os.path.join(STUDY_PATH, su, 'derivatives', 'func', se, 'MOT_VTC_cut')
        VTC = glob.glob(os.path.join(PATH_VTC, '*.vtc'))
        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', se, 'MOT_VTC_cut_2x')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)

        for file_vtc in VTC:
            #// Change output name
            basename = file_vtc.split(os.extsep, 1)[0]
            outname = basename.split("/")[-1]
            output_file = os.path.join(PATH_OUT, "{}_res2x.vtc".format(outname, se))

            #// Adjust header with double resolution
            print('Create secondary VTC with adapted header to 2x')
            outname = os.path.join(PATH_OUT, "{}_{}_BBR_resx2.vtc".format(outname, se))

            header, data = bvbabel.vtc.read_vtc(file_vtc, rearrange_data_axes=False)
            header["VTC resolution relative to VMR (1, 2, or 3)"] = 2
            header["XEnd"] = header["XEnd"] *2
            header["XStart"] = header["XStart"] *2

            header["YEnd"] = header["YEnd"]*2
            header["YStart"] = header["YStart"] *2

            header["ZEnd"] = header["ZEnd"] *2
            header["ZStart"] = header["ZStart"] *2
            bvbabel.vtc.write_vtc(output_file, header, data, rearrange_data_axes=False)
