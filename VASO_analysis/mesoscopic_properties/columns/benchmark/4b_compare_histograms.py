"""
Created on Tue Feb 22 10:29:54 2022

Evaluate columnar property (empirical data vs random data)

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import scipy.stats as stats
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
FUNC = ['BOLD', 'VASO']
MASK = 'BOLD_FDR'


PATH_OUT = "D:\\Pilot_Exp_VASO\\pilotAOM\\Results\\Control_Columns"
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=1, ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi), subplot_kw=dict(box_aspect=1), dpi=my_dpi)
n_bins = 50

for itSubj, su in enumerate(SUBJ):
    
    # ----------------------------------
    PATH_RAND = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'random_columns')
    RAND_DATA = '{}_{}_{}_random_columns_full_depth_UVD_columns_mode_filter_window_count_ratio.nii.gz'.format(su, ROI, MASK)
    # ---------------------------------

    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", "AOM", "vaso_analysis", "standard", "columns")

    # Loading benchmark dataset
    niir = nb.load(os.path.join(PATH_RAND, RAND_DATA))
    datar = niir.get_fdata()
    idx_r = (datar > 0) * (datar < 1)
    temp_datar = datar[idx_r]
    density_ran = stats.gaussian_kde(temp_datar)
    
    
    kur_ran = stats.kurtosis(temp_datar, fisher=True)
    skew_ran = stats.skew(temp_datar)
    
    # -----------------------------------------
    my_dpi = 96
    n_bins = 50

    eval_points = np.linspace(np.min(temp_datar), np.max(temp_datar))
    y_rand = density_ran.pdf(eval_points)
   
    for itFu, fu in enumerate(FUNC):
        FILE = "{}_{}_{}_{}_columns_full_depth_UVD_columns_mode_filter_window_count_ratio.nii.gz".format(su, ROI, MASK, fu)

        nii = nb.load(os.path.join(PATH_IN, FILE))
        data = nii.get_fdata()
        idx = (data > 0.25) * (data < 1)
        temp_data = data[idx]
        
        # Compute empirical distribution
        density_emp = stats.gaussian_kde(temp_data)
        y_emp = density_emp.pdf(eval_points)
        kur_emp = stats.kurtosis(temp_data, fisher=True)
        skew_emp = stats.skew(temp_data)
        
        # Plotting
        m = np.mean(temp_data)
        s = np.std(temp_data)
        print("For {}, {} mean {:.1f} +/- {:.1f} (random: {:.1f} +/- {:.1f})".format(su, fu, m, s, np.mean(temp_datar), np.std(temp_datar)))
        print("For {}, {} median {:.1f} (random: {:.1f})".format(su, fu, np.median(temp_data), np.median(temp_datar)))
        print("For {}, {} mode {} (random: {})".format(su, fu, stats.mode(temp_data), stats.mode(temp_datar)))

        print("For {}, {} kurtosis {:.1f} (random: {:.1f})".format(su, fu, kur_emp, kur_ran))
        print("For {}, {} skew {:.1f} (random: {:.1f})".format(su, fu, skew_emp, skew_ran))
        
        # // Empirical data 
        if fu == 'BOLD':
            axs[itSubj].plot(eval_points, y_emp, color = "blue")
        else:
            axs[itSubj].plot(eval_points, y_emp, color = "red")
        
        # //Random data
        axs[itSubj].plot(eval_points, y_rand, color = "black")
       
        axs[itSubj].set_xlim([0, 1])
        axs[itSubj].set_xlabel("Columnarity index")
        axs[itSubj].set_title("Sub-0{}".format(itSubj+1))


# # Saving plot
plt.savefig(os.path.join(PATH_OUT,'columnar_index_BOLD_VASO_{}_AllSbj_and_benchmark_pdf_random.jpeg'.format(ROI, MASK)), bbox_inches='tight')
plt.savefig(os.path.join(PATH_OUT,'columnar_index_BOLD_VASO_{}_AllSbj_and_benchmark_pdf_random.svg'.format(ROI, MASK)), bbox_inches='tight')
plt.show()
