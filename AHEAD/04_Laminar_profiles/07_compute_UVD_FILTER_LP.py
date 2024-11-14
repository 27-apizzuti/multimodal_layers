"""
Filter to remove TEARS
Run low-pass filter using LN2_UVD_FILTER
We pass a cylinder with radious 0.5 and height 0.1 mm and compute the median operation

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# VISUAL -----------------------------------
# USER's ENTRIES
PATH1 = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_VALUES"
PATH2 =  "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/06_COORD_UV"
PATH3 =  "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/02_LAYERS"
PATH4 =  "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS/2D_GM"

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/07_UVD_FILT_LP"

RAD = 0.5
HEIG = 0.1

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

NIFTIS1 = sorted(glob(os.path.join(PATH1, '*.nii*')))
NIFTIS2 = sorted(glob(os.path.join(PATH2, '*.nii*')))
NIFTIS3 = sorted(glob(os.path.join(PATH3, '*metric_equivol.nii*')))
NIFTIS4 = sorted(glob(os.path.join(PATH4, '*.nii*')))

for it, nii in enumerate(NIFTIS1):
    basename = nii.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    outputname = os.path.join(OUTDIR, "{}_median_filt_LP.nii.gz".format(temp))

    command = "LN2_UVD_FILTER "
    command += "-values {} ".format(nii)
    command += "-coord_uv {} ".format(NIFTIS2[it])
    command += "-coord_d {} ".format(NIFTIS3[it])
    command += "-domain {} ".format(NIFTIS4[it])
    command += "-radius {} -height {} -median -output {}".format(RAD, HEIG, outputname)

    subprocess.run(command, shell=True)
    print(command)

print("LN2_UVDFILTER is done.")
