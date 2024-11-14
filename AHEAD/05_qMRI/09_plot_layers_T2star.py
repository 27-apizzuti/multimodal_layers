"""
Plot layer profile, T2*

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
HEMI = 'RH'
MAIN_PATH = 'D:\\AHEAD_v2\\derivatives\\122017\\04_qMRI\\{}'.format(HEMI)
CONTRAST = ['Ahead_brain_122017_MRI-quantitative-R2star_{}_cut.nii.gz'.format(HEMI)]
CONTRAST_LABELS = ['T2star']
N_LAY = 21
ANGLE_THR = 60
thr_min = 20
thr_max = 80
TAG = 'intensity_{}'.format(str(N_LAY))
# -----------------------------------
# USER's ENTRIES
# Metric file
nii = nb.load(glob(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "*_metric_equivol_*3D_stack.nii"))[0])
metric = np.asarray(nii.dataobj)
idx_metric = metric > 0

# ROI file
nii = nb.load(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "Ahead_brain_122017_{}_MTatlas_V1V2V3_VORONOI_nocapsule.nii.gz".format(HEMI)))
roi_mat = np.asarray(nii.dataobj)
ROIS = ['hMT', 'V1', 'V2', 'V3']

# Bubble mask
nii = nb.load(glob(os.path.join(MAIN_PATH, "01_remove_bubble", "Ahead_brain_122017_segmentation_bubble_{}_closed.nii.gz".format(HEMI)))[0])
bubble = np.asarray(nii.dataobj)
idx_buble = bubble == 0

# Cutting angle
nii = nb.load(glob(os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", "*CUTangdif_voronoi.nii.gz"))[0])
cutangle = np.asarray(nii.dataobj)
idx_cut = (cutangle > (90 - ANGLE_THR)) * (cutangle < (90 + ANGLE_THR))

# // Create output path
PATH_OUT = os.path.join(MAIN_PATH, "03_Layers", "03_PLOT_LAYER_PROFILES", 'Figure_{}_{}'.format(TAG, CONTRAST_LABELS[0]))
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
    data_mat_raw = nii.get_fdata()
    data_mat_raw[data_mat_raw < 1 ] = 1
    data_mat_raw[data_mat_raw > 100 ] = 100

    # data_mat[data_mat == 0] = np.nan
    # R2star -> T2star
    idx = (data_mat_raw !=1)
    data_mat = np.zeros(np.shape(data_mat_raw), dtype=np.float32)

    values = (1. / data_mat_raw[idx])*1000
    data_mat[idx] = values
    data_mat[data_mat > thr_max] = 0
    data_mat[data_mat < thr_min] = 0
    idx_non_zeros = data_mat !=0

    outname = os.path.join(PATH_OUT, '{}'.format(CONTRAST_LABELS[it_contr]))
    test = nb.Nifti1Image(data_mat, header=nii.header, affine=nii.affine)
    test.set_data_dtype(data_mat.dtype)
    nb.save(test, outname)

    for it_roi, roi in enumerate(ROIS):
        idx_roi = roi_mat == (it_roi + 1)

        # // Compute layers
        layers = my_layer_profiles(metric, N_LAY)
        lay = np.reshape(layers, np.shape(metric))
        idx_layers = np.unique(layers)[1:]
        nr_layers = idx_layers.size
        layer_bins = np.zeros(nr_layers + 1)  # +1 for zeros indices

        # // Compute mean intensity for each layer
        idx_data = idx_roi * idx_cut * idx_buble * idx_metric *idx_non_zeros
        new_data = np.zeros(np.shape(idx_data))
        new_data[idx_data] = 1
        outname = os.path.join(PATH_OUT, 'Mask_{}_{}'.format(roi, CONTRAST_LABELS[it_contr]))


        for i in idx_layers:  # Compute bin averages
            i = int(i)
            layer_bins[i] = np.median(data_mat[(lay == i) * (idx_data)])

        # // Plotting
        print('Plot {} for {}'.format(roi, CONTRAST_LABELS[it_contr]))
        fig1, axs = plt.subplots(1, 1)
        mycmap = 'magma'
        # if HEMI == 'LH':
        #     mycmap = 'magma'
        # else:
            # mycmap = cmocean.cm.ice  # right hemiphere
        #       # left hemisphre                                         # cmocean.cm.ice, 'magma'
        # img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=100, cmap=mycmap, norm=mpl.colors.LogNorm(vmin=min_value, vmax= max_value))
        img = axs.hist2d(metric[idx_data], data_mat[idx_data], bins=100, cmap=mycmap)
        cb = fig1.colorbar(img[-1], ax=axs)
        axs.set_xlabel("Normalized cortical depth", fontsize=20)
        axs.set_ylabel("qT2* [ms]", fontsize=20)
        axs.set_title('{}, qT2* '.format(roi, CONTRAST_LABELS[it_contr], fontsize=22, pad=20))

        fig1.tight_layout()

        # Additional
        # mima = MIN_MAX[it_contr]
        axs.set_ylim(thr_min, thr_max)
        axs.tick_params(axis='x',labelsize=16)
        axs.tick_params(axis='y',labelsize=16)
        x = np.linspace(0, 1, nr_layers+1)
        axs.plot(x[1:], layer_bins[1:], linewidth=4, color= 'white', linestyle='-')
        fig1.savefig(os.path.join(PATH_OUT, '{}_2D-Hist_{}_ice'.format(roi, CONTRAST_LABELS[it_contr])), bbox_inches='tight')

        # Save mask
        print('Save mask {} for {}'.format(roi, CONTRAST_LABELS[it_contr]))
        new_data2 = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
        nb.save(new_data2, outname)
