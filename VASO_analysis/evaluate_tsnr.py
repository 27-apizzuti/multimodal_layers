"""
Created on Mon Jul 25 11:05:11 2022

Quantification t-SNR in ROI

@author: apizz
"""

import os
import numpy as np
import bvbabel
from copy import copy
import nibabel as nb

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD", "VASO_interp_LN"]
ROI_NAME = ["rightMT_Sphere16radius", "leftMT_Sphere16radius"]

for su in SUBJ:
    PATH_TSNR = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'boco')
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')

    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'boco', 'tSNR')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    for roi in ROI_NAME:
        for fu in FUNC:

            FILENAME_TSNR = '{}_tSNR.nii'.format(fu)
            FILENAME_ROI = '{}_{}.nii.gz'.format(su, roi)

             # Read nifti tsnr
            nii1 = nb.load(os.path.join(PATH_TSNR, FILENAME_TSNR))
            nii_tsnr = nii1.get_fdata()
            nii_tsnr = nii_tsnr[:, :, :, 0]

            # Read nifti ROI
            nii2 = nb.load(os.path.join(PATH_MASK, FILENAME_ROI))
            nii_roi = nii2.get_fdata()

            idx = nii_roi > 0

            ROI_tSNR = np.nanmean(nii_tsnr[idx])

            print('{} {} tSNR for {} : {}'.format(su, fu, roi, ROI_tSNR))
