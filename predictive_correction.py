#! /usr/bin/python

"""
Calculate the drift of the RFPA and save the correction factors for the predictive correction.
Author: Ali Aghaeifar <ali.aghaeifar@tuebingen.mpg.de>
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import twixtools
import dico_tools

plt.rcParams['svg.fonttype'] = 'none' # to embed fonts in SVG output
np.set_printoptions(linewidth=np.inf, precision=2)


twix_file_path = sys.argv[1]
print(f'Processing {twix_file_path}')
twix = twixtools.read_twix(twix_file_path)
forward_integral, forward_length = dico_tools.read_dico_memOpt(twix)


# calculate the drift respect to the reference RF (one can skip dummy RFs)
ref_rf    = 0
max_drift = [f[...,[-1]] for f in forward_integral]
max_drift = [100 * (dm/d0[...,[ref_rf]] - 1) for dm, d0 in zip(max_drift, forward_integral)]
print(f'Drifts: {np.array(max_drift[0]).squeeze()} %')

# calculate correction factors 
nTx           = forward_integral[0].shape[0]
corr_interval = 1 # correct for every nth RF

corr_factor_ci1 = forward_integral[0][...,:-1] / forward_integral[0][...,1:]  # ci1 = corrected integral = 1
corr_factor_cix = forward_integral[0][...,:-corr_interval] / forward_integral[0][...,corr_interval:] 
corr_factor_cix = np.hstack((np.ones((nTx, corr_interval)), corr_factor_cix)) # correct for the size
corr_factor_cix[...,:ref_rf] = 1 # no correction before reference RF

predictive_output = os.path.join(os.path.dirname(twix_file_path), 'RFPA_drift_correction.txt')
print(f'Saving correction factors to {predictive_output}')
print('Copy the file above to the scanner customerseq folder.')
np.savetxt(predictive_output, corr_factor_cix.T, fmt='%1.6f', header=f'{corr_factor_cix.shape[1]}\n{corr_factor_cix.shape[0]}\n{corr_interval}', comments='')

