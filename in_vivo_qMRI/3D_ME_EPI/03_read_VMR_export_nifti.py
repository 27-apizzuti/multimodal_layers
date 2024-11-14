"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

PATH_OUT = "/mnt/d/AHEAD_v2/derivatives/demo_whole_brain/CBA/"
HEMI = 'LH'

# Define VMR
# Segmentation file
FILENAME = "/mnt/d/AHEAD_v2/derivatives/demo_whole_brain/{}-CBA/sub-01_visual_areas_hMT_capsule_{}.vmr".format(HEMI, HEMI)
# FILENAME = "/mnt/d/AHEAD_v2/derivatives/122017/CBA-prep/Ahead_brain_122017_blockface-image_ISO_bvbabel_inverted_pt5_ACPC_seg-wm_rh_v04.vmr"
FILE = os.path.join(FILENAME)

# Load nifti for the header
NII_REF = "/mnt/d/AHEAD_v2/derivatives/demo_whole_brain/seg-01_{}_rim.nii.gz".format(HEMI)
nii = nb.load(NII_REF)

# Load vmr
header, data = bvbabel.vmr.read_vmr(FILE)
data = data[::-1, :, :]

# See header information
pprint.pprint(header)

# Export nifti
basename = FILENAME.split(os.extsep, 1)[0]
outname = os.path.join(PATH_OUT, "{}_bvbabel.nii.gz".format(basename))
img = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
nb.save(img, outname)

print("Finished.")
