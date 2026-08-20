"""
Constants and default configurations for pyLuciPHOr2
"""

from . import mass_provider

# Terminal modification positions
NTERM_MOD = -100
CTERM_MOD = 100

# Physical constants - derived from PyOpenMS
WATER_MASS = mass_provider.get_water_mass()
PROTON_MASS = mass_provider.get_proton_mass()
TINY_NUM = 1e-10

# Modification masses - derived from PyOpenMS
PHOSPHO_MOD_MASS = mass_provider.get_phospho_mass()
OXIDATION_MASS = mass_provider.get_oxidation_mass()

# Amino acid masses (monoisotopic) - derived from PyOpenMS ResidueDB
AA_MASSES = mass_provider.get_all_aa_masses()

# Add lowercase letter mass definitions for modification sites (including modification mass)
AA_MASSES.update(
    {
        "s": AA_MASSES["S"] + PHOSPHO_MOD_MASS,  # Ser + phosphorylation
        "t": AA_MASSES["T"] + PHOSPHO_MOD_MASS,  # Thr + phosphorylation
        "y": AA_MASSES["Y"] + PHOSPHO_MOD_MASS,  # Tyr + phosphorylation
        "a": AA_MASSES["A"] + PHOSPHO_MOD_MASS,  # Ala + PhosphoDecoy
        "m": AA_MASSES["M"] + OXIDATION_MASS,  # Met + oxidation
    }
)

# Decoy amino acid mapping
DECOY_AA_MAP = {
    "2": "A",
    "3": "R",
    "4": "N",
    "5": "D",
    "6": "C",
    "7": "E",
    "8": "Q",
    "9": "G",
    "0": "H",
    "@": "I",
    "#": "L",
    "$": "K",
    "%": "M",
    "&": "F",
    ";": "P",
    "?": "W",
    "~": "V",
    "^": "S",
    "*": "T",
    "=": "Y",
}

# Add mass definitions for all decoy symbols
# decoy amino acid mass = original amino acid mass + decoyMass (Phospho mass)
DECOY_MASS = PHOSPHO_MOD_MASS
for decoy_aa, orig_aa in DECOY_AA_MAP.items():
    if decoy_aa not in AA_MASSES and orig_aa in AA_MASSES:
        AA_MASSES[decoy_aa] = AA_MASSES[orig_aa] + DECOY_MASS

# Default configuration
DEFAULT_CONFIG = {
    # Algorithm settings
    "fragment_method": "CID",
    "fragment_mass_tolerance": 0.5,
    "fragment_mass_unit": "Da",
    "min_mz": 150.0,
    # Modification settings
    "target_modifications": ["Phospho (S)", "Phospho (T)", "Phospho (Y)"],
    "neutral_losses": [
        "sty -H3PO4 -97.97690"  # Amino acid list, neutral loss name, mass
    ],
    "decoy_neutral_losses": ["X -H3PO4 -97.97690"],  # Neutral loss for decoy sequences
    "decoy_mass": 79.966331,
    # Peptide settings
    "max_charge_state": 5,
    "max_peptide_length": 40,
    "max_num_perm": 16384,
    # Scoring settings
    "modeling_score_threshold": 0.95,
    "scoring_threshold": 0.0,
    "min_num_psms_model": 50,
    # Performance settings
    "num_threads": 6,
    "rt_tolerance": 0.01,
}

# PSM types
DECOY = 0
REAL = 1
