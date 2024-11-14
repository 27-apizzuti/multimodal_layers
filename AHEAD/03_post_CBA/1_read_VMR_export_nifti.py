"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/d/AHEAD_v2"
PATH_OUT = os.path.join(STUDY_PATH, 'Volume_ROI_visAtlas-to-AHEAD')

# Define VMR
# Segmentation file
FILENAME = "/mnt/d/AHEAD_v2/derivatives/122017/01_ROI/CBA/LH/122017_MTatlas_capsule_LH.vmr"
# FILENAME = "/mnt/d/AHEAD_v2/derivatives/122017/CBA-prep/Ahead_brain_122017_blockface-image_ISO_bvbabel_inverted_pt5_ACPC_seg-wm_rh_v04.vmr"
FILE = os.path.join(FILENAME)

# Load vmr
header, data = bvbabel.vmr.read_vmr(FILE)

# See header information
pprint.pprint(header)

# Export nifti
basename = FILENAME.split(os.extsep, 1)[0]
outname = os.path.join(PATH_OUT, "{}_bvbabel.nii.gz".format(basename))
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
