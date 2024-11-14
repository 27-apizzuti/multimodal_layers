"""
Created on Thu Sep 30 17:57:13 2021

Evaluating AVG-CV-voxels

1) Rank voxels according to Sens and Spec
2) Compare AVG vs CV-AVG voxels

Input: AVG VMP, CV-AVG VMP


@author: apizz
"""

import os
import numpy as np
import bvbabel
import scipy
import scipy.stats as sps
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']                                         # Always put BOLD first, "VASO"
ROI_NAME = ['leftMT_Sphere16radius']

tag = 'c_thr_4'
VASO_BOLD_MASK = True
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')

for roi in ROI_NAME:
    red_bin_spec = np.zeros([2, 5, 5])
    for i, su in enumerate(SUBJ):
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'GLM', 'ROI')
        PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'cross_validation', 'Results')

        for j, fu in enumerate(FUNC):

            print("Working on {}, {}, {}".format(su, roi, fu))
            # Get data
            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

            # AVG dictionary
            NPY_FILENAME = "{}_{}_meanRuns_{}_ROI_{}_{}{}_tuning_dict.npy".format(su, fu, CONDT[0], roi, tag, mask_suffix)

            tuning_dict = np.load(os.path.join(PATH_IN, NPY_FILENAME),
                                  allow_pickle=True).item()

            # CV-AVG final voxels
            NPY_CV_AVG = "{}_{}_{}_{}{}_cv_step2_dict.npy".format(su, fu, roi, tag, mask_suffix)


            cv_avg_dict = np.load(os.path.join(PATH_CV, NPY_CV_AVG),
                                  allow_pickle=True).item()

            # Find discarded voxels from the cluster thresholding
            temp = cv_avg_dict["idx_AVG_3D"] == True
            idx = cv_avg_dict["idx_cv_avg_c_thr"]
            CV_AVG_C_THR = idx[temp>0]

            spec_avg = tuning_dict["Specificity"]
            spec_cv_avg = tuning_dict["Specificity"] * CV_AVG_C_THR
            spec_cv_avg = spec_cv_avg[spec_cv_avg>0]
            bins_spec = np.array([0, 0.2, 0.4, 0.6, 0.8])

            for k in range(0,5):
                n = np.sum((spec_avg >= bins_spec[k]) * (spec_avg < bins_spec[k] + 0.2))
                nn = np.sum((spec_cv_avg >= bins_spec[k]) * (spec_cv_avg < bins_spec[k] + 0.2))
                if (n > 0) & (nn > 0):
                    red_bin_spec[j, k, i] = (1 - (nn / n)) *100
                else:
                    red_bin_spec[j, k, i] = 'nan'
                    print("Original: {}, CV: {} -> {} %".format(n, nn, red_bin_spec[j, k, i]))
# Build the plot
my_dpi = 96
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
for z in range(0,2):
    x_ticks_lab = ['0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']
    x_pos = np.array([1, 2, 3, 4, 5])
    y_pos = np.arange(0, 100, 10)
    y = np.nanmean(red_bin_spec[z, :, :], axis=1)
    s_error = scipy.stats.sem(red_bin_spec[z, :, :], axis=1, nan_policy='omit')
    ax[z].bar(x_pos, y, yerr=s_error, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax[z].set_ylabel('% Percentage of voxels reduction after CV')
    ax[z].set_xlabel('Specificity')
    ax[z].set_xticks(x_pos)
    ax[z].set_yticks(y_pos)
    ax[z].set_ylim([0, 100])
    ax[z].set_xticklabels(x_ticks_lab)
    if z == 0:
        ax[z].set_title('BOLD')
    else:
        ax[z].set_title('VASO')
    ax[z].yaxis.grid(True)
fig_filename = "CV_AVG_Specificity_Reduction{}{}".format(roi, mask_suffix)
plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()




            # # Sensitivity
            # # Flatten matrix and sorted
            # avg_sens = data_avg[..., 2].flatten()
            # cv_sens = data_cv_avg[..., 2].flatten()

            # y_avg_sens = avg_sens[np.argsort(avg_sens)[::-1]]
            # y_cv_senss = cv_senss[np.argsort(cv_senss)[::-1]]

            # y_avg_sens = y_avg_sens[y_avg_sens>0]
            # y_cv_senss = y_cv_senss[y_cv_senss>0]

            # # # Specificity
            # # avg_spec = data_avg[..., 3].flatten()
            # # cv_avg_spec = data_cv_avg[..., 3].flatten()

            # # y_avg_spec = avg_sens[np.argsort(avg_spec)[::-1]]
            # # y_cv_avg_spec = cv_senss[np.argsort(cv_avg_spec)[::-1]]

            # # y_avg_spec = y_avg_spec[y_avg_spec>0]
            # # y_cv_avg_spec = y_cv_avg_spec[y_cv_avg_spec>0]
            # y = y_avg_sens

            # mn = np.min(y)
            # mx = np.max(y)
            # size = mx
            # x = np.arange(size)

            # plt.hist(y_avg_sens, bins=range(48))

            # dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']

            # for dist_name in dist_names:
            #     dist = getattr(scipy.stats, dist_name)
            #     params = dist.fit(y)
            #     arg = params[:-2]
            #     loc = params[-2]
            #     scale = params[-1]
            #     if arg:
            #         pdf_fitted = dist.pdf(x, *arg, loc=loc, scale=scale) * size
            #     else:
            #         pdf_fitted = dist.pdf(x, loc=loc, scale=scale) * size
            #     plt.plot(pdf_fitted, label=dist_name)
            #     plt.xlim(0,47)


            # # plotting
            # my_dpi = 96
            # plt.figure(figsize=(1920/my_dpi, 1080/my_dpi))
            # #fig, axs = plt.subplots(2, 2)
            # #plt.hist([y_avg_sens, y_cv_senss], 100, histtype='barstacked', density=True, alpha=0.4, edgecolor='none')
            # plt.hist(y_avg_sens, 100, histtype='barstacked', density=True, alpha=0.4, edgecolor='none', color='C0')
            # plt.hist(y_cv_senss, 100, histtype='barstacked', density=True, alpha=0.4, edgecolor='none', color='C1')

            # mn, mx = plt.xlim()
            # plt.xlim(mn, mx)
            # x = np.linspace(mn, mx, 1000)
            # kde_avg = sps.gaussian_kde(y_avg_sens)
            # kde_cv_avg = sps.gaussian_kde(y_cv_senss)

            # #plt.axvline(x[np.argmax(kde_avg.pdf(x))], ymin=np.min(kde_avg.pdf(x)), ymax=np.max(kde_avg.pdf(x)), color='C0', ls='--')
            # plt.plot(x, kde_avg.pdf(x), label='AVG voxels', color='C0')
            # plt.plot(x, kde_cv_avg.pdf(x), label='CV AVG voxels', color='C1')


            # #plt.axvline(x[np.argmax(kde_cv_avg.pdf(x))], color='C1', ls='--')

            # plt.legend()
            # plt.ylabel('Probability density')
            # plt.xlabel('Sensitivity')

            # # Specificity
            # axs[0, iter].plt.hist([y_avg_spec, y_cv_avg_spec], 100, histtype='barstacked', density=True, alpha=0.4, edgecolor='none')

            # mn, mx = plt.xlim()
            # plt.xlim(mn, mx)
            # x = np.linspace(mn, mx, 1000)
            # kde_avg2 = sps.gaussian_kde(y_avg_spec)
            # kde_cv_avg2 = sps.gaussian_kde(y_cv_avg_spec)


            # plt.plot(x, kde_avg2.pdf(x), label='AVG voxels', color='C0')
            # plt.plot(x, kde_cv_avg2.pdf(x), label='CV AVG voxels', color='C1')
            # plt.axvline(x[np.argmax(kde_avg2.pdf(x))], ymin=np.min(kde_avg2.pdf(x)), ymax=np.max(kde_avg2.pdf(x)), color='C0', ls='--')
            # plt.axvline(x[np.argmax(kde_cv_avg2.pdf(x))], color='C1', ls='--')

            # plt.legend()
            # plt.ylabel('Probability density')
            # plt.xlabel('Specificity')


            # plt.plot(x, d2.pdf(x), color='C1', ls='--', label='d2')

            # x = np.array([1, 2, 3, 4])
            # fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

            # thres_1 = int(n_avg * k / 100)
            # kk = z[0:thres_1]
            # np.sum(kk > 0)
            #x = avg_sens.reshape(data_dims)
