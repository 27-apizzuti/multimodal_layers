# preprocess FMR: slictime, moco, highpass ; AP
# This script was used to preprocess high-res and lo-res functional data acquired with CMRR sequence;

import numpy as np
import os
import glob

print("Hello.")

# =============================================================================
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-04"]
SESS = [2]
TASK = ["rest"]

# Parameters
for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')

    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))
        for tas in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            print(runs)
            # // Here refer to the reference volume for the motion correction (indicate the nifti). It should be the first functional run of the session
            MOCO_REF_VOL = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'sess-0{}'.format(se), 'phy01', '{}_task-phy_acq-2depimb4_run-01.fmr'.format(su))

            for path_run in runs:
                docPathIn = glob.glob(os.path.join(path_run, '*.fmr'))[0]
                #1// Correct Slice Timing
                docFMR = bv.open(docPathIn)
                docFMR.correct_slicetiming_using_timingtable(2) # window. sinc interpolation
                Fnme_newFMR = docFMR.preprocessed_fmr_name
                docFMR.close()

                #2// Motion Correction
                docFMR=bv.open(Fnme_newFMR)
                docFMR.correct_motion_to_run_ext(MOCO_REF_VOL, 0, 2, 1, 100, 1, 1)
                Fnme_newFMR = docFMR.preprocessed_fmr_name
                docFMR.close()
