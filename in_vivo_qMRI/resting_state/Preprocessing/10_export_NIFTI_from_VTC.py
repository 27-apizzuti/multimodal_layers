"""Prepare data for computing extra affine matrices for appling correctly MNI transformation"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from scipy import ndimage
import subprocess
from glob import glob

# Settings
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUB = ['sub-04']
TASK = ['rest']

for su in SUB:
    print('Working on {}'.format(su))

    # // Load VMR
    FILE_VMR = glob(os.path.join(STUDY_PATH, su, 'derivatives', 'anat', '*_acq-mp2rage_UNI_denoised_IIHC_ISOpt6.vmr'))[0]
    header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)

    for ta in TASK:
        VTC_list = glob(os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'VTC_native', '{}_task-{}_acq-2depimb2_*_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_sess-02_BBR.vtc'.format(su, ta)))

        for VTC_file in VTC_list:

            # Load VTC
            header, tdata = bvbabel.vtc.read_vtc(VTC_file, rearrange_data_axes=False)
            print('Dimension of VTC {}'.format(np.shape(tdata)))

            # VTC -> NIFTI entire time series
            tdata = np.transpose(tdata, [0, 2, 1, 3])
            tdata = tdata[::-1, ::-1, ::-1, :]
            tdata.astype(np.float32)
            print('Dimension of NIFTI at 0.35 {}'.format(np.shape(tdata)))
            basename = VTC_file.split(os.extsep, 1)[0]
            outname = "{}_resx2.nii.gz".format(basename)
            temp = np.eye(4)

            img = nb.Nifti1Image(tdata, affine=temp)

            nb.save(img, outname)
            print("Finished.")

            # VTC -> Temporal mean
            datamean = np.mean(tdata, axis=-1)
            outname = "{}_mean_resx2.nii.gz".format(basename)
            img = nb.Nifti1Image(datamean, affine=temp)
            nb.save(img, outname)
            print("Finished.")
