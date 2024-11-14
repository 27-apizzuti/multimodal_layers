"""Polish manually edited MRI white & gray matter segmentations."""

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

# Segmentation file
FILE = "/mnt/d/AHEAD_v2/derivatives/122017/Segmentation/Ahead_brain_122017_cruise-left-cortex_binarized_plus_GM_v-10.nii.gz"
SLICES = [570, 850]

# Integer labels for tissue classes
WM = 2
GM = 1

# =============================================================================
# Load data
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)
data = np.pad(data, 1, mode="reflect")  # to prevent data edge artifacts
# -----------------------------------------------------------------------------
new_data = np.zeros(np.shape(data))
print('New data dims: {}'.format(np.shape(new_data)))

# // Iterate across SLICES
slice_range = np.arange(SLICES[0], SLICES[1]+1) # include the 850
print('Slice range: {}'.format(slice_range))
print('Number of slices: {}'.format(np.shape(slice_range)))

for slice in slice_range:
    print("Working on slice: {}".format(slice))
    # Separate white matter
    wm = data[..., slice] == WM

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
    # Separate white matter toether with gray matter
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

# Save as nifti
SUFFIX = "polished_sigma2"
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(new_data.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_{}.{}".format(basename, SUFFIX, ext))

print("Finished. Don't forget the check the result carefully!.")
