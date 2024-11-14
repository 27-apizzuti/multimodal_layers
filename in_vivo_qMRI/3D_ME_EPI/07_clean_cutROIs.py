"""
Zeroed slices tfor which segmentation was not optimized

@author: apizz
"""
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import cmocean
from glob import glob
import pathlib

# -----------------------------------
HEMI = 'RH'

if HEMI == 'LH':
    slices = [61, 230]
else:
    slices = [85, 255]

MAIN_PATH = '/mnt/d/AHEAD_v2/derivatives/T2star_in-vivo/02_segmentation'
nii = nb.load(os.path.join(MAIN_PATH, "sub-01_visual_areas_hMT_plus_capsule_{}_bvbabel_ups2X_VORONOI_no_capsule.nii.gz".format(HEMI)))
data_mat = np.asarray(nii.dataobj)

new_data = np.zeros(np.shape(data_mat))
print(np.shape(new_data))
new_data[:, slices[0]-1:slices[1], :] = data_mat[:, slices[0]-1:slices[1], :]

new_data = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
nb.save(new_data, os.path.join(MAIN_PATH, "sub-01_visual_areas_hMT_plus_capsule_{}_bvbabel_ups2X_VORONOI_no_capsule_clean.nii.gz".format(HEMI)))
