CLASS with self-interacting neutrinos   
==============================================

This is modified version the CLASS code (see http://class-code.net and https://github.com/lesgourg/class_public) that computes anisotropies for different neutrino self-interaction models:

For resonant neutrino self-interactions the implementation is based on: 
https://arxiv.org/abs/2303.12792

-----------------------------------

Implementation
----------------
2025_November:
We modified the Boltzmann equations in the background and perturbation modules, source/background.c and soruce/perturbations.c, to account for self-interacting neutrinos as presented in arXiv:2309.03941 and reference therein. Following arXiv:1902.00534, we use precompute interaction rates (in this code they can be recomputed using the resonance.py script). 

Implementation
-----------------

Using this code
----------------
Please cite https://arxiv.org/abs/2303.12792 and https://arxiv.org/abs/2506.07994 if you use this code.
-------------------------------

