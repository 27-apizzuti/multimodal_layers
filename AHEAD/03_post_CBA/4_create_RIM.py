"""Add CSF to WM/GM and prepare whole brain RIM file"""
import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/AHEAD_v2/derivatives/122017/Volume_ROI_visAtlas-to-AHEAD'

# Load nifti: whole brain segmentation
WMGM = os.path.join(STUDY_PATH, 'Ahead_brain_122017_cruise-right-cortex_binarized_plus_GM.nii.gz')
wmgm_file =  nb.load(os.path.join(STUDY_PATH, WMGM))
wmgm_data = np.asarray(wmgm_file.dataobj)
wmgm_data = np.round(wmgm_data)
wmgm_data = wmgm_data.astype(int)


# Load nifti: brainmask
CSF = os.path.join(STUDY_PATH, 'Ahead_brain_122017_blockface-image.nii.gz')
csf_file =  nb.load(os.path.join(STUDY_PATH, CSF))
csf_data = np.asarray(csf_file.dataobj)

# Create RIM file
new_data = np.ones(np.shape(wmgm_data), dtype=np.int8)
new_data[csf_data != 0] = 1
new_data[wmgm_data == 1] = 3
new_data[wmgm_data == 2] = 2

# Save nifti
outname = os.path.join(STUDY_PATH, 'Ahead_brain_122017_RH_RIM.nii.gz')
img = nb.Nifti1Image(new_data, affine=np.eye(4))
nb.save(img, outname)

# Save also only GM
wmgm_data[wmgm_data == 2] = 0
wmgm_data[wmgm_data == 1] = 1

outname = os.path.join(STUDY_PATH, 'Ahead_brain_122017_RH_RIM_GM.nii.gz')
img = nb.Nifti1Image(wmgm_data, affine=np.eye(4))
nb.save(img, outname)
