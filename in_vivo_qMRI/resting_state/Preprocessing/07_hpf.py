# preprocess FMR: highpass ; AP
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

HPF_CUTOFF = 3

for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')
    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))
        for tas in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            for path_run in runs:
                print(path_run)
                temp = path_run.split("\\")[-2]
                print(temp)
                if temp == 'phy00':
                    print("Skip")
                else:

                    print("Run HPF for {}".format(path_run))
                    docPathIn = glob.glob(os.path.join(path_run, 'topup', '*fix.nii.gz'))[0]

                    # // High-pass filtering
                    docnii=bv.open(docPathIn)
                    docnii.filter_temporal_highpass_glm_fourier(HPF_CUTOFF)
                    docnii.close()
