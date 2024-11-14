"""
In order to create U,V coordinates we need to define 'control points' (see LN2_MULTILATERATE documentation)
Control points are defined on the midGM file (LN2_LAYERS output). For convenience, we stuck the midGM 2D slices in one NIFTI.

Afterwards, we manually load the output of this script in ITK-SNAP as a 'segmentation file'.
The chosen control points (one for each slice) are marked with label 2.   

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# VISUAL -----------------------------------
# USER's ENTRIES
FOLDERS = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/02_LAYERS"]
ROI_FOLDER = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_ROIS"

PATH_OUT = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/04_MIDGM"

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

for folder in FOLDERS:
    NIFTIS = sorted(glob(os.path.join(folder, '*midGM_equidist.nii*')))
    nslices = np.shape(NIFTIS)[-1]

    # ROIs nifti used as MASK
    MAS = sorted(glob(os.path.join(ROI_FOLDER, '*.nii*')))

    for itnii, nifti in enumerate(NIFTIS):

        # Open NIFTI
        nii = nb.load(nifti)
        data = np.asarray(nii.dataobj)

        # Open MASK
        nii2 = nb.load(MAS[itnii])
        mask = np.asarray(nii2.dataobj)
        mask[mask > 0] = 1
        data = np.multiply(data, mask)

        if itnii == 0:
            datatype = nii.header.get_data_dtype()
            dims = np.shape(data)
            new_data = np.zeros((dims[0], dims[1], nslices), dtype=datatype)

            # Create output name
            basename = nifti.split('/')[-1]
            temp = basename.split(os.extsep, 1)[0]
            outname = os.path.join(PATH_OUT, '{}_3D_mas_stack.nii.gz'.format(temp))

        # // Fill in the new matrix
        new_data[..., itnii] = np.squeeze(data)

    # Save new nifti
    new_data2 = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
    nb.save(new_data2, outname)

print("Finished")
