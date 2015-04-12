import itertools


import numpy as np
import os

from msibi import MSIBI, State, Pair, mie


# Clear out the temp files
os.system('rm state*/_* rdfs/pair* potentials/* f_fits.log state*/log.txt')
os.system('rm state*/err.txt')

# Set up global parameters.
rdf_cutoff = 5.0
opt = MSIBI(rdf_cutoff=rdf_cutoff, n_rdf_points=101, pot_cutoff=3.0, smooth_rdfs=False)

# Specify states.
state0 = State(k=1, T=0.5, state_dir='./state0', top_file='target.pdb',
               name='state0', backup_trajectory=False)
state1 = State(k=1, T=1.5, state_dir='./state1', top_file='target.pdb',
               name='state1', backup_trajectory=False)
state2 = State(k=1, T=2.0, state_dir='./state2', top_file='target.pdb',
               name='state2', backup_trajectory=False)
states = [state0, state1, state2]

# Specify pairs.
indices = list(itertools.combinations(range(1468), 2))  # all-all for 1468 atoms
initial_guess = mie(opt.pot_r, 1.0, 1.0)  # 1-D array of potential values.
rdf_targets = [np.loadtxt('rdfs/rdf.target{0:d}.t1t1.txt'.format(i))
               for i in range(3)]

pair0 = Pair('1', '1', initial_guess)
alphas = [1.0, 1.0, 1.0]

# Add targets to pair.
for state, target, alpha in zip(states, rdf_targets, alphas):
    pair0.add_state(state, target, alpha, indices)
pairs = [pair0]

# Do magic.
opt.optimize(states, pairs, n_iterations=5, engine='hoomd')
opt.plot()

