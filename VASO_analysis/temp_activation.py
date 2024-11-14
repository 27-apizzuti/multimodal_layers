"""
Created on Mon Jul 25 12:09:36 2022

Evaluate activity volume

@author: apizz
"""

import os
import numpy as np
import bvbabel
from copy import copy
from skimage.measure import label

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["leftMT_Sphere16radius", "rightMT_Sphere16radius"]

for su in SUBJ:
    # Read VMP
    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'GLM', 'ROI')
    for roi in ROI_NAME:
        for fu in FUNC:
            print("Working on {} {} {}".format(su, fu, roi))
            if fu == "VASO_interp_LN":
                FILENAME_VMP = "{}_{}_meanRuns_{}_ROI_{}_c_thr_4_BOLDMASK_preference_metrics.vmp".format(su, fu, CONDT[0], roi)
            else:
                FILENAME_VMP = "{}_{}_meanRuns_{}_ROI_{}_c_thr_4_preference_metrics.vmp".format(su, fu, CONDT[0], roi)

            # Load VMP
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data_vmp = bvbabel.vmp.read_vmp(IN_FILE)

            idx = data_vmp[..., 0] > 0

            count = np.sum(idx)
            print('{} {} {} count: {}'.format(su, fu, roi, count))





# Count activation in map (1) [both BOLD and VASO are positive]
