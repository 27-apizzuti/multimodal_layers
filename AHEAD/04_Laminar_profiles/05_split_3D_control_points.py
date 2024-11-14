"""
3D Mask midGM file with control points is split again as 2D series.

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
from copy import copy

# VISUAL -----------------------------------
# USER's ENTRIES
FILE1 = glob("/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/04_MIDGM/*_control_points.nii.gz")[0]

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/05_CONTR_POINTS"

if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)


filename = FILE1.split('/')[-1]
print(filename)
basename, ext = filename.split(os.extsep, 1)

SLICES = np.arange(141, 191)

# Open NIFTI
nii = nb.load(FILE1)
data = np.asarray(nii.dataobj)
datatype = nii.header.get_data_dtype()
# data = data[..., ::-1]

dims = np.shape(data)
print(dims)
pad = np.zeros((dims[0], dims[1], 1), dtype=datatype)
print(np.shape(pad))

for itslice in range(0, dims[2]):
    print(itslice)
    # Save control points
    pad = copy(data[..., itslice, None])
    pad[pad == 1] = 0
    pad[pad == 2] = 1
    numb = str(SLICES[itslice]).zfill(3)

    new_data = nb.Nifti1Image(pad, header=nii.header, affine=nii.affine)
    nb.save(new_data, os.path.join(OUTDIR, "{}_{}.nii.gz".format(basename, numb)))

    # Save domains
    pad2 = copy(data[..., itslice, None])
    pad2[pad2 > 0] = 1

    new_data = nb.Nifti1Image(pad2, header=nii.header, affine=nii.affine)
    nb.save(new_data, os.path.join(OUTDIR, "{}_domains_{}.nii.gz".format(basename, numb)))
