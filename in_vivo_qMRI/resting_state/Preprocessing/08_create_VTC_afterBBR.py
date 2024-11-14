# This script creates VTC after running BBR (main experiment at 0.8 iso mm --> co-registered and resampled to 0.7 iso mm)

import numpy as np
import os
import glob

print("Hello.")

# =============================================================================
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-04"]
SESS = ["sess-02"]
TASK = ["rest"]

for su in SUBJ:
    for se in SESS:
        print('Working on {}, {}'.format(su, se))
        PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')
        #// Open VMR
        if su == 'sub-09':
            file_vmr = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr".format(su))
        else:
            file_vmr = os.path.join(STUDY_PATH, su, "derivatives", "anat", "{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr".format(su))
        doc_vmr = bv.open(file_vmr)
        path_out = os.path.join(STUDY_PATH, su, "derivatives", "func", se, 'MOT_VTC_cut')

        if not os.path.exists(path_out):
            os.mkdir(path_out)
        path_in = os.path.join(PATH_FMR, '{}'.format(se))
        for ta in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, ta), recursive=True)
            for path_run in runs:
                print(path_run.split("\\"))
                temp = path_run.split("\\")[-2]


                if (temp == 'phy00'):
                    print('Skipping {}'.format(temp))
                else:
                    print('Working on {}'.format(temp))
                    #// Input files
                    path_run = os.path.join(path_run, "topup")

                    if (su == 'sub-01') & (se == 'sess-02'):
                        path_trx = os.path.join(STUDY_PATH, su, "derivatives", "func", "sess-01", "BBR")
                    else:
                        path_trx = os.path.join(STUDY_PATH, su, "derivatives", "func", se, "BBR")
                    print(path_run)
                    FMR = glob.glob(os.path.join(path_run, '*THPGLMF5c.fmr'))[0]
                    coreg_fa_trf_file = glob.glob(os.path.join(path_trx, "*_BBR_FA.trf"))[0]
                    coreg_ia_trf_file = glob.glob(os.path.join(path_trx, "*_IA.trf"))[0]

                    #// Bounding box option
                    BB_XYZ = [15, 225, 115, 313, 1, 190];
                    if su == 'sub-07':
                        BB_XYZ = [30, 220, 165, 300, 40, 150];
                    elif su == 'sub-08':
                        BB_XYZ = [30, 220, 200, 300, 90, 210];
                    elif su == 'sub-09':
                        BB_XYZ = [20, 220, 200, 300, 90, 220];
                    elif su == 'sub-10':
                        BB_XYZ = [20, 220, 200, 300, 90, 240];
                    else:
                        BB_XYZ = [20, 220, 200, 300, 90, 220];
                    doc_vmr.vtc_creation_use_bounding_box = 'true';
                    doc_vmr.vtc_creation_bounding_box_from_x = BB_XYZ[0]; doc_vmr.vtc_creation_bounding_box_to_x = BB_XYZ[1]; #//coded in bbx as X
                    doc_vmr.vtc_creation_bounding_box_from_y = BB_XYZ[2]; doc_vmr.vtc_creation_bounding_box_to_y = BB_XYZ[3]; #//coded in bbx as Y
                    doc_vmr.vtc_creation_bounding_box_from_z = BB_XYZ[4]; doc_vmr.vtc_creation_bounding_box_to_z = BB_XYZ[5]; #//coded in bbx as Z

                    #// Output name
                    basename = FMR.split(os.extsep, 1)[0]
                    outname = basename.split("\\")[-1]
                    vtc_file = os.path.join(path_out, "{}_{}_BBR.vtc".format(outname, se))
                    print('Creating VTC for {}'.format(basename))
                    doc_vmr.create_vtc_in_native_space(FMR, coreg_ia_trf_file, coreg_fa_trf_file, vtc_file, 1, 1)   #//1 codes for trilinear interpolation
