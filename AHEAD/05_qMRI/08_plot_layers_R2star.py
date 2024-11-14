"""
Plot layer profile, R2*

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
MAIN_PATH = 'D:\\AHEAD_v2\\derivatives\\122017\\04_qMRI\\LH'
CONTRAST = ['Ahead_brain_122017_MRI-quantitative-R2star_LH_cut.nii.gz']
CONTRAST_LABELS = ['R2star']
N_LAY = 3
ANGLE_THR = 60
MIN_MAX= [[10, 50]]
TAG = 'intensity_{}_R2star'.format(str(N_LAY))
# -----------------------------------
# USER's ENTRIES
# Metric file
nii = nb.load(glob(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "*_metric_equivol_*3D_stack.nii"))[0])
metric = np.asarray(nii.dataobj)
idx_metric = metric > 0

# ROI file
nii = nb.load(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "Ahead_brain_122017_LH_MTatlas_V1V2V3_VORONOI_nocapsule.nii.gz"))
roi_mat = np.asarray(nii.dataobj)
ROIS = ['hMT', 'V1', 'V2', 'V3']

# Bubble mask
nii = nb.load(glob(os.path.join(MAIN_PATH, "01_remove_bubble", "Ahead_brain_122017_segmentation_bubble_LH_closed.nii.gz"))[0])
bubble = np.asarray(nii.dataobj)
idx_buble = bubble == 0

# Cutting angle
nii = nb.load(glob(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "*CUTangdif_voronoi.nii.gz"))[0])
cutangle = np.asarray(nii.dataobj)
idx_cut = (cutangle > (90 - ANGLE_THR)) * (cutangle < (90 + ANGLE_THR))

# // Create output path
PATH_OUT = os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", 'Figure_{}'.format(TAG))
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# // Initiate figure
my_dpi = 300
plt.style.use('dark_background')
# ----------------------------------
# Plot starts here
for it_contr, contr in enumerate(CONTRAST):

    # // Load qMRI data
    nii = nb.load(os.path.join(MAIN_PATH, "{}".format(contr)))
    data_mat = np.asarray(nii.dataobj)

    for it_roi, roi in enumerate(ROIS):
        idx_roi = roi_mat == (it_roi + 1)

        # // Compute layers
        layers = my_layer_profiles(metric, N_LAY)
        lay = np.reshape(layers, np.shape(metric))
        idx_layers = np.unique(layers)[1:]
        nr_layers = idx_layers.size
        layer_bins = np.zeros(nr_layers + 1)  # +1 for zeros indices

        # // Compute mean intensity for each layer
        idx_data = idx_roi * idx_cut * idx_buble * idx_metric
        new_data = np.zeros(np.shape(idx_data))
        new_data[idx_data] = 1
        outname = os.path.join(PATH_OUT, 'Mask_{}_{}'.format(roi, CONTRAST_LABELS[it_contr]))

        for i in idx_layers:  # Compute bin averages
            i = int(i)
            layer_bins[i] = np.median(data_mat[(lay == i) * (idx_data)])

        # // Plotting

        print('Plot {} for {}'.format(roi, CONTRAST_LABELS[it_contr]))
        print(layer_bins)
        # fig1, axs = plt.subplots(1, 1)
        # # mycmap = cmocean.cm.ice  # right hemiphere
        # mycmap = 'magma'       # left hemisphre                                         #
        # img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=100, cmap=mycmap)
        # cb = fig1.colorbar(img[-1], ax=axs)
        # axs.set_xlabel("Normalized cortical depth", fontsize=20)
        # axs.set_ylabel("qR2* [s-1]", fontsize=20)
        # axs.set_title('{}, qR2*'.format(roi), fontsize=22, pad=20)
        #
        # fig1.tight_layout()
        #
        # # Compute slope: fit a line to the data
        # x = np.linspace(0, 1, nr_layers + 1)
        # y = layer_bins[1:]
        # slope, intercept = np.polyfit(x[1:], y, 1)  # Linear fit (degree 1)
        # print('Slope for {} {}: {}'.format(roi, CONTRAST_LABELS[it_contr], slope))
        # fitted_line = slope * x[1:] + intercept
        # axs.plot(x[1:], fitted_line, color='red', linestyle='--', linewidth=2, label='Fitted Line')
        #
        # # Additional
        # mima = MIN_MAX[it_contr]
        # axs.set_ylim(mima[0], mima[1])
        # axs.tick_params(axis='x',labelsize=16)
        # axs.tick_params(axis='y',labelsize=16)
        # x = np.linspace(0, 1, nr_layers+1)
        # axs.plot(x[1:], layer_bins[1:], linewidth=4, color= 'white', linestyle='-')
        # fig1.savefig(os.path.join(PATH_OUT, '{}_2D-Hist_{}_ice'.format(roi, CONTRAST_LABELS[it_contr])), bbox_inches='tight')
        #
        # # CBV estimate: additional Deep and Superficial Layers Laminar value
        # deep = np.mean([layer_bins[2], layer_bins[3], layer_bins[4]])
        # sup = np.mean([layer_bins[-2], layer_bins[-3], layer_bins[-4]])
        # print('{} Laminar profiles: {} {}'.format(roi, deep, sup))
        #
        # # Save mask
        # print('Save mask {} for {}'.format(roi, CONTRAST_LABELS[it_contr]))
        # new_data2 = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
        # nb.save(new_data2, outname)
