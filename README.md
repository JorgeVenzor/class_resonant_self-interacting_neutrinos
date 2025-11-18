# CLASS with self-interacting neutrinos   

This is modified version of the CLASS code v3.1 (see http://class-code.net and https://github.com/lesgourg/class_public) that computes anisotropies for different neutrino self-interaction models:

For resonant neutrino self-interactions the implementation is based on: 
https://arxiv.org/abs/2303.12792

----------------------------------------

## Implementation

**Resonant neutrino self-interactions:**
We modified the Boltzmann equations in the background and perturbation modules, to account for resonant neutrino self-interactions as presented in arXiv:2309.03941. We use precomputed interaction rates (in this code you compute new ones using the resonance.py script) you will find the precomputed files in the folder tables_Gamma_resonance. 

## Running this code

Tu run the code, you need to set the see the example.ini file. Additionaly, You can find example python scripts in the folder resonance_scripts.

-------------------------------------------

## Using this code

If you use the resonant neutrino self-interactions implementation please cite https://arxiv.org/abs/2303.12792 and https://arxiv.org/abs/2506.07994.

------------------------------------------

