"""Quick way of extracting a subset of voxels from a nifti image."""

import os
import nibabel as nb
import numpy as np

FILE1 = "/mnt/d/AHEAD_v2/derivatives/restingState/GREEDY/sub-04_task-rest_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-02_BBR_mean_res2X.nii.gz"
FILE2 = "/mnt/d/AHEAD_v2/derivatives/restingState/GREEDY/sub-01_part-mag_MP2RAGE_uni_beta-20_CURED_n5_s0pt5_r1pt0_g1_masked_stitched_composite-max07_reg_to_T2star_ups2X_crop.nii.gz"

# =============================================================================
print("  Loading nifti...")
nii1 = nb.load(FILE1)
data = np.asarray(nii1.dataobj)

print("  Mirror over L-R...")
data = data[::-1, :, :]

print("  Fix header...")
nii2 = nb.load(FILE2)
basename, ext = FILE1.split(os.extsep, 1)
temp = np.copy(nii2.affine)
temp[0, 0] *= 2.0
temp[1, 1] *= 2.0
temp[2, 2] *= 2.0
temp[3, 3] *= 2.0
print(temp)

print("  Saving...")
out = nb.Nifti1Image(data, affine=temp, header=nii1.header)
# (Optional fix header voxel size)
out.header["pixdim"][1] = 0.35  # mm
out.header["pixdim"][2] = 0.35  # mm
out.header["pixdim"][3] = 0.35  # mm
nb.save(out, "{}_fixdim.{}".format(basename, ext))

print("Finished.")
