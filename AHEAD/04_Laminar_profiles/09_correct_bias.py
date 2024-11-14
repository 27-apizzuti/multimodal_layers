"""
Use the previous output to correct the original microscopy data for bias field inhomogeneity

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# -----------------------------------
# USER's ENTRIES
# PATH1 = "/mnt/c/Users/apizz/Desktop/AHEAD_layers/3D_inputs/BIAS_FIELD/V5/2D_UVD_FILT_LP"
# PATH2 =  "/mnt/c/Users/apizz/Desktop/AHEAD_layers/3D_inputs/BIAS_FIELD/V5/2D_UVD_FILT_LP_HP"
#
# OUTDIR = "/mnt/c/Users/apizz/Desktop/AHEAD_layers/3D_inputs/BIAS_FIELD/V5/2D_BIAS_CORR_LP_HP"
# SOMATOSENSORY -----------------------------------
# USER's ENTRIES
PATH1 = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/07_UVD_FILT_LP"
PATH2 =  "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/08_UVD_FILT_LP_HP"

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/09_BIAS_CORR_LP_HP"
if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

NIFTIS1 = sorted(glob(os.path.join(PATH1, '*.nii*')))
NIFTIS2 = sorted(glob(os.path.join(PATH2, '*.nii*')))

for it, nii in enumerate(NIFTIS1):
    basename = nii.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    outputname = os.path.join(OUTDIR, "{}_bias_corrected.nii.gz".format(temp))

    nii1 = nb.load(nii)
    data = np.asarray(nii1.dataobj)

    nii2 = nb.load(NIFTIS2[it])
    median = np.asarray(nii2.dataobj)

    new_data = np.divide(data, median)
    new_nii = nb.Nifti1Image(new_data, affine=nii1.affine, header=nii1.header)
    nb.save(new_nii, "{}".format(outputname))

print("Bias correction is done.")
