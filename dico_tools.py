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
    for mdb in tqdm(mdb_vop, desc='Reading DICO'):
        if mdb.mdh.Counter.Ide == 0:
            DICO_comb.append(mdb.data)
        else:
            DICO_comb[-1] = np.concatenate((DICO_comb[-1],mdb.data), axis=1)

    DICO = []
    shapes = [dico.shape for dico in DICO_comb]  # all shapes
    shapes = sorted(set(shapes), key=shapes.index)  # unique shapes
    for i, shape in enumerate(shapes):
        temp = [dico for dico in tqdm(DICO_comb, desc=f'RF Pulse {i}') if dico.shape == shape]
        DICO.append(np.stack(temp, axis=-1))

    forward = [dico_frw[::2] for dico_frw in DICO]
    reflect = [dico_rfl[1::2] for dico_rfl in DICO]

    return forward, reflect


# memory optimized version, but slower. Only save integral of forward signal
def read_dico_memOpt(twixObj):
    mdb_vop = [mdb for mdb in twixObj[-1]['mdb'] if mdb.is_flag_set('MDH_VOP')]
    if len(mdb_vop) == 0:
        raise ValueError('No DICO data found in the file')
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
    forward_length_unq = sorted(set(forward_length), key=forward_length.index)
    forward_integral   = [forward_integral[:, np.where(np.array(forward_length) == l)[0]] for l in forward_length_unq]

    return forward_integral, forward_length_unq


def plot_drift(twixObj):
    forward_integral, forward_length = read_dico_memOpt(twixObj)
    fig, axes = plt.subplots(nrows=len(forward_integral), ncols=1, figsize=(10, 5 * len(forward_integral)))
    for dico, L, ax in zip(forward_integral, forward_length, axes.flatten()):
        drift = 100 * (dico/dico[:,[0]] - 1)
        ax.plot(drift.squeeze().T)
        ax.set_title(f'RF Length: {L} us')
        ax.set_xlabel('RF Pulse No.')
        ax.set_ylabel('Drift (%)')
    # plt.show()
