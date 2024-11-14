import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
si = "sub-02"
ROI = "conj_bilMT_anat_sphere16radius"

PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')
PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func',
                            'AOM', 'vaso_analysis', 'standard', 'cross_validation', 'run_0', 'GLM')

docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
docVMR.link_vtc(os.path.join(PATH_VTC, "BOLD_interp_bvbabel_bvbabel_masked_VOI_" + ROI + ".vtc"))

docVMR.load_glm(os.path.join(PATH_VTC, si + '_standard_BOLD_interp.glm'))

docVMR.clear_contrasts()
docVMR.add_contrast("Vertical vs Flicker")
docVMR.set_contrast_string("Vertical vs Flicker")
docVMR.set_contrast_value_at_index(1, -1)
docVMR.set_contrast_value_at_index(3, +1)

docVMR.add_contrast("Diag45 vs Flicker")
docVMR.set_contrast_string("Diag45 vs Flicker")
docVMR.set_contrast_value_at_index(1, -1)
docVMR.set_contrast_value_at_index(4, +1)

docVMR.show_glm()
n_vmps = docVMR.n_maps
print(n_vmps)

docVMR.save_maps(os.path.join(PATH_VTC, si + '_testVMP.vmp'))

docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
docVMR.load_maps(os.path.join(PATH_VTC, si + '_testVMP.vmp'))

#docVMR.show_maps_dialog()
