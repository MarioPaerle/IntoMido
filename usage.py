from intomido.composers import Composer

if __name__ == '__main__':
    comp = Composer()
    # Modalità di default ('a'): appende dopo l'ultimo messaggio
    comp.add_fv_pattern([50, 51, 59, '-', 40, 42, 47, '-'], step='1/8', mode='a')
    # Modalità overlay ('o'): pattern che si sovrappone agli altri
    comp.add_fv_pattern([10, 11, 10, 11, 10, 11], step='1/16', mode='o')
    comp.finalize("output.mid")
