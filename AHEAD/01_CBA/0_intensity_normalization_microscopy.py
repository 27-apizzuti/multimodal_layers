"""Intensity normalization for 3D model using percentale"""

import nibabel as nb
import numpy as np
import os
import matplotlib.pyplot as plt


# Nifti reference
nii = nb.load("/mnt/d/AHEAD_v2/Ahead_brain_122017-3D_reconstructions/Ahead_brain_122017_stacked-microscopy-slices.nii.gz")
data = np.asarray(nii.dataobj)
data[np.isnan(data)] = 0
print("Original data type: {}".format(data.dtype))

# Load brainmask
nii2 = nb.load("/mnt/d/AHEAD_v2/Ahead_brain_122017-3D_reconstructions/brainmask_smoothed.nii.gz")
mask = np.asarray(nii2.dataobj, dtype=np.int8)
print("Mask data type: {}".format(mask.dtype))
data[mask != 1] = 0

dims = np.shape(data)
new_data = np.zeros(dims, dtype=data.dtype)

print("Normalization...")
for itslice in range(0, dims[-1]):

    # Just for testing on one slice
    data1 = data[..., itslice]
    idx = data1 != 0

    if (np.sum(idx)) > 0:
        # Percentale
        v_min, v_max = np.percentile(data1[idx], [5, 95])

        new_data[..., itslice] = (data1 - v_min) / (v_max - v_min)

  
# Save Nifti
print("Save...")
new_data[mask != 1] = 0
print("Normalized data type: {}".format(new_data.dtype))

out = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
nb.save(out, "/mnt/d/AHEAD_v2/Ahead_brain_122017-3D_reconstructions/Ahead_brain_122017_stacked-microscopy-slices_percentale_norm.nii.gz")
