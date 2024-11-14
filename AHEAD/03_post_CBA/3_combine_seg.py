"""Combine cruise seg + WM brainvoyager segmentation"""

import os
import nibabel as nb
import numpy as np

# -------------------------------------------------------------------------
# Define input
# -------------------------------------------------------------------------
# Segmentatin files
FILE1 = "/mnt/d/AHEAD_v2/derivatives/122017/Volume_ROI_visAtlas-to-AHEAD/Ahead_brain_122017_cruise-left-cortex.nii.gz"
FILE2 = "/mnt/d/AHEAD_v2/derivatives/122017/Volume_ROI_visAtlas-to-AHEAD/Ahead_brain_122017_blockface-image_ISO_bvbabel_inverted_pt5_ACPC_seg-wm_lh_v05_to_02.nii.gz"

# Load data
nii = nb.load(FILE1)
seg = np.asarray(nii.dataobj)
seg[seg > 0 ] = 1

nii = nb.load(FILE2)
wm = np.asarray(nii.dataobj)
idx_wm = wm > 0

seg[idx_wm] = 2

# save
new_data = nb.Nifti1Image(seg, header=nii.header, affine=nii.affine)
nb.save(new_data, "/mnt/d/AHEAD_v2/derivatives/122017/Volume_ROI_visAtlas-to-AHEAD/Ahead_brain_122017_cruise-left-cortex_binarized_plus_GM.nii.gz")

print("Finished.")
