"""Create averaged time series for cross-validation.

Created on Mon May 31 14:31:31 2021

@author: apizz

Run (standard) P02, P03, P04
"""

import os
import glob
import numpy as np
import nibabel as nib

print("Hello!")

# =============================================================================
# Input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-04"
PROC = "magn_only_noNOISE"
PATH_IN = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'moco')
PATH_OUT = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'cross_validation')
# =============================================================================
# Execution
nn_a = glob.glob(PATH_IN + "\\Not_Nulled*a.nii")    # not nulled basis a
n_b = glob.glob(PATH_IN + "\\Nulled_Basis*b.nii")     # nulled basis b

nruns = len(nn_a)

dim_a = (nib.load(nn_a[0])).shape
dim_b = (nib.load(n_b[0])).shape

# Put all the runs in a single matrix
dataNotNulled = np.zeros(dim_a + (nruns,))  # not nulled
dataNulled = np.zeros(dim_b + (nruns,))  # nulled

for iterRun in range(0, nruns):
    print(iterRun)

    FILE_not_nulled = nib.load(nn_a[iterRun])
    FILE_nulled = nib.load(n_b[iterRun])

    dataNulled[..., iterRun] = FILE_nulled.get_fdata()
    dataNotNulled[..., iterRun] = FILE_not_nulled.get_fdata()

# Free some memory
# FILE_not_nulled, FILE_nulled = None, None

# Leave one run out
runs = np.array(range(0, nruns))
for iterRunOut in runs:
    print(iterRunOut)
    arr1 = runs[:iterRunOut]
    arr2 = runs[iterRunOut+1:]
    idx = list(arr1) + list(arr2)
    fld_name = "runs_" + str(idx)
    fld_name = fld_name.replace(", ", "_")
    fld_name = fld_name.replace("[", "")
    fld_name = fld_name.replace("]", "")
    # kept_runs_not_nulled =      # extract the kept runs (not nulled)
    # kept_runs_nulled =      # extract the kept runs (nulled)

    # Create output folder
    if not os.path.exists(os.path.join(PATH_OUT, fld_name)):
        os.mkdir(os.path.join(PATH_OUT, fld_name))

    # Compute average across runs
    averaged_not_nulled = np.mean(dataNotNulled[..., idx], axis=4)
    averaged_nulled = np.mean(dataNulled[..., idx], axis=4)

    # Saving time series
    FILE_not_nulled = nib.Nifti1Image(averaged_not_nulled,
                                      affine=FILE_not_nulled.affine,
                                      header=FILE_not_nulled.header)
    FILE_nulled = nib.Nifti1Image(averaged_nulled,
                                  affine=FILE_nulled.affine,
                                  header=FILE_nulled.header)

    nib.save(FILE_not_nulled, os.path.join(PATH_OUT, fld_name,
                                           'Not_Nulled_Basis_a.nii.gz'))
    nib.save(FILE_nulled, os.path.join(PATH_OUT, fld_name,
                                       'Nulled_Basis_b.nii.gz'))

print("Done.")
