"""
Plot layer profile

NB: Few input files need to be correctly manually set (indicated by !!!)

@author: apizz
"""
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import cmocean
from glob import glob
import pathlib
from my_layer_profiles import *

# -----------------------------------
HEMI = 'LH'
ROIS = ['V1' ,'V2', 'V3']      # hMT is in a separate folder
MAIN_PATH = 'D:\\AHEAD_v2\\derivatives\\122017\\03_Layers\\{}\\V1_V2_V3\\10_PLOT_LAYER_PROFILES'.format(HEMI)    # !!! if hMT, replace V1_V2_V3 with hMT

nii = nb.load(glob(os.path.join(MAIN_PATH, "*_median_filt_LP_UVD_median_filter_bias_corrected_3D_stack.nii"))[0])
data_mat = np.asarray(nii.dataobj)
N_LAY = 21
ANGLE_THR = 60
TAG = 'intensity_{}'.format(str(N_LAY))
# -----------------------------------
# USER's ENTRIES
# Metric file
nii = nb.load(glob(os.path.join(MAIN_PATH, "*_metric_equivol_*3D_stack.nii"))[0])
metric = np.asarray(nii.dataobj)

# ROI file
nii = nb.load(glob(os.path.join(MAIN_PATH, "*VORONOI_*3D_stack.nii"))[0]) # !!! if hMT, replace with the correct file below
# nii = nb.load(os.path.join(MAIN_PATH, "Ahead_brain_122017_hMT_ROI.nii"))
roi_mat = np.asarray(nii.dataobj)

# Microscopy label
nii = nb.load(glob(os.path.join(MAIN_PATH, "*_microscopy_labels_*3D_stack.nii"))[0])
miclab = np.asarray(nii.dataobj)
MICRS = ['Bielschowsky', 'Thionin', 'Parvalbumin']

# Cutting angle
nii = nb.load(glob(os.path.join(MAIN_PATH, "*ang*_3D_stack.nii"))[0])
cutangle = np.asarray(nii.dataobj)
idx_cut = (cutangle > (90 - ANGLE_THR)) * (cutangle < (90 + ANGLE_THR))
# idx_cut = cutangle != 0

# // Create output path
PATH_OUT = os.path.join(MAIN_PATH, 'Figure_{}'.format(TAG))
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# // Initiate figure
my_dpi = 300
plt.style.use('dark_background')
min_value = 1
max_value = 500
# ----------------------------------
# ----------------------------------
Layer_database = np.zeros((len(ROIS), len(MICRS), N_LAY+1))
# Plot starts here
for it_roi, roi in enumerate(ROIS):
    if roi == 'hMT':
        idx_roi = roi_mat == (it_roi + 1)

    else:
        idx_roi = roi_mat == (it_roi + 2)

    for it_micr, micr in enumerate(MICRS):
        idx_micr = miclab == (it_micr + 1)

        # Compute layers
        layers = my_layer_profiles(metric, N_LAY)
        lay = np.reshape(layers, np.shape(metric))
        idx_layers = np.unique(layers)[1:]
        nr_layers = idx_layers.size
        layer_bins = np.zeros(nr_layers + 1)  # +1 for zeros indices

        # // Compute mean intensity for each layer
        idx_data = idx_roi * idx_micr * idx_cut
        for i in idx_layers:  # Compute bin averages
            i = int(i)
            layer_bins[i] = np.median(data_mat[(lay == i) * (idx_data)])

        Layer_database[it_roi, it_micr, :] = layer_bins

        print(layer_bins)
        # // Plotting
        fig1, axs = plt.subplots(1, 1)
        # mycmap = cmocean.cm.ice
        mycmap = 'magma'                                                # cmocean.cm.ice, 'magma'
        img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=100, cmap=mycmap, norm=mpl.colors.LogNorm(vmin=min_value, vmax= max_value))
        cb = fig1.colorbar(img[-1], ax=axs)
        axs.set_xlabel("Normalized cortical depth", fontsize=20)
        axs.set_ylabel("Voxel intensity", fontsize=20)
        axs.set_title('{}, {} ({})'.format(roi, micr, str(it_micr+1)), fontsize=22, pad=20)

        fig1.tight_layout()

        # Additional
        axs.set_ylim(0.5, 1.5)

        axs.tick_params(axis='x',labelsize=16)
        axs.tick_params(axis='y',labelsize=16)
        x = np.linspace(0, 1, nr_layers+1)
        axs.plot(x[1:], layer_bins[1:], linewidth=4, color= 'white', linestyle='-')
        fig1.savefig(os.path.join(PATH_OUT, '{}_2D-Hist_{}_ice'.format(roi, micr)), bbox_inches='tight')

# Save numpy array: ROIS x CONTRAST x N_LAYERS
np.save(os.path.join(PATH_OUT, "V1_V2_V3_{}_Biel_Thion_Parv_vs_depth_{}.npy".format(HEMI, N_LAY)), Layer_database) # !!!! Change if hMT is selected
