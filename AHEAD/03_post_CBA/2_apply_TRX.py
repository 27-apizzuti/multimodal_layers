"""Apply transformation + upsample to 0.2 iso mm to segmentation/ROIs"""

import os
import nibabel as nb
import bvbabel
import subprocess

# -------------------------------------------------------------------------
# Define input
# -------------------------------------------------------------------------
# Point to the reference NIFTI
REF_NIFTI = "/mnt/d/AHEAD_v2/derivatives/122017/01_ROI/Volume_ROI_visAtlas-to-AHEAD/Ahead_brain_122017_blockface-image.nii.gz"

# Point to trx file
TRX = "/mnt/d/AHEAD_v2/derivatives/122017/01_ROI/Volume_ROI_visAtlas-to-AHEAD/BV_ISOACPC_to_native.mat"

# In/out directory
PATH_IN_OUT = "/mnt/d/AHEAD_v2/derivatives/122017/01_ROI/Volume_ROI_visAtlas-to-AHEAD"

NIFTIS = ["122017_MTatlas_capsule_LH_bvbabel.nii.gz", "122017_MTatlas_capsule_RH_bvbabel.nii.gz"]

# -------------------------------------------------------------------------
# Apply affine transformation matrix
# -------------------------------------------------------------------------
# Prepare output
for file in NIFTIS:
    basename = file.split(os.extsep, 1)[0]
    IN_NIFTI = os.path.join(PATH_IN_OUT, file)
    OUT_NIFTI = os.path.join(PATH_IN_OUT, "{}_to_02.nii.gz".format(basename))

    # Execute
    command = "greedy "
    command += "-d 3 "
    command += "-rf {} ".format(REF_NIFTI)  # reference
    command += "-ri LABEL 0.5vox "
    # command += "-ri NN "
    command += "-rm {} {} ".format(IN_NIFTI, OUT_NIFTI)  # moving resliced
    command += "-r {} ".format(TRX)

    # Execute command
    subprocess.run(command, shell=True)

print("Finished.")
