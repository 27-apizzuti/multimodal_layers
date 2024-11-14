"""
Crop NIFTI to reduce data dimensions

@author:apizz

"""
import numpy as np
import nibabel as nb
import glob
import os

# !!!! Left hemisphere !!!!
filenames = [
"Ahead_brain_122017_MRI-proton-density", "Ahead_brain_122017_MRI-quantitative-R1", "Ahead_brain_122017_MRI-quantitative-R2star"]

cropDims = {'x':[464,933],
            'y':[36,620],
            'z': [558,860]}

tmpDims = f"{cropDims['x'][0]} {cropDims['x'][1]-cropDims['x'][0]} {cropDims['y'][0]} {cropDims['y'][1]-cropDims['y'][0]} {cropDims['z'][0]} {cropDims['z'][1]-cropDims['z'][0]}"
for it in filenames:
    file = '/mnt/d/AHEAD_v2/Ahead_brain_122017-3D_reconstructions/{}.nii.gz'.format(it)
    file_out = '/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/{}_LH_cut.nii.gz'.format(it)
    truncCommand = f'fslroi {file} {file_out} {tmpDims}'
    os.system(truncCommand)

# ------------------------------------
# # !!!! Right hemisphere !!!!!

# filenames = [
# "Ahead_brain_122017_MRI-proton-density", "Ahead_brain_122017_MRI-quantitative-R1", "Ahead_brain_122017_MRI-quantitative-R2star", "Ahead_brain_122017_cruise-right-wm-surface"]

# filenames = [
# "Ahead_brain_122017_cruise-right-cortex_binarized_plus_GM"]

# cropDims = {'x':[6, 493],
#             'y':[67, 706],
#             'z': [558, 860]}

# tmpDims = f"{cropDims['x'][0]} {cropDims['x'][1]-cropDims['x'][0]} {cropDims['y'][0]} {cropDims['y'][1]-cropDims['y'][0]} {cropDims['z'][0]} {cropDims['z'][1]-cropDims['z'][0]}"

# for it in filenames:
#     file = '/mnt/d/AHEAD_v2/Ahead_brain_122017-3D_reconstructions/{}.nii.gz'.format(it)
#     file_out = '/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/{}_RH_cut.nii.gz'.format(it)
#     truncCommand = f'fslroi {file} {file_out} {tmpDims}'
#     os.system(truncCommand)
