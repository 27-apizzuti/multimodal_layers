"""
Created on Wed Jul 28 14:51:03 2021
    Tuning Curves (subject-specfic)

INPUT: niftis of all subjects
OUTPUT: figures

@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
N_SUB = len(SUBJ)
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
#MASK = ["BOLD_FDR_mask", "BOLD_FDR_mask"]
MASK = ""
ROI_NAME = "leftMT_Sphere16radius"
NMAP = 2
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Tuning_only_Hor_Vert')

if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)


for iterSubj, su in enumerate(SUBJ):

    PATH_WINNER = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'masks')
    PATH_TMAP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')

    # Initialize output variables
    tuning = np.zeros([2, NMAP, NMAP, 2])
    NrOfVox = np.zeros([2, NMAP, 2])
    n_vox = np.zeros(2)

    n_vox = np.zeros(2)

    for iterfu, fu in enumerate(FUNC):

        TMAPS_NII = TMAPS_NII = "{}_{}_{}_tmaps.nii.gz".format(su, fu, ROI_NAME)
        WINNER_NII = "{}_{}_{}_winner_map.nii.gz".format(su, ROI_NAME, fu)
        ROI_NII = "{}_{}.nii.gz".format(su, ROI_NAME)

        # Read nifti tmap
        nii1 = nb.load(os.path.join(PATH_TMAP, TMAPS_NII))
        nii_tmaps = nii1.get_fdata()
        nii_tmaps = nii_tmaps[..., 0:NMAP]

        # Read nifti ROI
        nii2 = nb.load(os.path.join(PATH_WINNER, ROI_NII))
        vox_roi = nii2.get_fdata()
        idx1 = vox_roi > 0

        # Read winner map
        nii3 = nb.load(os.path.join(PATH_WINNER, 'maps', WINNER_NII))
        nii_win = nii3.get_fdata()

        if len(MASK) > 0 :

            MASK_NII = "{}_{}_{}.nii.gz".format(su, ROI_NAME, MASK[iterfu])
            nii4 = nb.load(os.path.join(PATH_MASK, MASK_NII))
            mask = nii4.get_fdata()
            mask_name = "{}_{}".format(MASK[0], MASK[1])
            idx2 = mask > 0
            idx = idx2 * idx1
        else:
            idx = idx1
            mask_name = "no_mask"

        # Extract voxel tvalue for each class and compute tuning
        vox_tvalue = nii_tmaps[idx]
        vox_label = nii_win[idx]
        n_vox[iterfu] = vox_tvalue.shape[0]

        for i, j in enumerate(range(1, NMAP+1)):
            print(i,j)
            vox_data = vox_tvalue[vox_label == j, :]
            tuning[iterfu, i, :, 0] = np.mean(vox_data, axis=0)
            #tuning[i, :, 1] = np.var(vox_data, axis=0)                # standard deviation
            tuning[iterfu, i, :, 1] = scipy.stats.sem(vox_data, axis=0)        # standard error
            NrOfVox[iterfu, i, 0] = vox_data.shape[0]
            NrOfVox[iterfu, i, 1] = vox_data.shape[0] / n_vox[iterfu] * 100

# %% Plotting
    my_dpi = 96
    x = np.array([1, 2])
    fig, axs = plt.subplots(nrows=1, ncols=NMAP, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    contrast = ["Horizontal", "Vertical"]

    TS_B = [tuning[0, 0, 0, 0]-tuning[0, 0, 1, 0], tuning[0, 1, 1, 0]-tuning[0, 1, 0, 0]]
    TS_V = [tuning[1, 0, 0, 0]-tuning[1, 0, 1, 0], tuning[1, 1, 1, 0]-tuning[1, 1, 0, 0]]

    for k in range(0, NMAP):
        axs[k].errorbar(x, tuning[0, k, :, 0], tuning[0, k, :, 1], color='black', label='BOLD')

        axs[k].errorbar(x, tuning[1, k, :, 0], tuning[1, k, :, 1], color='red', label='VASO')

        axs[k].axvspan(x[k]-0.5, x[k]+0.5, facecolor='#2ca02c', alpha=0.5)
        axs[k].set_title("Tuning for {}".format(contrast[k]))
        axs[k].set_xticks(x)
        axs[k].set_xticklabels(contrast)
        axs[k].set_ylim([-1, 3.5])
        axs[k].set_ylabel("T-value")
        axs[k].set_xlabel("Conditions")
        axs[k].legend();
    # fig_filename = 'allsubject_smooth_{}_{}_vmin_{}_vmax_{}.png'.format(smt_suffix, rest, my_vmin[smt], my_vmax[smt])

    text_counts = " \n|BOLD: H({:.0f}%) V({:.0f}%)| T.S.: H({:.2f}), V({:.2f})|Tot. {:.0f}|\n|VASO: H({:.0f}%) V({:.0f}%)|T.S.: H({:.2f}), V({:.2f})|Tot. {:.0f}|".format(NrOfVox[0, 0, 1],
                                                                  NrOfVox[0, 1, 1], TS_B[0], TS_B[1],
                                                                  n_vox[0],

                                                                  NrOfVox[1, 0, 1],
                                                                  NrOfVox[1, 1, 1], TS_V[0], TS_V[1],
                                                                  n_vox[1])

    plt.suptitle('{}-Tuning curves {}{} \n\n({})'.format(su, ROI_NAME, text_counts, mask_name))
    fig_filename = "{}_Tuning_Curves_{}_{}".format(su, ROI_NAME, mask_name)
    plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
    plt.show()
