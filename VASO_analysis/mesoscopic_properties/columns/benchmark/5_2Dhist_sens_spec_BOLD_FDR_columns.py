"""
Created on Mon Oct 10 16:34:07 2022

Compute sesnitivity/specificity scatterplot for the BOLF_FDR mask extended to the whole cortical depth.

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
PATH_OUT = "D:\\Pilot_Exp_VASO\\pilotAOM\\Results\\Control_Columns"

FUNC = ['BOLD', 'VASO']
MASK = 'BOLD_FDR'

my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi), subplot_kw=dict(box_aspect=1),
                    dpi=my_dpi)
# plt.style.use('dark_background')
n_bins = [50, 50]

myCMAX = [250, 160, 150, 150, 150]

for isu, su in enumerate(SUBJ):
    print("Processing {}".format(su))
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'masks')
    PATH_MAP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'maps')

    for ifu, fu in enumerate(FUNC):
        
        # File definitions
        FILE1 = "{}_leftMT_Sphere16radius_BOLD_FDR_mask_scaled_4_full_depth_UVD_max_filter.nii.gz".format(su)
        FILE2 = "{}_leftMT_Sphere16radius_{}_sensitivity_map_scaled_4.nii.gz".format(su, fu)
        FILE3 = "{}_leftMT_Sphere16radius_{}_specificity_map_scaled_4.nii.gz".format(su, fu)
        
        # Loading
        nii1 = nb.load(os.path.join(PATH_MASK, FILE1))
        mask = nii1.get_fdata()

        nii2 = nb.load(os.path.join(PATH_MAP, FILE2))
        sen_map = nii2.get_fdata()

        nii3 = nb.load(os.path.join(PATH_MAP, FILE3))
        sp_map = nii3.get_fdata()
        
        # Find index inside the mask
        idx = mask > 0
        
        # Plotting
        vox_sens = sen_map[idx]
        vox_spec = sp_map[idx]
        # im = axs[ifu, isu].hist2d(vox_sens,
        #                   vox_spec, cmap='Greys', bins=n_bins, vmin=0, vmax=myCMAX[isu])
        im = axs[ifu, isu].hist2d(vox_sens,
                          vox_spec, cmap='Greys', bins=n_bins)
        vmin, vmax = im[-1].get_clim()
        axs[ifu, isu].set_ylabel("Specificity", fontsize=18)
        axs[ifu, isu].set_xlabel("Sensitivity", fontsize=18)
        axs[ifu, isu].set_ylim([0, 1])
        axs[ifu, isu].set_xlim([0, 30])
        axs[ifu, isu].grid("True")
        axs[ifu, isu].set_title("{} {} {}".format(su, fu, vmax))
        cb = fig.colorbar(im[-1], ax=axs[ifu, isu], pad=0.03, shrink=0.5)
        
fig_filename = "All_sbj_Columns_Voxel_Characterization_squared"
fig.tight_layout()
plt.savefig(os.path.join(PATH_OUT, fig_filename),
            bbox_inches='tight', dpi=my_dpi)
plt.tight_layout()
plt.show()
