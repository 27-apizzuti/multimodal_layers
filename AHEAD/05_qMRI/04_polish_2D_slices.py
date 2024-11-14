"""Run this script after the segmentation file was manually polished. """

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

# USER'S SPECIFICATIONS
# // RH
FILE = "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/RH/02/Ahead_brain_122017_RH_RIM_polished_cut_141_190_and_22_72_warped_2D_polished_final.nii.gz"
SLICES = [[22,72], [141,191]]   # hMT+  # V1, V2, V3
# SLICES = [[22,72]]   # hMT+  # V1, V2, V3

# // LH
# FILE = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/Ahead_brain_122017_LH_RIM_polished_cut_43_93.nii.gz"
# SLICES = [[43, 93], [127, 177]]    # hMT+ # V1, V2, V3

# # =============================================================================

# Integer labels for tissue classes
WM = 2
GM = 3

# Load data
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)
data = np.pad(data, 1, mode="reflect")  # to prevent data edge artifacts
# -----------------------------------------------------------------------------
new_data = np.ones(np.shape(data))
print('New data dims: {}'.format(np.shape(new_data)))

# # // Iterate across SLICES
slice_range = []
for interval in range(0, len(SLICES)):
    INTV = SLICES[interval]
    slice_range.append(np.arange(INTV[0], INTV[1]+1)) # include the 850

slice_range = np.asarray(slice_range).flatten()


print('Slice range: {}'.format(slice_range))
print('Number of slices: {}'.format(np.shape(slice_range)))

for slice in slice_range:
    print("Working on slice: {}".format(slice))

    # Separate white matter
    wm = data[..., slice] == WM
    print(np.shape(wm))

    # [Step-01] Dilate (to preserve thin bridges frequent in white matter)
    struct = generate_binary_structure(2, 1)  # 2 Number of dimensions of the array to which the stru}cturing element will be applied # 1 jump neighbourbhood
    wm = morphology.binary_dilation(wm, structure=struct, iterations=3)

    # [Step-02] Smooth
    FWHM = 2  # Full width half maximum of Gaussian kernel. In voxel size units.
    SIGMA = FWHM / 2.35482004503  # Convert to filter standard deviation
    wm = gaussian_filter(wm.astype(float), sigma=SIGMA, mode="reflect")
    wm = wm > 0.5

    # [Step-03] Erode (to go back to original white matter average thickness)
    wm = morphology.binary_erosion(wm, structure=struct, iterations=3)

    # -----------------------------------------------------------------------------
    # Separate white matter together with gray matter
    wmgm = data[..., slice] == GM
    wmgm = wmgm + wm

    # [Step-01] Erode (to keep kissing gyri as separate as possible)
    wmgm = morphology.binary_erosion(wmgm, structure=struct, iterations=3)

    # [Step-02] Smooth & re-binarize
    wmgm = gaussian_filter(wmgm.astype(float), sigma=SIGMA, mode="reflect")
    wmgm = wmgm > 0.5

    # [Step-03] Dilate (to go back to original outer gray matter average thickness)
    wmgm = morphology.binary_dilation(wmgm, structure=struct, iterations=3)

    # -----------------------------------------------------------------------------
    # Reform the segmentation file
    new_data[wmgm != 0, slice] = 3
    new_data[wm != 0, slice] = 2

# Trim padded elements
new_data = new_data[1:-1, 1:-1, 1:-1]

new_data[..., 0:22] = 0
new_data[..., 72:140] = 0
new_data[..., 191:302] = 0

# Save as nifti
SUFFIX = "2D_polished"
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(new_data.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_{}.{}".format(basename, SUFFIX, ext))

print("Finished. Don't forget the check the result carefully!.")
