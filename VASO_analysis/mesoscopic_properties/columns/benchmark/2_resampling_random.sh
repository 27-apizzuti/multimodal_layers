#!/bin/bash
# Upsample random data
SUBJ=sub-06
NII=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/random_columns/${SUBJ}_leftMT_Sphere16radius_random.nii.gz
OUTPUT_NII=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/random_columns/${SUBJ}_leftMT_Sphere16radius_random_upsampled.nii.gz
thr=4

# 1. Upsample > find the paramenters
delta_x=$(3dinfo -di $NII)
delta_y=$(3dinfo -dj $NII)
delta_z=$(3dinfo -dk $NII)
echo "Starting pixel resolution: " $delta_x $delta_y $delta_z
sdelta_x=$(echo "((sqrt($delta_x * $delta_x) / ${thr}))"|bc -l)
sdelta_y=$(echo "((sqrt($delta_y * $delta_y) / ${thr}))"|bc -l)
sdelta_z=$(echo "((sqrt($delta_z * $delta_z) / ${thr}))"|bc -l)
echo "Find upsampling parameters: " $sdelta_x $sdelta_y $sdelta_z

delta_x=$(3dinfo -di $NII)
delta_y=$(3dinfo -dj $NII)
delta_z=$(3dinfo -dk $NII)

3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix $OUTPUT_NII -input $NII
