import numpy as np

from run_3_1 import runForParticleCount

runForParticleCount(80, prefix="3_3", seed=True, bins=21)
runForParticleCount(64, prefix="3_3", seed=True, bins=17)
runForParticleCount(8, prefix="3_3", seed=True,
                    bins=np.linspace(-0.5, 8.5, 10))
