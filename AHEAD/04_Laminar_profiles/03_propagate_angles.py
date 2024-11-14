"""
Propagate 2D angular map (from 03_post_CBA\cutting_effect) using LN2_VORONOI

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# -----------------------------------
# USER's ENTRIES
ANG_PATH = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_ANGLES"
DOM_PATH = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS/2D_GM"
PATH_OUT = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/03_ANGLES_VORONOI"

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

NIFTIS = glob(os.path.join(ANG_PATH, '*.nii.gz'))

for nii in NIFTIS:
    basename = nii.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    outname = os.path.join(PATH_OUT, '{}'.format(temp))
    slice = temp.split('_')[-1]
    print(slice)
    domain = glob(os.path.join(DOM_PATH, "*{}.nii.gz".format(slice)))[0]
    print(domain)

    print('Propagating angular measure for slice: {}'.format(slice))
    command = "LN2_VORONOI "
    command += "-init {} ".format(nii)
    command += "-domain {} ".format(domain)
    command += "-output {} ".format(outname)
    subprocess.run(command, shell=True)
print("Finished")
