from intomido.composers import Composer
import numpy as np

if __name__ == '__main__':
    comp = Composer()
    pattern = np.array([50, 51, 59, 61, 40, 42, 47, 51], dtype=object)
    comp.add_fv_pattern(pattern + 12, step='1/8', mode='a')
    # Modalità overlay ('o'): pattern che si sovrappone agli altri
    comp.add_fv_pattern([10, 11, 10, 11, 10, 11], step='1/16', mode='o')
    comp.finalize("output.mid")
