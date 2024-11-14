"Merging segmentation"

import nibabel as nb
import numpy as np
from time import time
import os
from glob import glob
import pathlib
import subprocess

# -----------------------------------
# USER's ENTRIES
FILE1= "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/02_segmentation/initial_ROIs/122017_MTatlas_capsule_LH_bvbabel_to_02_cut.nii.gz"
FILE2="/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/02_segmentation/initial_ROIs/Ahead_brain_122017_LH_visAtlas-short_plus_capsule_bvbabel_to_02_cut.nii.gz"

OUTNAME = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/02_segmentation/initial_ROIs/Ahead_brain_122017_LH_MTatlas_V1V2V3_capsule.nii.gz"

nii1 = nb.load(FILE1)
roi1 = np.asarray(nii1.dataobj)
roi1[roi1 > 1] = 5

nii2 = nb.load(FILE2)
roi2 = np.asarray(nii2.dataobj)
# roi2[..., 22:141] = 0  # RH
roi2[..., 42:127] = 0    # LH
roi2[roi2 == 1] = 5
roi2[roi1 == 1] = 1
roi2[roi1 == 5] = 5

gmag = nb.Nifti1Image(roi2, header=nii1.header, affine=nii1.affine)
nb.save(gmag, "{}".format(OUTNAME))

# -----------------------------------
# # Load segmentation and remove ones across slices
# FILE3 = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/RH/Ahead_brain_122017_RH_RIM_polished_cut_141_190_and_22_72_warped_2D_polished_farukv01.nii.gz"
# OUTNAME = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/RH/Ahead_brain_122017_RH_RIM_polished_cut_141_190_and_22_72_warped_2D_polished_final.nii.gz"

# nii1 = nb.load(FILE3)
# seg = np.asarray(nii1.dataobj)
# seg[..., 0:22] = 0
# seg[..., 72:140] = 0
# seg[..., 191:302] = 0

# gmag = nb.Nifti1Image(seg, header=nii1.header, affine=nii1.affine)
# nb.save(gmag, "{}".format(OUTNAME))