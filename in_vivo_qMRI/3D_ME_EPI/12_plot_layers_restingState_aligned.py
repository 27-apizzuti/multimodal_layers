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
HEMI = 'RH'

MAIN_PATH = 'D:\\AHEAD_v2\\derivatives\\T2star_in-vivo\\03_layers\\{}'.format(HEMI)
nii = nb.load(os.path.join(MAIN_PATH, "sub-04_task-rest_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-02_BBR_mean_res2X_fixdim_reg-nonlin_{}_cut.nii.gz".format(HEMI)))
data_mat = np.asarray(nii.dataobj)
N_LAY = 21
TAG = 'intensity_{}'.format(str(N_LAY))
BINS = [100, 50, 100, 100]

# -----------------------------------
# USER's ENTRIES
# Metric file
nii = nb.load(glob(os.path.join(MAIN_PATH, "*_metric_equivol*"))[0])
metric = np.asarray(nii.dataobj)

# ROI file
nii = nb.load(glob(os.path.join(MAIN_PATH, "sub-01_visual_areas_hMT_plus_capsule_{}_bvbabel_ups2X_VORONOI_no_capsule_clean_cut.nii.gz".format(HEMI)))[0])
roi_mat = np.asarray(nii.dataobj)

# // Create output path
PATH_OUT = os.path.join(MAIN_PATH, 'Figure_{}_rest-01'.format(TAG))
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
        #layer_bins[i] = np.percentile(data_mat[(lay == i) * (idx_data)], 25)
    
    # Remove nan if exist
    layer_bins[np.isnan(layer_bins)] = 0 
    Layer_database[it_roi, :] = layer_bins
    layer_bins[1] = layer_bins[2]
    layer_bins[-1] = layer_bins[-2]
    
    # // mean
    mymax = 15000
    mymin = 4000
    
    # mymax = 1000
    # mymin = 200
    
    
    print(layer_bins)
    # // Plotting
    fig1, axs = plt.subplots(1, 1)
    mycmap = cmocean.cm.ice  
    mycmap = 'magma'                                                # cmocean.cm.ice, 'magma'
    # img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=500, cmap=mycmap, norm=mpl.colors.LogNorm(vmin=min_value, vmax=max_value))
    
    img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=[50, BINS[it_roi]], cmap=mycmap)
    cb = fig1.colorbar(img[-1], ax=axs)
    axs.set_xlabel("Normalized cortical depth", fontsize=20)
    axs.set_ylabel("wT2* [a.u.]", fontsize=20)
    axs.set_title('{}, fMRI mean '.format(roi), fontsize=22, pad=20)

    fig1.tight_layout()

    # Additional
    axs.set_ylim(mymin, mymax)

    axs.tick_params(axis='x',labelsize=16)
    axs.tick_params(axis='y',labelsize=16)
    x = np.linspace(0, 1, nr_layers+1)
    axs.plot(x[1:], layer_bins[1:], linewidth=4, color= 'white', linestyle='-')
    fig1.savefig(os.path.join(PATH_OUT, '{}_2D-Hist_restState_wT2star_{}_mean'.format(roi, HEMI)), bbox_inches='tight')

# Save numpy array: ROIS x CONTRAST x N_LAYERS
np.save(os.path.join(PATH_OUT, "ROI_{}_wT2star_vs_depth_{}_mean.npy".format(HEMI, N_LAY)), Layer_database)

