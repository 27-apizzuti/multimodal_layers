"""
Stack 3D the data needed to compute layer profile
This avoid to iterate over each slice.

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob
import subprocess

# -----------------------------------
# # USER's ENTRIES

PATH_OUT = "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/10_PLOT_LAYER_PROFILES"

FOLDERS = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_VALUES",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS/2D_GM",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/02_LAYERS",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/09_BIAS_CORR_LP_HP",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_ROIS",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/03_ANGLES_VORONOI",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_MICR_LAB",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS"]

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

for folder in FOLDERS:
    base_folder = folder.split('/')[-1]

    if base_folder == '02_LAYERS':
        NIFTIS = sorted(glob(os.path.join(folder, '*metric_equivol.nii*')))
    else:
        NIFTIS = sorted(glob(os.path.join(folder, '*.nii*')))
    print(NIFTIS)
    nslices = np.shape(NIFTIS)[-1]
    print("Compressing {}".format(folder))

    for itnii, nifti in enumerate(NIFTIS):
        # Open NIFTI
        nii = nb.load(nifti)
        data = np.asarray(nii.dataobj)

        if itnii == 0:
            datatype = nii.header.get_data_dtype()
            dims = np.shape(data)
            new_data = np.zeros((dims[0], dims[1], nslices), dtype=datatype)

            # Create output name
            basename = nifti.split('/')[-1]
            temp = basename.split(os.extsep, 1)[0]
            outname = os.path.join(PATH_OUT, '{}_3D_stack'.format(temp))

        # // Fill in the new matrix
        new_data[..., itnii] = np.squeeze(data)

    # Save new nifti
    new_data2 = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
    nb.save(new_data2, outname)

print("Finished")
