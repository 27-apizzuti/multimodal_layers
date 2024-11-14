""" Create figures of CV_step1_inspection.

Created on Wed Sep 22 11:42:17 2021

@author: apizz
"""

import os
import numpy as np
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"

PATH_IN = os.path.join(STUDY_PATH, "Results", "LORO_investivation")


NPZ_FILE1 = "allSbj_descriptives_part1_dict.npy"
NPZ_FILE2 = "allSbj_descriptives_part2_dict.npy"

dict1 = np.load(os.path.join(PATH_IN, NPZ_FILE1), allow_pickle=True).item()
dict2 = np.load(os.path.join(PATH_IN, NPZ_FILE2), allow_pickle=True).item()

SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07']

# Plot1: Agreement of training set voxel selection: from dict2
# Subplot(1, 2)-BOLD and VASO, [mean_std vs subjects]
# // Extract Y
Y = np.zeros([2, len(SUBJ), 2])
for iter, su in enumerate(SUBJ):
    Y[0, iter, :] = dict2[su]["BOLD"]["train"]["glob_mean_std"]
    Y[1, iter, :] = dict2[su]["VASO"]["train"]["glob_mean_std"]

my_dpi = 96
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
x = np.array([2, 3, 4, 5, 6, 7])

contrast = ["BOLD", "VASO"]

for k in range(0, 2):

    axs[k].errorbar(x, Y[k, :, 0], Y[k, :, 1], color='black')
    axs[k].axvspan(x[-1]-0.5, x[-1]+0.5, facecolor='yellow', alpha=0.5)
    axs[k].set_title("{}".format(contrast[k]))
    axs[k].set_xticks(x)
    axs[k].set_ylim([60, 100])
    axs[k].set_ylabel("% Voxels Overlap Across Folds (from TrainingData)")
    axs[k].set_xlabel("Subjects")

fig_filename = "Voxels_selection_acrossFolds_BOLD_VASO"
plt.savefig(os.path.join(PATH_IN, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()


# Plot2: Training Agreement across CV folds: from dict2
# Subplot(1, 2)-BOLD and VASO, [mean_std vs category]
x = np.array([2, 3, 4, 5, 6, 7])
Y = np.zeros([2, len(SUBJ), 4])   # mean
Z = np.zeros([2, len(SUBJ), 4])   # std
contrast = ["Horizontal", "Vertical", "Diag45", "Diag135"]

for iter, su in enumerate(SUBJ):
    Y[0, iter, :] = dict2[su]["BOLD"]["train"]["glob_cat_mean"]
    Z[0, iter, :] = dict2[su]["BOLD"]["train"]["glob_cat_std"]

    Y[1, iter, :] = dict2[su]["VASO"]["train"]["glob_cat_mean"]
    Z[1, iter, :] = dict2[su]["VASO"]["train"]["glob_cat_std"]

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

for k in range(0, 4):
    print(k)
    axs[k].errorbar(x, Y[0, :, k], Z[0, :, k], color='black', label='BOLD')
    axs[k].errorbar(x, Y[1, :, k], Z[1, :, k], color='red', label='VASO')
    axs[k].axvspan(x[-1]-0.5, x[-1]+0.5, facecolor='yellow', alpha=0.5)

    axs[k].set_title("{}".format(contrast[k]))
    axs[k].set_xticks(x)
    axs[k].set_ylim([25, 60])
    axs[k].set_ylabel("% Voxels Overlap Across Folds (from TrainingData)")
    axs[k].set_xlabel("Subjects")
    axs[k].legend();

fig_filename = "Voxels_selection_Training_perCategory_acrossFolds_BOLD_VASO"
plt.savefig(os.path.join(PATH_IN, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()

# Plot3: Test Agreement across CV folds: from dict2
# Subplot(1, 2)-BOLD and VASO, [mean_std vs category]
x = np.array([2, 3, 4, 5, 6, 7])
Y = np.zeros([2, len(SUBJ), 4])   # mean
Z = np.zeros([2, len(SUBJ), 4])   # std
contrast = ["Horizontal", "Vertical", "Diag45", "Diag135"]

for iter, su in enumerate(SUBJ):
    Y[0, iter, :] = dict2[su]["BOLD"]["test"]["glob_cat_mean"]
    Z[0, iter, :] = dict2[su]["BOLD"]["test"]["glob_cat_std"]

    Y[1, iter, :] = dict2[su]["VASO"]["test"]["glob_cat_mean"]
    Z[1, iter, :] = dict2[su]["VASO"]["test"]["glob_cat_std"]

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

for k in range(0, 4):
    print(k)
    axs[k].errorbar(x, Y[0, :, k], Z[0, :, k], color='black', label='BOLD')
    axs[k].errorbar(x, Y[1, :, k], Z[1, :, k], color='red', label='VASO')
    axs[k].axvspan(x[-1]-0.5, x[-1]+0.5, facecolor='yellow', alpha=0.5)
    axs[k].set_title("{}".format(contrast[k]))
    axs[k].set_xticks(x)
    axs[k].set_ylim([10, 40])
    axs[k].set_ylabel("% Voxels Overlap Across Folds (from TestData)")
    axs[k].set_xlabel("Subjects")
    axs[k].legend();

fig_filename = "Voxels_selection_Test_perCategory_acrossFolds_BOLD_VASO"
plt.savefig(os.path.join(PATH_IN, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()
