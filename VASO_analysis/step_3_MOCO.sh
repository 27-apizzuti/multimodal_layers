#!/bin/bash
echo "Starting MOCO.sh (bash script)"
# This script is used for both NORDIC and not NORDIC preprocessed data.
#
# Run P04: NORDIC[vaso_analysis/magn_phase--/vaso_analysis/magn_only]--REF.[/vaso_analysis/no_nordic]
# Run P03: NORDIC[vaso_analysis/magn_phase--/vaso_analysis/magn_only]--REF.[/vaso_analysis/no_nordic] & magn_phasenoNOISE
# Run P02: NORDIC[vaso_analysis/magn_only--REF.[/vaso_analysis/no_nordic]
# Run P05: REF.[/vaso_analysis/no_nordic]

SUBJ=sub-05

# NORDIC
path_der_in=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/NORDIC/output/magn_phase
path_der_out=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/magn_phase/moco

# REFERENCE
# path_der_in=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/sourcedata/session1/NIFTI/func/vaso
# path_der_out=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/moco

path_brainmask=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/brainmask

myscript=/mnt/d/Pilot_Exp_VASO/AOM-project/VASO_analysis

#===========================================
echo "Data folder: " ${path_der_in}
echo "Working folder: " ${path_der_out}

# Create output folder
if [ ! -d ${path_der_out} ]; then
  mkdir -p ${path_der_out};
fi


cd ${path_der_out} 	# remain in this folder
cnt=0
for filename in ${path_der_in}/N*.nii   ##### Change with N*.nii with NODIC data; s*.nii with no NORDIC
do
cp $filename ./Basis_${cnt}a.nii

3dTcat -prefix Basis_${cnt}a.nii Basis_${cnt}a.nii'[4..7]' Basis_${cnt}a.nii'[4..$]' -overwrite

cp ./Basis_${cnt}a.nii ./Basis_${cnt}b.nii

3dinfo -nt Basis_${cnt}a.nii >> NT.txt
3dinfo -nt Basis_${cnt}b.nii >> NT.txt
cnt=$(($cnt+1))
echo run $cnt

done
# copy the mask for motion correction
cp ${path_brainmask}/mask.nii .
mv mask.nii moma.nii

# copy the matlab script
cp ${myscript}/mocobatch_VASO_flex.m .
echo "Starting mocobatch_VASO_flex.m (matlab script)"
/mnt/c/'Program Files'/MATLAB/R2020b/bin/matlab.exe -nodesktop -nosplash -r "run mocobatch_VASO_flex.m"
