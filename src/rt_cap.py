import numpy as np
from scipy.linalg import inv

'''
Molecular Orbital Complex Absorbing Potential (CAP)
'''


class MOCAP:
    def __init__(self, expconst, emin, prefac=1, maxval=100, thr=1e-7):
        self.expconst = expconst
        self.emin = emin
        self.prefac = prefac
        self.maxval = maxval
        self.thr = thr

    def calculate_cap(self, rt_mf, fock):
        # Construct fock_orth without CAP
        fock_orth = np.dot(rt_mf.orth.T, np.dot(fock,rt_mf.orth))

        # Calculate MO energies
        mo_energy, mo_orth = np.linalg.eigh(fock_orth)

        # Construct damping terms
        damping_diagonal = []

        for energy in mo_energy:
            energy_corrected = energy - self.emin

            if energy_corrected > 0:
                damping_term = self.prefac * (1 - np.exp(self.expconst* energy_corrected))
                if damping_term < (-1 * self.maxval):
                    damping_term = -1 * self.maxval
                damping_diagonal.append(damping_term)
            else:
                damping_diagonal.append(0)

        damping_diagonal = np.array(damping_diagonal).astype(np.complex128)

        # Construct damping matrix
        damping_matrix = np.diag(damping_diagonal)
        damping_matrix = np.dot(mo_orth, np.dot(damping_matrix, np.conj(mo_orth.T)))

        # Rotate back to ao basis
        transform = inv(rt_mf.orth.T)
        damping_matrix_ao = np.dot(transform, np.dot(damping_matrix, transform.T))
        return 1j * damping_matrix_ao

    def calculate_potential(self, rt_mf):
        if rt_mf.nmat == 1:
            return self.calculate_cap(rt_mf, rt_mf.fock_ao)
        else:
            return np.stack((self.calculate_cap(rt_mf, rt_mf.fock_ao[0]), self.calculate_cap(rt_mf, rt_mf.fock_ao[1])))
