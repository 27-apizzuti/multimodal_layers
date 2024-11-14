"""Use LN2_LAYERS -steamlines output to compute CUT angular differences."""

import os
import numpy as np
import nibabel as nb

# Vector file
# STREAMLINES = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_streamline_vectors.nii.gz"
#
# MIDGM = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_midGM_equidist.nii.gz"
# Output directory
# OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT"

STREAMLINES = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/temp/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_4figure_176_streamline_vectors.nii.gz"

MIDGM = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/temp/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_4figure_176_midGM_equidist.nii.gz"

OUTDIR = "/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/temp"


# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Load midGM Nifti1Image
nii = nb.load(MIDGM)
midGM = np.asarray(nii.dataobj)
dims = np.shape(midGM)
new = [0, 0, 1]
idx = (midGM !=0)

# Load vector nifti
nii = nb.load(STREAMLINES)
vec_local = np.asarray(nii.dataobj)

# Prepare 4D nifti (3 elements on 4th axis determine 3D vector per voxel)
vec_CUT = np.zeros(dims + (3,), dtype=np.float32)
vec_CUT[idx, 0] = new[0]
vec_CUT[idx, 1] = new[1]
vec_CUT[idx, 2] = new[2]

# Save
filename = os.path.basename(MIDGM)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_CUTvector.{}".format(basename, ext))
img = nb.Nifti1Image(vec_CUT, affine=nii.affine, header=nii.header)
nb.save(img, outname)

# Compute angular difference between two 3D vectors at every voxel.
term1 = np.sqrt(np.sum(vec_CUT**2., axis=-1))
term2 = np.sqrt(np.sum(vec_local**2., axis=-1))
temp_dot = np.sum(vec_CUT * vec_local, axis=-1)
temp_angle = np.arccos(temp_dot / (term1 * term2))

# Convert radians to degrees
temp_angle = temp_angle * 180 / np.pi

temp_angle[~idx] = 0
temp_angle[np.isnan(temp_angle)] = 0

# Save
filename = os.path.basename(STREAMLINES)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_CUTangdif.{}".format(basename, ext))
img = nb.Nifti1Image(temp_angle, affine=nii.affine, header=nii.header)
nb.save(img, outname)

print("Finished.")

# Set a threshold
THR = 60        # deviation from 90°, perfect cutting angle
idx_good_slices = (temp_angle > 90-THR) & (temp_angle < 90+THR)

seg_slices = np.zeros(dims, dtype=np.int8)
seg_slices[idx_good_slices] = 1

filename = os.path.basename(STREAMLINES)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_SEG_slices.{}".format(basename, ext))
img = nb.Nifti1Image(seg_slices, affine=nii.affine, header=nii.header)
nb.save(img, outname)
