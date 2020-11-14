# built in library
import string


"""
terminal keys supported on all platforms
"""

UNKNOWN = "UNKNOWN"

US_ENGLISH = "US_ENGLISH"
UK_ENGLISH = "UK_ENGLISH"
CAN_ENGLISH = "CAN_ENGLISH"
AUS_ENGLISH = "AUS_ENGLISH"

SPA_SPANISH = "SPA_SPANISH"
LAT_SPANISH = "LAT_SPANISH"

GER_GERMAN = "GER_GERMAN"

FRE_FRENCH = "FRE_FRENCH"

def _get_keys():
    """
    info: Gets a set of all support keys
    :return: set
    """
    keys = set()
    for key in string.digits + string.ascii_letters + "`-=[]\\;',./~!@#$%^&*()_+{}|:\"<>?":
        keys.add((key, "NORMAL"))

    for key in range(1, 10):
        keys.add(("F{0}".format(key), "SPECIAL"))
        keys.add(("F{0}_SHIFT".format(key), "SPECIAL"))

    for key in ("UP", "DOWN", "LEFT", "RIGHT", "DELETE", "F12", "F12_SHIFT", "BACKSPACE", "ESCAPE"):
        keys.add((key, "SPECIAL"))

    for key in " \t\n":
        keys.add((key, "WHITESPACE"))
    return keys


KEYS = _get_keys()
