"""
Created on Thu Oct 14 18:43:35 2021
    Get 2D histogram for each file
    Get overlayed layer profile across contrasts
        Input: metric file (from LN2_LAYERS), intensity values

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
ROIS = ['hMT', 'V1' ,'V2', 'V3']
HEMI = 'LH'

MAIN_PATH = 'D:\\AHEAD_v2\\derivatives\\T2star_in-vivo\\03_layers\\{}'.format(HEMI)
nii = nb.load(os.path.join(MAIN_PATH, "sub-01_part-mag_ME3DEPI_crop_ups2X_prepped_reg_T2s_{}_cut.nii.gz".format(HEMI)))
data_mat = np.asarray(nii.dataobj)
N_LAY = 3
TAG = 'intensity_{}'.format(str(N_LAY))
data_mat = (1 / data_mat) *1000
# data_mat[data_mat < 20] = 20
# data_mat[data_mat > 50] = 50

# -----------------------------------
# USER's ENTRIES
# Metric file
nii = nb.load(glob(os.path.join(MAIN_PATH, "*_metric_equivol*"))[0])
metric = np.asarray(nii.dataobj)

# ROI file
nii = nb.load(glob(os.path.join(MAIN_PATH, "*VORONOI_no_capsule_clean_cut*"))[0])
roi_mat = np.asarray(nii.dataobj)

# // Create output path
PATH_OUT = os.path.join(MAIN_PATH, 'Figure_{}_R2'.format(TAG))
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# // Initiate figure
my_dpi = 300
plt.style.use('dark_background')

# ----------------------------------
# ----------------------------------
Layer_database = np.zeros((len(ROIS), N_LAY+1))
# Plot starts here
for it_roi, roi in enumerate(ROIS):
    idx_roi = roi_mat == (it_roi + 1)

    # Compute layers
    layers = my_layer_profiles(metric, N_LAY)
    lay = np.reshape(layers, np.shape(metric))
    idx_layers = np.unique(layers)[1:]
    nr_layers = idx_layers.size
    layer_bins = np.zeros(nr_layers + 1)  # +1 for zeros indices

    # // Compute mean intensity for each layer
    idx_data = idx_roi
    for i in idx_layers:  # Compute bin averages
        i = int(i)
        layer_bins[i] = np.median(data_mat[(lay == i) * (idx_data)])

#     Layer_database[it_roi, :] = layer_bins
    print('Plot {}'.format(roi))
    print(layer_bins)
#     # // Plotting
#     fig1, axs = plt.subplots(1, 1)
#     # mycmap = cmocean.cm.ice
#     mycmap = 'magma'                                                # cmocean.cm.ice, 'magma'
#     # img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=500, cmap=mycmap, norm=mpl.colors.LogNorm(vmin=min_value, vmax=max_value))
#     img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=[50, 100], cmap=mycmap)
#     cb = fig1.colorbar(img[-1], ax=axs)
#     axs.set_xlabel("Normalized cortical depth", fontsize=20)
#     axs.set_ylabel("qR2* [s-1]", fontsize=20)
#     axs.set_title('{}, qR2*'.format(roi), fontsize=22, pad=20)
#
#     fig1.tight_layout()
#
#     # Compute slope: fit a line to the data
#     x = np.linspace(0, 1, nr_layers + 1)
#     y = layer_bins[1:]
#     slope, intercept = np.polyfit(x[1:], y, 1)  # Linear fit (degree 1)
#     print('Slope for {}: {}'.format(roi, slope))
#     fitted_line = slope * x[1:] + intercept
#     axs.plot(x[1:], fitted_line, color='red', linestyle='--', linewidth=2, label='Fitted Line')
#
#     # Additional
#     axs.set_ylim(10, 50)
#
#     axs.tick_params(axis='x',labelsize=16)
#     axs.tick_params(axis='y',labelsize=16)
#     x = np.linspace(0, 1, nr_layers+1)
#     axs.plot(x[1:], layer_bins[1:], linewidth=4, color= 'white', linestyle='-')
#     fig1.savefig(os.path.join(PATH_OUT, '{}_2D-Hist_qR2star_ice'.format(roi)), bbox_inches='tight')
#
#     # CBV estimate: additional Deep and Superficial Layers Laminar value
#     deep = np.mean([layer_bins[2], layer_bins[3], layer_bins[4]])
#     sup = np.mean([layer_bins[-2], layer_bins[-3], layer_bins[-4]])
#     print('{} Laminar profiles: {} {}'.format(roi, deep, sup))
#
# # Save numpy array: ROIS x CONTRAST x N_LAYERS
# np.save(os.path.join(PATH_OUT, "ROI_{}_qR2star_vs_depth_{}.npy".format(HEMI, N_LAY)), Layer_database)
