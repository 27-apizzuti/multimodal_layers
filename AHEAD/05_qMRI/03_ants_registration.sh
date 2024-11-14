#!/bin/bash
# Here we take the segmentation file from the microscopy data and try to fine tuned on the qMRI using non Linear Coregistration (Syn, by ANTs)
# A mask around the ROI is used to optimize the alignment.

echo "I expect 2 filed: target file (e.g. high-res T1w from VASO) and a moving (or source) file"
echo " Co-registration-part II: Source to Target ----> Syn [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# 1. microscopy --> qMRI R1 (similar contrast)
mydata=/mnt/d/AHEAD_v2/derivatives/122017/04_qMRI/LH/
myTarget=${mydata}/Ahead_brain_122017_MRI-quantitative-R1_LH_cut_STEDI_n10_s0pt5_r1pt0_g1.nii.gz
mySource=${mydata}/Ahead_brain_122017_LH_microscopy_stack_percentale_normalization_cut_STEDI_n10_s0pt5_r1pt0_g1.nii.gz
myMask=${mydata}/Ahead_brain_122017_MTatlas_capsule_LH_bvbabel_to_02_cut_VORONOI_nocapsule.nii.gz

outfld=${mydata}/alignment_ANTs_hMT

# Create output folder
if [ ! -d ${outfld} ]; then
  mkdir -p ${outfld};
fi

cd ${outfld}
#===========================================
echo "*****************************************"
echo "************* starting with ANTS ********"
echo "*****************************************"

antsRegistration \
--verbose 1 \
--dimensionality 3 \
--float 1 \
--output [${mydata}/registered_,${mydata}/registered_Warped.nii.gz,${mydata}/registered_InverseWarped.nii.gz] \
--interpolation BSpline[5] \
--use-histogram-matching 0 \
--winsorize-image-intensities [0.005,0.995] \
--transform Rigid[0.05] \
--metric MI[${myTarget},${mySource},0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--transform Affine[0.1] \
--metric MI[${myTarget},${mySource},0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--transform SyN[0.1,2,0] \
--metric MI[${myTarget},${mySource},1,2] \
--convergence [500x100,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
-x ${myMask}

# Apply to microscopy data
antsApplyTransforms -d 3 -i ${mySource} -o Ahead_brain_122017_LH_microscopy_stack_percentale_normalization_cut_brainmasked_STEDI_n10_s0pt5_r0pt5_g1_hMT_warped.nii.gz -r ${myTarget} -t ${mydata}/registered_1Warp.nii.gz -t ${mydata}/registered_0GenericAffine.mat

# Apply to segmentation file // Multilabel interpolation option is selected here
antsApplyTransforms -d 3 -i ${mydata}/Ahead_brain_122017_LH_RIM_polished_cut_43_93_2D_polished.nii.gz -o Ahead_brain_122017_LH_RIM_polished_cut_43_93_2D_polished_hMT_warped_ML.nii.gz -r ${mydata}/Ahead_brain_122017_MRI-quantitative-R1_LH_cut_STEDI_n10_s0pt5_r1pt0_g1.nii.gz -n MultiLabel -t ${mydata}/registered_1Warp.nii.gz -t ${mydata}/registered_0GenericAffine.mat
