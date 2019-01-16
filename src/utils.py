

def var_name(species, bacteria, drug, time_point):
    return species + '_' + bacteria + '_' + drug + '_t' + str(time_point)


def build_encoding(l):
    return {e: i for i, e in enumerate(l)}


def build_decoding(enc):
    return {v: k for k, v in enc.items()}


drug_names = ['CIP', 'AMC.AX', 'SXT', 'S', 'NA.', 'TE', 'CN', 'C']
species_names = ['HUMAN', 'PIG']
site_names = ['KAMPALA', 'MUBENDE']
resistance_level_names = ['S', 'I', 'R']

site_encoding = build_encoding(site_names)
site_decoding = build_decoding(site_encoding)
resistance_encoding = build_encoding(resistance_level_names)
resistance_decoding = build_decoding(resistance_encoding)

def proportion_ci(x, n):
    p = x/n
    se_p = (p*(1-p)/n)**0.5
    z = 1.96    # z-score for the 95% confidence interval
    return p, p - z*se_p, p + z*se_p
