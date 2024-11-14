# -*- coding: utf-8 -*-
"""
Created on Fri May 14 12:35:09 2021

@author: apizz
"""

"""
OPEN GLM in BV-Axis of Motion Pilot
    Load GLM results in BrainVoyager to create .vmp maps

14-05-21

AP [BV22]
# Run for P04, P03, P02
"""

import os
from glob import glob

print("Hello!")

# ======== Specify the input

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-04'];
COND = ['magn_only_noNOISE'];    # ['standard', 'magn_only','magn_phase']
FUNC = ['BOLD_interp', 'VASO_interp_LN']    # ['VASO_interp_LN']

CV_RUN = ['runs_1_2']
for si in SUBJ:
    for co in COND:
        PATH_SBJ = os.path.join(STUDY_PATH, si, 'derivatives',
                                'func', 'AOM', 'vaso_analysis', co, 'cross_validation')
        sbf = os.path.join(PATH_SBJ, CV_RUN[0])

        for fu in FUNC:
            PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')
            PATH_VTC = os.path.join(sbf, 'GLM')

            docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
            docVMR.link_vtc(os.path.join(PATH_VTC, fu + "_NeuroElf_IDENTITY.vtc"))
            docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols', si + '_Pilot_AOM_run01.prt'))
            docVMR.load_glm(os.path.join(PATH_VTC, '{}_{}_{}.glm'.format(si, co, fu)))
