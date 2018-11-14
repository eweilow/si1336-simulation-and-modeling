import numpy as np

from run_3_1 import runForParticleCount

runForParticleCount(80, "3_1", bins=41)
runForParticleCount(64, "3_1", bins=31)
runForParticleCount(8, "3_1", bins=np.linspace(-0.5, 8.5, 10))
