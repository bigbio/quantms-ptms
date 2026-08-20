"""
Global variables module.
"""

import logging
from .constants import DECOY_AA_MAP

logger = logging.getLogger(__name__)


def get_decoy_symbol(c: str) -> str:
    """
    Get decoy symbol for amino acid

    Args:
        c: Amino acid character

    Returns:
        str: Decoy symbol
    """
    ret = ""
    src_char = c.upper()

    for k, v in DECOY_AA_MAP.items():
        if v.upper() == src_char:
            ret = k
            break

    return ret
