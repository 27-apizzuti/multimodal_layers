"""
Run LN_2LAYERS for each 2D slice

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# VISUAL -----------------------------------
# USER's ENTRIES
PATH_IN = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/03_Layers/01_2D_RIMS"
OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/03_Layers/02_LAYERS"

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

NIFTIS = sorted(glob(os.path.join(PATH_IN, '*.nii*')))

for nii in NIFTIS:
    basename = nii.split('/')[-1]
    outname = os.path.join(OUTDIR, '{}'.format(basename.split(os.extsep, 1)[0]))
    print('Computing layers for: {}'.format(nii))
    command = "LN2_LAYERS "
    command += "-rim {} ".format(nii)
    command += "-equivol "
    command += "-output {} ".format(outname)
    subprocess.run(command, shell=True)
print("Finished")
