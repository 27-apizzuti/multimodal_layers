# Compute initial transformation matrix in ITK-SNAP and save it as .txt
# Compute warp field
greedy -d 3 -m NCC 4x4x4 -i sub-01_part-mag_ME3DEPI_crop_ups2X_prepped_reg_echo-mean.nii.gz sub-04_task-rest_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-02_BBR_mean_res2X_fixdim.nii.gz -it initial_transformation.txt -o /home/faruk/temp-ale_greedy2/warp.nii.gz -sv -n 100x50x10 -mm regmask_bin_ero.nii.gz

# Apply transformation
greedy -d 3 -rf sub-01_part-mag_ME3DEPI_crop_ups2X_prepped_reg_echo-mean.nii.gz -ri LINEAR -rm sub-04_task-rest_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-02_BBR_mean_res2X_fixdim.nii.gz sub-04_task-rest_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-02_BBR_mean_res2X_fixdim_reg-nonlin.nii.gz -r warp.nii.gz initial_transformation.txt
