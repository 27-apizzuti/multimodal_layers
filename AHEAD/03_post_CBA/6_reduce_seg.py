"""Combine cruise seg + WM brainvoyager segmentation"""

import os
import nibabel as nb
import numpy as np

# -------------------------------------------------------------------------
# Define input
# -------------------------------------------------------------------------
# Segmentatin files
# FILE1 = "/mnt/d/AHEAD_v2/derivatives/122017/01_ROI/Volume_ROI_visAtlas-to-AHEAD/Ahead_brain_122017_RH_RIM_polished.nii.gz"
FILE1 = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/RH/Original_dimension/Ahead_brain_122017_RH_RIM_polished.nii.gz"

BOX_x = [6, 493]
BOX_y = [67, 706]
BOX_z = [564, 860]

# Load data
nii = nb.load(FILE1)
seg = np.asarray(nii.dataobj)

# Reduce data
new_data = np.zeros(np.shape(seg), dtype=np.int8)
new_data[BOX_x[0]: BOX_x[1], BOX_y[0]: BOX_y[1], BOX_z[0]: BOX_z[1]] = seg[BOX_x[0]: BOX_x[1], BOX_y[0]: BOX_y[1], BOX_z[0]: BOX_z[1]]

# save
new_data = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
nb.save(new_data, "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/RH/Original_dimension/Ahead_brain_122017_RH_RIM_polished_ext.nii.gz")
