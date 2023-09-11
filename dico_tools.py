import twixtools
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

"""
Reads Siemens rawdata file and returns the DICOs values
Author: Ali Aghaeifar <ali.aghaeifar@tuebingen.mpg.de>
"""

def read_dico(twixObj):
    mdb_vop = [mdb for mdb in twixObj[-1]['mdb'] if mdb.is_flag_set('MDH_VOP')]
      # concatenate segments of RFs longer than 1ms
    DICO_comb = []
    for mdb in tqdm(mdb_vop):
        if mdb.mdh.Counter.Ide == 0:
            DICO_comb.append(mdb.data)
        else:
            DICO_comb[-1] = np.concatenate((DICO_comb[-1],mdb.data), axis=1)

        # split RFs with different lengths
    DICO = []
    shapes = list(set([dico.shape for dico in DICO_comb]))  # unique shapes
    for shape in shapes:
        temp = [dico for dico in DICO_comb if dico.shape == shape]
        DICO.append(np.stack(temp, axis=-1))

    # split forward and reflected signals
    forward = [dico_frw[::2] for dico_frw in DICO]
    reflect = [dico_rfl[1::2] for dico_rfl in DICO]
    return forward, reflect


# memory optimized version, but slower. Only save integral of forward signal
def read_dico_memOpt(twixObj):
    mdb_vop = [mdb for mdb in twixObj[-1]['mdb'] if mdb.is_flag_set('MDH_VOP')]
    forward_integral = []
    forward_length = []
    for mdb in tqdm(mdb_vop, desc = 'Reading DICO'):
        DICO_integral = np.sum(np.abs(mdb.data[::2]), axis=1)
        DICO_length = mdb.data.shape[1]
        if mdb.mdh.Counter.Ide == 0:
            forward_integral.append(DICO_integral)
            forward_length.append(DICO_length)
        else:
            forward_integral[-1] = forward_integral[-1] + DICO_integral
            forward_length[-1] = forward_length[-1] + DICO_length

    forward_integral = np.stack(forward_integral, axis=-1)

    # split RFs with different lengths
    forward_length_unq = list(set(forward_length))
    forward_integral   = [forward_integral[:, np.where(np.array(forward_length) == l)[0]] for l in forward_length_unq]

    return forward_integral, forward_length

def plot_drift(twixObj):
    forward_integral, _ = read_dico_memOpt(twixObj)
    for dico in forward_integral:
        _, ax = plt.subplots()
        ax.plot(forward_integral[0].squeeze().T)
    plt.show()