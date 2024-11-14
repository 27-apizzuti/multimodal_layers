import numpy as np
import numpy as np
import nibabel as nb
import glob
import os

# # !!!! Left hemisphere !!!!
filenames = ["Ahead_brain_122017_microscopy_stack_percentale_normalization", "Ahead_brain_122017_LH_RIM_polished_ext",
"Ahead_brain_122017_LH_ROIs",  "Ahead_brain_122017_LH_microscopy_labels_offset", "122017_MTatlas_capsule_LH_bvbabel_to_02"]

filenames = [
"Ahead_brain_122017_LH_visAtlas-short_plus_capsule_bvbabel_to_02"]

cropDims = {'x':[464,933],
            'y':[36,620],
            'z': [558,860]}

tmpDims = f"{cropDims['x'][0]} {cropDims['x'][1]-cropDims['x'][0]} {cropDims['y'][0]} {cropDims['y'][1]-cropDims['y'][0]} {cropDims['z'][0]} {cropDims['z'][1]-cropDims['z'][0]}"
for it in filenames:
    file = '/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/Original_dimension/{}.nii.gz'.format(it)
    file_out = '/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/LH/CUT/{}_cut.nii.gz'.format(it)
    truncCommand = f'fslroi {file} {file_out} {tmpDims}'
    os.system(truncCommand)

# ------------------------------------
# # !!!! Right hemisphere !!!!!
filenames = ["Ahead_brain_122017_microscopy_stack_percentale_normalization", "Ahead_brain_122017_RH_RIM_polished",
"Ahead_brain_122017_RH_visAtlas-short_plus_capsule_bvbabel_to_02_VORONOI_nocapsule",  "Ahead_brain_122017_microscopy_labels_offset"]

filenames = [
"Ahead_brain_122017_RH_visAtlas-short_plus_capsule_bvbabel_to_02"]

# filenames = [
# "122017_MTatlas_capsule_RH_bvbabel_to_02"]

cropDims = {'x':[6, 493],
            'y':[67, 706],
            'z': [558, 860]}

tmpDims = f"{cropDims['x'][0]} {cropDims['x'][1]-cropDims['x'][0]} {cropDims['y'][0]} {cropDims['y'][1]-cropDims['y'][0]} {cropDims['z'][0]} {cropDims['z'][1]-cropDims['z'][0]}"

for it in filenames:
    file = '/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/RH/Original_dimension/{}.nii.gz'.format(it)
    file_out = '/mnt/d/AHEAD_v2/derivatives/122017/02_Segmentation/RH/CUT/{}_cut.nii.gz'.format(it)
    truncCommand = f'fslroi {file} {file_out} {tmpDims}'
    os.system(truncCommand)
