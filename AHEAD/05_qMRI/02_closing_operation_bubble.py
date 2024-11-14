"""
Closing operation through morphology

The input file is obtained by using ITK-SNAP, segmentation menu.
'Bubble' are very bright in R2* data. Simple intensity-based threshold tool will capture it.
This operation makes the inside of the 'bubbles' more homogeneous. 

@author:apizz
"""

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

# Segmentation file
FILE = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/01_remove_bubble/Ahead_brain_122017_segmentation_bubble_LH.nii.gz"
# FILE = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_RH_RIM_polished_cut_22_72_3D_polished_brainmask.nii.gz"

# Integer labels for tissue classes
bubble = 1

# =============================================================================
# Load data
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)
# data = np.pad(data, 1, mode="reflect")  # to prevent data edge artifacts
# -----------------------------------------------------------------------------
new_data = np.zeros(np.shape(data))
print('New data dims: {}'.format(np.shape(new_data)))

# Separate white matter
wm = data == bubble

# [Step-01] Dilate (to preserve thin bridges frequent in white matter)
struct = generate_binary_structure(3, 1)  # 2 Number of dimensions of the array to which the stru}cturing element will be applied # 1 jump neighbourbhood
wm = morphology.binary_dilation(wm, structure=struct, iterations=3)   # 3 bubble   # 5 brainmask

# [Step-02] Smooth
FWHM = 2  # Full width half maximum of Gaussian kernel. In voxel size units.
SIGMA = FWHM / 2.35482004503  # Convert to filter standard deviation
wm = gaussian_filter(wm.astype(float), sigma=SIGMA, mode="reflect")
wm = wm > 0.5

# [Step-03] Erode (to go back to original white matter average thickness)
wm = morphology.binary_erosion(wm, structure=struct, iterations=3)   # 3 bubble   # 5 brainmask

new_data[wm !=0] = 1

# Save as nifti
SUFFIX = "closed"
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(new_data.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_{}.{}".format(basename, SUFFIX, ext))

print("Finished. Don't forget the check the result carefully!.")
