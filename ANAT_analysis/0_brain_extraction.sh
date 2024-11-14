#!/bin/bash
# This script is used to extract the brain for MP2RAGE anatomy and to create a brainmask
# P04, P03, P02, P05, P06
# 1. Use INV2 to extract the brain --> skull stripped
# 2. Apply brain mask to UNI_reg 
# 3. Create a brain mask using AFNII
# 
SUBJ=sub-06
anat_inv2=${SUBJ}_acq-mp2rage_inv2.nii   # usually we want to use INV2 to do brain extraction
anat_uni=${SUBJ}_acq-mp2rage_UNI.nii	 # can be UNI or UNI_reg

pathIn=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat
mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/brain_extraction

#===========================================
# Create output folder
if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi

# bet ${pathIn}/${anat_inv2} ${mywork}/ss_f03_${anat_inv2} -m -R -f 0.03
fslmaths ${pathIn}/${anat_uni} -mas ${mywork}/ss_f03_${anat_inv2}.gz ${pathIn}/${SUBJ}_acq-mp2rage_UNI_ss.nii

# 2. Bias field correction
# cp ${pathIn}/${anat_uni} ./uncorr.nii
# /mnt/c/'Program Files'/MATLAB/R2020b/bin/matlab.exe -nodesktop -nosplash -r "run Bias_field_script_job.m"

# 3dAutomask -prefix ${pathIn}/T1w_preparation/mask.nii -peels 3 -dilate 2 -overwrite ${pathIn}/T1w_preparation/denoised_muncorr.nii
# defined in the 'fixed' image space, can be used later


# #-f 0.01 -r 65
# # T1 doesnt work
# # cd ${pathIn}
# fslmaths ${path2} -mas ${pathIn}/brain_extraction/ss_inv2_f03_mask.nii.gz ${pathIn}/sub-04_acq-mp2rage_UNI_reg_ss.nii
# path2=/mnt/d/Pilot_Exp_VASO/pilotAOM/sub-04/derivatives/func/loc01/alignment_ANTs
# antsApplyTransforms -d 3 -i ${path2}/Moving.nii -o ${path2}/warped_moved_warpMP2RAGE.nii -r ${path2}/Moving.nii -t ${pathIn}/registered_1Warp.nii.gz -t ${pathIn}/registered_0GenericAffine.mat -t ${path2}/registered_1Warp.nii.gz -t ${path2}/registered_0GenericAffine.mat 
# antsApplyTransforms -d 3 -i ${path2}/Moving.nii -o ${path2}/warped_moved__warpMP2RAGE_EPI.nii -r ${path2}/EPI.nii -t ${pathIn}/registered_1Warp.nii.gz -t ${pathIn}/registered_0GenericAffine.mat -t ${path2}/registered_1Warp.nii.gz -t ${path2}/registered_0GenericAffine.mat  

# antsApplyTransforms -d 3 -e 3 -i ${path2}/sub-04_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_undist.nii.gz -o ${path2}/warped_tserie_EPI.nii -r ${path2}/EPI.nii -t ${pathIn}/registered_1Warp.nii.gz -t ${pathIn}/registered_0GenericAffine.mat -t ${path2}/registered_1Warp.nii.gz -t ${path2}/registered_0GenericAffine.mat