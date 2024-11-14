"""
Creation of U,V coordinates

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# VISUAL -----------------------------------
# USER's ENTRIES
PATH = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/05_CONTR_POINTS"

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/06_COORD_UV"

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

OUTDIR = os.path.join(OUTDIR, '01')
if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

NIFTIS1 = sorted(glob(os.path.join(PATH, '*control_points_[0-9]*.nii*')))
NIFTIS2 = sorted(glob(os.path.join(PATH, '*control_points_domains_[0-9]*.nii*')))

for it, nii in enumerate(NIFTIS1):

    basename = nii.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    outputname = os.path.join(OUTDIR, "{}_geodistance.nii.gz".format(temp))

    command = "LN2_GEODISTANCE "
    command += "-domain {} ".format(NIFTIS2[it])
    command += "-init {} ".format(nii)
    command += "-output {}".format(outputname)
    subprocess.run(command, shell=True)
    print(command)

print("LN2_GEODISTANCE is done.")
# ----------------------------
# RUN LN2_VORONOI
PATH1 = OUTDIR
PATH2 = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS/2D_GM"

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/06_COORD_UV/02"

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

NIFTIS1 = sorted(glob(os.path.join(PATH1, '*.nii*')))
NIFTIS2 = sorted(glob(os.path.join(PATH2, '*.nii*')))

for it, nii in enumerate(NIFTIS1):

    basename = nii.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    outputname = os.path.join(OUTDIR, "{}_voronoi.nii.gz".format(temp))

    command = "LN2_VORONOI "
    command += "-domain {} ".format(NIFTIS2[it])
    command += "-iter_smooth 100 "
    command += "-init {} -output {}".format(nii, outputname)
    subprocess.run(command, shell=True)

print("LN2_VORONOI is done.")
# --------------------------------------
PATH_IN = OUTDIR
OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/06_COORD_UV"

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)

# -----------------------------------
# // Load data
NIFTIS = sorted(glob(os.path.join(PATH_IN, '*.nii.gz')))

for it, file in enumerate(NIFTIS):
    nii = nb.load(file)
    data = np.asarray(nii.dataobj)
    dims = np.shape(data)
    datatype = nii.header.get_data_dtype()

    new_data = np.ones((dims[0], dims[1], dims[2], 2), dtype=datatype)
    new_data[..., 0] = data

    # Save
    basename = file.split('/')[-1]
    temp = basename.split(os.extsep, 1)[0]
    new_nii = nb.Nifti1Image(new_data, affine=nii.affine, header=nii.header)
    nb.save(new_nii, os.path.join(OUTDIR, "{}_coord_UV.nii.gz".format(temp)))
