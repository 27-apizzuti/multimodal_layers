# Run LN2_LAYERS to get streamlines --> cutting angle computation
#// RH
# LN2_RIM_POLISH -rim /mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/RH/02/Ahead_brain_122017_RH_RIM_polished_cut_141_190_and_22_72_warped_2D_polished_final.nii.gz

LN2_LAYERS -rim /mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/RH/02/Ahead_brain_122017_RH_RIM_polished_cut_141_190_and_22_72_warped_2D_polished_final_polished.nii.gz -equivol -streamlines

LN2_LAYERS -rim /mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/02_segmentation/Ahead_brain_122017_LH_RIM_polished_cut_43_93_121_171_2D_polished_warped_ML_manual_faruk_polished.nii.gz -equivol -streamlines
