"""
Select a subset of 'optimal slices'. Split input 3D to separate 2D.
# !!!!! The selection of slices is done after FSLROI !!!!!!!

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from glob import glob

# -----------------------------------
# USER's ENTRIES
# // LH
# Ahead_brain_122017_LH_RIM_polished_cut_43_93_2D_polished.nii.gz --> segmentation filename
# V1, V2, V3
OFFSET = 558; EXCL_SLIDES = [577-OFFSET, 597-OFFSET, 666-OFFSET, 700-OFFSET, 754-OFFSET];
SLICES = [127, 177]

# hMT+
# OFFSET = 558; EXCL_SLIDES = [615-OFFSET, 621-OFFSET, 622-OFFSET];
# SLICES = [43, 93]

# FILES = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/Ahead_brain_122017_LH_microscopy_stack_percentale_normalization_cut.nii.gz",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/Ahead_brain_122017_LH_microscopy_labels_offset_cut.nii.gz",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/Ahead_brain_122017_MTatlas_capsule_LH_bvbabel_to_02_cut_VORONOI_nocapsule.nii.gz",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_streamline_vectors_CUTangdif.nii.gz",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/Ahead_brain_122017_LH_RIM_polished_cut_43_93_2D_polished.nii.gz"]

# OUTDIR = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/01_2D_VALUES",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/01_2D_MICR_LAB",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/01_2D_ROIS",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/01_2D_ANGLES",
# "/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/hMT/01_2D_RIMS"]

# ---------------------------------------------------------------------------------
# // RH
# Ahead_brain_122017_LH_RIM_polished_cut_22_72_2D_polished.nii.gz --> segmentation filename
V1, V2, V3
OFFSET = 558; EXCL_SLIDES = [577-OFFSET, 597-OFFSET, 666-OFFSET, 754-OFFSET, 703-OFFSET, 706-OFFSET, 719-OFFSET, 725-OFFSET, 728-OFFSET, 743-OFFSET];
SLICES = [141, 191]

# hMT+
OFFSET = 558; EXCL_SLIDES = [597-OFFSET];
SLICES = [22, 72]
# Ahead_brain_122017_MTatlas_capsule_RH_bvbabel_to_02_cut_VORONOI_nocapsule.nii.gz --> ROI filename

FILES = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/Ahead_brain_122017_LH_microscopy_stack_percentale_normalization_cut.nii.gz",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/Ahead_brain_122017_microscopy_labels_offset_cut.nii.gz",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/Ahead_brain_122017_LH_visAtlas-short_plus_capsule_bvbabel_to_02_cut_VORONOI_nocapsule.nii.gz",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/Ahead_brain_122017_LH_RIM_polished_cut_43_93_3D_polished_streamline_vectors_CUTangdif.nii.gz",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/Ahead_brain_122017_LH_RIM_polished_cut_43_93_2D_polished.nii.gz"]

OUTDIR = ["/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_VALUES",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_MICR_LAB",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_ROIS",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_ANGLES",
"/mnt/d/AHEAD_v2/derivatives/122017/03_Layers/LH/V1_V2_V3/01_2D_RIMS"]


for it, nifti in enumerate(FILES):
    filename = nifti.split('/')[-1]
    print(filename)
    basename, ext = filename.split(os.extsep, 1)
    print('Split 3D into 2D for: {}'.format(basename))

    # Create output directory
    if not os.path.exists(OUTDIR[it]):
        os.mkdir(OUTDIR[it])

    base_output = OUTDIR[it].split('/')[-1]

    if (base_output == "01_2D_RIMS"):
        OUTDIR_GM = os.path.join(OUTDIR[it], "2D_GM")
        if not os.path.exists(OUTDIR_GM):
            os.mkdir(OUTDIR_GM)

    # Open NIFTI
    nii = nb.load(nifti)
    data = np.asarray(nii.dataobj)
    datatype = nii.header.get_data_dtype()

    dims = np.shape(data)
    pad = np.zeros((dims[0], dims[1], 1), dtype=datatype)

    for itslice in range(SLICES[0], SLICES[-1]):

        if itslice in EXCL_SLIDES:
            print('Excluded slice')
        else:
            pad = data[..., itslice-1, None]
            numb = str(itslice).zfill(3)

            new_data = nb.Nifti1Image(pad, header=nii.header, affine=nii.affine)
            nb.save(new_data, os.path.join(OUTDIR[it], "{}_{}.nii.gz".format(basename, numb)))

            if (base_output == "01_2D_RIMS"):
                idx = pad < 3
                pad[idx] = 0
                pad[pad == 3] = 1

                # save
                new_data = nb.Nifti1Image(pad, header=nii.header, affine=nii.affine)
                nb.save(new_data, os.path.join(OUTDIR_GM, "{}_GM_{}.nii.gz".format(basename, numb)))


print("Finished")
