from os import path, getenv
import os
from dotenv import load_dotenv

load_dotenv()



def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default



class config:

    API_ID = "14688437"
    API_HASH = "5310285db722d1dceb128b88772d53a6"
    STRING = getenv("STRING", "BQCNjfMAML4lfLtuxzfYinyvCYDTuUzvgt_eY7wTMcbzIcRYnVc0G4D9VcLFHUCfCD77ps8GGI2aAYJcNX4gnqGrA21x7dg7itfuOlUexZA4AIUbgNmNPm9KEMhPlBxDKmFxXi8VXFKsaPqMQ3CchAL6j2P2e1yEXlpz6H2nNUVsnyNMYjxMS35rpfUR_LtchG_ClsF4G6xXtl_UUxNzfZW-wSU6x3zx6a016tFRKWDC7ooDIQ_JCo5hrj51sTS9Vg_HvMVxqsEkr-WbMlLJXozXEgr7Nj76aHw6t5-P91vkR5knKMRo4_hv46ikuDyaUjYd_sr8OloFhpH4_FO80NLEuSXJXQAAAAFaU4PhAA")
    OWNER_ID = int(os.environ.get("OWNER_ID", "5857041668"))
