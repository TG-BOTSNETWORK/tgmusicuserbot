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

API_ID =  int(getenv("API_ID", "11163590"))
API_HASH = getenv("API_HASH", "fa76f31e5f7a64d906d4978dd0e5d3b3")
STRING = getenv("STRING", "BQDgILUAbQN9pexKBryrY_JQWFRhW2iIvLdUFEhx-aGRXkPj3WuRJ3UchPySJorQq4sibiuYk6fv_U_AGIe1YDb7j3_cZ6hBY0v-VvStWdjCCv1Jk2JKqWIb5eDRSvkOthhj5RYnnLYdJfMORAIt8eHWjGYwLHDvGU4tQ50UdCwQ8INvqIGGhFoCJv48E68vg3X5kdMWTkQYaxKLqu8_EnA69vs8wn5RiLUjIScTub-zitTB2HEwjPwLBrAgkbNNrVnamYEWA2MfZsj0hyM-pe8VxOf90BAynis8CySqX-ADoTwzuPg6FNLaGTmfO9RLISjicilvU9xsoaB02azuL2uw-S0KIgAAAAFWwDFOAA")
OWNER_ID = int(os.environ.get("OWNER_ID", "7398382204"))
