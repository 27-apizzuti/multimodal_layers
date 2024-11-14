"""
Created on Thu Oct  6 12:25:36 2022
Compare the CV_BOLD_mask with the AllPositiveMASK
@author: apizz
"""

import os
import numpy as np
import nibabel as nb

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
MASK = ["CV_BOLD_mask", "CV_VASO_mask"]
ROI_NAME = "rightMT_Sphere16radius"

for i, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'masks')
    for it, fu in enumerate(FUNC):
        print("Processing {} {} ".format(fu, su))

        # Read CV mask
        nii1 = nb.load(os.path.join(PATH_IN, "{}_{}_{}.nii.gz".format(su, ROI_NAME, MASK[it])))
        nii_CV = nii1.get_fdata()
        
        idx1 = nii_CV == 1

        # Read nifti All Positives T-values
        nii2 = nb.load(os.path.join(PATH_IN, "{}_{}_{}_allPositiveTValues_voxels.nii.gz".format(su, ROI_NAME, fu)))
        nii_POS = nii2.get_fdata()
        idx2 = nii_POS == 1
        
        # Combine the two mask
        idx3 = idx1 * idx2
        
        # Count number of voxels discarted
        n1 = np.sum(idx1)
        n2 = n1 - np.sum(idx3)
        p = (n2/n1)*100
        
        print('Removed voxels {} {} = {} (from {}) [{}%]'.format(su, fu, n2, n1, p))
        print('Surviving voxels {} {} = {}'.format(su, fu, np.sum(idx3)))
        
        # Save new mask
        new_data = np.zeros(np.shape(nii_CV))
        new_data[idx3] =  1
        outname = os.path.join(PATH_IN, "{}_{}_{}_CV_allPositiveTValues.nii.gz".format(su, ROI_NAME, fu))
        img = nb.Nifti1Image(new_data, affine=nii1.affine)
        nb.save(img, outname)
        
        # Read t-maps
        PATH_MAP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                        'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
        
        nii3 = nb.load(os.path.join(PATH_MAP, "{}_{}_{}_tmaps.nii.gz".format(su, fu, ROI_NAME)))
        nii_map = nii3.get_fdata()
        
        # Apply CV mask to each map
        c = np.zeros(4)
        d = np.zeros(4)
        for it in range(0, np.shape(nii_map)[-1]-1):
            print(it)
            CVmap = nii_map[idx1, it]
            idxNeg = CVmap < 0
            c[it] = (np.sum(idxNeg)/n1) * 100
            d[it] = np.sum(idxNeg)
            
        print('Removed voxels {} {}: {}'.format(su, fu, c))
        print('Average removal {} {}: {}'.format(su, fu, np.mean(c)))
        print('2) Average removal {} {}: {}'.format(su, fu, (np.sum(d)/ (n1*4)*100)))
            
                        
        
        
        
        
        
        
        
        
        
        