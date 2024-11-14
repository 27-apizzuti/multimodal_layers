# bet "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_MRI-proton-density_RH_cut.nii.gz" "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/head_brain_122017_MRI-proton-density_RH_cut_SS.nii.gz" -m -R -f 0.08

fslmaths "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_RH_RIM_polished_cut_22_72_3D_polished.nii.gz" -thr 2 -bin "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_RH_RIM_polished_cut_22_72_3D_polished_brainmask.nii.gz"

fslmaths "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_MRI-quantitative-R1_RH_cut.nii.gz" -mas "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_RH_RIM_polished_cut_22_72_3D_polished_brainmask_closed.nii.gz" "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_MRI-quantitative-R1_RH_cut_brainmask.nii.gz"

fast -n 3 -o "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_MRI-quantitative-R1_RH_cut_brainmask.nii.gz" "/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/Ahead_brain_122017_MRI-quantitative-R1_RH_cut_brainmask.nii.gz"
