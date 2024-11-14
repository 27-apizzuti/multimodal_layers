""" Characterizing CV-Step 1

Discovering the percentage of discarding voxels per CV fold and per category
when comparing training and test set.

Which category is more stable? Has the control model a lower number of voxels?

Input VMP file.

Created on Tue Sep 21 11:44:13 2021
@author: apizz
"""
import os
import numpy as np
import bvbabel
from glob import glob


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07']
CONDT = ['standard']
FUNC = ['BOLD', "VASO"]  # Always put BOLD first, "VASO"
ROI_NAME = 'leftMT_Sphere16radius'
q = 0.05

allSBJ_stats = {'sub-02': [], "sub-03": [], "sub-04": [], "sub-05": [], "sub-06": [], "sub-07": []}
allSBJ_withinFLD = {'sub-02': [], "sub-03": [], "sub-04": [], "sub-05": [], "sub-06": [], "sub-07": []}

# Used to append subjects
# Q: How much percentage overlap do we have between training and test label for each fold?
# Q: Is the percentage overlap constant across folds?
PATH_OUT = os.path.join(STUDY_PATH, 'Results', "LORO_investivation")


for su in SUBJ:

    # Single subject variables
    SBJ_stats = {"BOLD": [], "VASO": []}

    for fu in FUNC:
        SBJ_stats[fu] = {"SubjID": su,"N_start_train_voxels": [], "Perc_overlap_test": [], "Perc_overlap_test_4cat": [],
                     "Bool_train_test": [], "Bool_train_4cat": [], "Bool_test_4cat": []};


        PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                        'vaso_analysis', CONDT[0], 'cross_validation')

        print("Processing {} {}".format(fu, su))
        CVFLD = glob(os.path.join(PATH_CV, "runs*", ""))
        n_fold = len(CVFLD)

        for iter, cv in enumerate(CVFLD):
            PATH_VMP = os.path.join(cv, 'GLM')
            FILE_VMP = '{}_check_cv_vox.vmp'.format(fu)
            header, data = bvbabel.vmp.read_vmp(os.path.join(PATH_VMP, FILE_VMP))

            # Training vs Test comparison across CV folds
            train = data[:, :, :, 7]; train_lab = train[train > 0]
            test = data[:, :, :, 8]; test_lab = test[test > 0]

            # 1) General overlap between training and test
            n_start_vox = len(train_lab)
            print("Number of selected voxels from training {}".format(n_start_vox))
            n_vox = np.sum(train_lab == test_lab)
            gen_over = 100* n_vox/np.sum(train > 0)
            SBJ_stats[fu]["N_start_train_voxels"].append(n_start_vox)
            SBJ_stats[fu]["Perc_overlap_test"].append(gen_over)

            print("Num. of common voxels betw training and test dataset {} ({}%)".format(n_vox, int(gen_over)))
            print("Grouping train and test labels across CV")
            SBJ_stats[fu]["Bool_train_test"].append(train > 0)

            # Initialize variables
            temp_cat_train = []
            temp_cat_test = []
            temp_cat_tt = np.zeros(4)

            # 2) Count voxels per category training and test
            for itercat, lab in enumerate(range(1, 5)):
                print(itercat, lab)
                print("Category {}".format(lab))
                idx = (train_lab == lab) * (test_lab == lab)
                n_vox_cat = np.sum(idx)
                x = 100 * n_vox_cat / n_vox
                temp_cat_tt[itercat] = x
                temp_cat_train.append(train == lab)
                temp_cat_test.append(test == lab)

            SBJ_stats[fu]["Perc_overlap_test_4cat"].append(temp_cat_tt)
            SBJ_stats[fu]["Bool_train_4cat"].append(temp_cat_train)
            SBJ_stats[fu]["Bool_test_4cat"].append(temp_cat_test)

    allSBJ_stats[su] = SBJ_stats
# %% Exploring across folds overlap: SBJ_train, SBJ_test
# Q: How much robust are the training dataset and the test dataset, separatetly, across CV fold?
# Q: Can we conclude that training is more robust than the test?

# 4Category
DATASET = ["train", "test"]

for itersbj in SUBJ:
    # Single subject variables
    SBJ_stats = {"BOLD": [], "VASO": []}

    for itercontr in FUNC:
        SBJ_stats[itercontr] = {"train": [], "test": []}

        for data in DATASET:
            SBJ_stats[itercontr][data] = {"global": [], "global_4cat": [], "glob_mean_std": [], "glob_cat_mean": [], "glob_cat_std": []}
            n_cv = len(allSBJ_stats[itersbj][itercontr]["Bool_train_test"])
            print(n_cv)

            glob = np.zeros([n_cv, n_cv])
            glob_cat = np.zeros([4, n_cv, n_cv])

            for iterCV1 in range(0, n_cv):
                x = allSBJ_stats[itersbj][itercontr]["Bool_train_test"][iterCV1]

                # 4 category
                c1 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV1][0]
                c2 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV1][1]
                c3 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV1][2]
                c4 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV1][3]

                for iterCV2 in range(0, n_cv):
                    y = allSBJ_stats[itersbj][itercontr]["Bool_train_test"][iterCV2]
                    glob[iterCV1, iterCV2] = 100 * np.sum(x * y)/np.sum(x)

                    # 4 category
                    d1 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV2][0]
                    d2 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV2][1]
                    d3 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV2][2]
                    d4 = allSBJ_stats[itersbj][itercontr]["Bool_{}_4cat".format(data)][iterCV2][3]

                    glob_cat[0, iterCV1, iterCV2] = 100 * np.sum(c1 * d1)/np.sum(c1)
                    glob_cat[1, iterCV1, iterCV2] = 100 * np.sum(c2 * d2)/np.sum(c2)
                    glob_cat[2, iterCV1, iterCV2] = 100 * np.sum(c3 * d3)/np.sum(c3)
                    glob_cat[3, iterCV1, iterCV2] = 100 * np.sum(c4 * d4)/np.sum(c4)

            SBJ_stats[itercontr][data]["global"] = glob
            SBJ_stats[itercontr][data]["global_4cat"] = glob_cat

            SBJ_stats[itercontr][data]["glob_mean_std"] = [np.mean(glob[~np.eye(glob.shape[0], dtype=bool)]),
                                                           np.std(glob[~np.eye(glob.shape[0], dtype=bool)])]

            SBJ_stats[itercontr][data]["glob_cat_mean"] = [np.mean(glob_cat[0, ~np.eye(glob_cat[0, :, :].shape[0], dtype=bool)]),
                                                                np.mean(glob_cat[1, ~np.eye(glob_cat[1, :, :].shape[0], dtype=bool)]),
                                                                np.mean(glob_cat[2, ~np.eye(glob_cat[2, :, :].shape[0], dtype=bool)]),
                                                                np.mean(glob_cat[3, ~np.eye(glob_cat[3, :, :].shape[0], dtype=bool)]),
                                                                ]
            SBJ_stats[itercontr][data]["glob_cat_std"] = [np.std(glob_cat[0, ~np.eye(glob_cat[0, :, :].shape[0], dtype=bool)]),
                                                                np.std(glob_cat[1, ~np.eye(glob_cat[1,:, :].shape[0], dtype=bool)]),
                                                                np.std(glob_cat[2, ~np.eye(glob_cat[2,:, :].shape[0], dtype=bool)]),
                                                                np.std(glob_cat[3, ~np.eye(glob_cat[3,:, :].shape[0], dtype=bool)]),
                                                                ]

    allSBJ_withinFLD[itersbj] = SBJ_stats

np.save(os.path.join(PATH_OUT, "allSbj_descriptives_part1_dict"),
                allSBJ_stats, allow_pickle=True)

np.save(os.path.join(PATH_OUT, "allSbj_descriptives_part2_dict"),
                allSBJ_withinFLD, allow_pickle=True)
