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
    STRING = "BQCNjfMAE_sZ0Y_B8jtlKS7f2faXZXffSlgZDv6d044JWkfAirHDd9n9tsWr4ETbzNjutZHz_sNMyKCRk2l5RQGoGF3Bzw7lB_OtacWRQQfZ2M9dgSXmfzbsiSr7ECQzogDxGDOrLKb5HzvfhI7ZvtFt3LMpLqQDR6MM-s0DUqbqCqXOaXVyoSgCzGmVE1VBTFGJBg5e8Yd8l9VkkpIhFtE7_bIxD48gc9BGNWdv7z9Sdzf60Pl8oGhY3FqPYfwb2GWEUS96ZXT0qEriVHY418kFLqvEzZ9SdaubDkNKw7js-k-7gQoBpYePNYBers1VUmEo451RqJIXH8s7uTg1UdUlCgFyPgAAAAFaU4PhAA"
    OWNER_ID = int(os.environ.get("OWNER_ID", "5857041668"))
