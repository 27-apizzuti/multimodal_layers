"""Read BrainVoyager FMR file format and save first volume for each run.
   Check motion correction"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import glob
import matplotlib.pyplot as plt
from pprint import pprint
# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-04"]
SESS = [2]
TASK = ["rest"]

for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')
    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))

        for tas in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            for path_run in runs:
                print(path_run)
                temp = path_run.split("/")[-2]
                if (su == 'sub-10') & (se == 2):
                    if temp == 'phy00':
                        # // Load nifti (created for topup)
                        print('Skip phy00')
                    else:
                        # // Load nifti (created for topup)
                        nifti_file = os.path.join(path_in, "topup", "{}_sess-0{}_PA.nii.gz".format(su, se))
                        nii = nb.load(nifti_file) # // We take the header from here
                else:
                    if temp == 'phy00':
                        # // Load nifti (created for topup)
                        nifti_file = os.path.join(path_in, "topup", "{}_sess-0{}_PA.nii.gz".format(su, se))
                        nii = nb.load(nifti_file) # // We take the header from here
                    else:
                        # // Load nifti (created for topup)
                        nifti_file = os.path.join(path_in, "topup", "{}_sess-0{}_AP.nii.gz".format(su, se))
                        nii = nb.load(nifti_file) # // We take the header from here

                # Find FMR and create output name
                PATH_TOPUP = os.path.join(path_run, 'topup')
                if not os.path.exists(PATH_TOPUP):
                    os.mkdir(PATH_TOPUP)

                # FMR = glob.glob(os.path.join(path_run, '*01.fmr'))[0]
                FMR = glob.glob(os.path.join(path_run, '*3DMCTS.fmr'))[0]
                basename = FMR.split(os.extsep, 1)[0]
                filename = basename.split("/")[-1]
                outname1 = "{}_reference_bvbabel.nii.gz".format(basename)
                outname2 = os.path.join(PATH_TOPUP, "{}_bvbabel.nii.gz".format(filename))

                # Load FMR
                print('Read {}'.format(FMR))
                header, datafmr = bvbabel.fmr.read_fmr(FMR, rearrange_data_axes=False)
                nslices = header['NrOfSlices']
                nvol = header['NrOfVolumes']
                resY = header['ResolutionY']
                resX = header['ResolutionX']
                datafmr = np.transpose(datafmr, (3, 2, 0, 1))
                datafmr=datafmr[:,::-1,:,:]

                # Save first volume as NIFTI
                print('Save reference nifti')

                datafmr1 = datafmr[..., 0:5]

                img = nb.Nifti1Image(datafmr1, affine=nii.affine, header=nii.header)
                nb.save(img, outname1)

                # Save all time course for topup
                print('Save time course nifti')
                img = nb.Nifti1Image(datafmr, affine=nii.affine, header=nii.header)
                nb.save(img, outname2)


print("Finished.")
