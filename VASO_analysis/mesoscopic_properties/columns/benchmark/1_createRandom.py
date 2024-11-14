"""
Created on Thu Oct  6 16:10:27 2022

Create random winner map from the winner map at 0.8
Updameple random winner map
Compute columnarity
Plot PDF of random next to the empirical PDF 

@author: apizz
"""

import numpy as np
import nibabel as nb
import os
import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CAT = np.array([1, 2, 3, 4])

for itSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt8') 
    FILENAME = '{}_leftMT_Sphere16radius.nii.gz'.format(su)

    # Create output directory
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'random_columns')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
    
    # Load the winner map
    nii = nb.load(os.path.join(PATH_IN, FILENAME))
    vox_map = nii.get_fdata()
    
    data = copy.copy(vox_map)

    idx = data > 0
    temp_data = data[idx]
    n_vox = np.size(temp_data)

    for i in range(0, n_vox):
        lab = np.random.choice(CAT)
        temp_data[i] = lab

    # Put back
    data[idx] = temp_data

    # Save nifti
    out_name = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_random.nii.gz'.format(su))
    out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
    nb.save(out, out_name)
    
    
    
