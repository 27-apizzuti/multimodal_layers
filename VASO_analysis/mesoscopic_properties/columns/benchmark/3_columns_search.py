"""
Created on Monday 21rst of January

This script searches for columns.

@author: apizz
"""
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
name_mask = 'BOLD_FDR'
RADIUS_DISK = [15, 13, 12, 13, 16]

# Program parameter (cylinder)
RADIUS = 0.6  # diameter spans the effective resolution (0.8mm)
HEIGHT = 2

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'random_columns')

    PATH_OUT = PATH_IN

    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS_DISK[iterSbj]))
    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))


    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin_masked_{}_full_depth.nii.gz'.format(su, name_mask))

    print("For {}, searching columns in per_chunck masked with {}".format(su, name_mask))

    VALUE = os.path.join(PATH_IN, '{}_{}_random_upsampled.nii.gz'.format(su, ROI))
    outname = os.path.join(PATH_OUT, '{}_{}_{}_random_columns_full_depth.nii.gz'.format(su, ROI, name_mask))

    command = "LN2_UVD_FILTER "
    command += "-values {} ".format(VALUE)
    command += "-coord_uv {} ".format(COORD_UV)
    command += "-coord_d {} ".format(COORD_D)
    command += "-domain {} ".format(DOMAIN)
    command += "-radius {} ".format(RADIUS)
    command += "-height {} ".format(HEIGHT)
    command += "-columns "
    command += "-output {} ".format(outname)
    subprocess.run(command, shell=True)
