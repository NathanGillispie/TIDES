import numpy as np

'''
Real-time Output Functions
'''

def update_output(rt_mf):
    rt_mf._log.note(f'{"="*25} \n')
    rt_mf._log.note(f'Current Time (AU): {rt_mf.current_time:.8f} \n')
    for key, function in rt_mf._observables_functions.items():
        function[1](rt_mf)

    rt_mf._log.note(f'{"="*25} \n')

def _print_energy(rt_mf):
    energy = rt_mf._energy
    rt_mf._log.note(f'Total Energy (AU): {energy[0]} \n')
    if len(energy) > 1:
        for index, fragment in enumerate(energy[1:]):
            rt_mf._log.note(f'Fragment {index + 1} Energy (AU): {fragment} \n')
    if rt_mf.istype('RT_Ehrenfest'):
        kinetic_energy = rt_mf._kinetic_energy
        rt_mf._log.note(f'Total Kinetic Energy (AU): {np.sum(kinetic_energy)} \n')
        rt_mf._log.info(f'Atom Kinetic Energies (AU):')
        for atom in zip(rt_mf.nuc.labels, kinetic_energy):
            rt_mf._log.info(f' {atom[0]} {atom[1]}')
        rt_mf._log.info(' ')
        for index, frag in enumerate(rt_mf.fragments):
            rt_mf._log.note(f'Fragment {index + 1} Kinetic Energy (AU): {np.sum(kinetic_energy[frag.match_indices])} \n')

def _print_mo_occ(rt_mf):
    mo_occ = rt_mf._mo_occ
    rt_mf._log.note(f'Molecular Orbital Occupations: {' '.join(map(str,mo_occ))} \n')

def _print_charge(rt_mf):
    charge = rt_mf._charge
    rt_mf._log.note(f'Total Electronic Charge: {np.real(charge[0])} \n')
    if len(charge) > 1:
        for index, fragment in enumerate(charge[1:]):
            rt_mf._log.note(f'Fragment {index + 1} Electronic Charge: {np.real(fragment)} \n')

def _print_dipole(rt_mf):
    dipole = rt_mf._dipole
    rt_mf._log.note(f'Total Dipole Moment [X, Y, Z] (AU): {' '.join(map(str,dipole[0]))} \n')
    if len(dipole) > 1:
        for index, fragment in enumerate(dipole[1:]):
            rt_mf._log.note(f'Fragment {index + 1} Dipole Moment [X, Y, Z] (AU): {' '.join(map(str,fragment))} \n')

def _print_mag(rt_mf):
    mag = rt_mf._mag
    rt_mf._log.note(f'Total Magnetization [X, Y, Z]: {' '.join(map(str,np.real(mag[0])))} \n')
    if len(mag) > 1:
        for index, fragment in enumerate(mag[1:]):
            rt_mf._log.note(f'Fragment {index + 1} Magnetization [X, Y, Z] (AU): {' '.join(map(str,fragment))} \n')

def _print_nuclei(rt_mf):
    nuclei = rt_mf._nuclei
    rt_mf._log.note(f'Nuclear Coordinates (AU):')
    for atom in zip(nuclei[0], nuclei[1]):
        rt_mf._log.note(f' {atom[0]} \t {'\t'.join(map(lambda x: f"{x:.11f}",atom[1]))}')
    rt_mf._log.note(' ')
    rt_mf._log.info(f'Nuclear Velocities (AU):')
    for atom in zip(nuclei[0], nuclei[2]):
        rt_mf._log.info(f' {atom[0]} \t {'\t'.join(map(lambda x: f"{x:.11f}",atom[1]))}')
    rt_mf._log.info(' ')
    rt_mf._log.debug(f'Nuclear Forces (AU):')
    for atom in zip(nuclei[0], nuclei[3]):
        rt_mf._log.debug(f' {atom[0]} \t {'\t'.join(map(lambda x: f"{x:.11f}",atom[1]))}')
    rt_mf._log.debug(' ')

