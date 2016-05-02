import os, hashlib, random
from datetime import datetime

def get_random_filename(filename):
    return hashlib.md5((str(datetime.now()) + filename +
                        str(random.randint(1, 10000))).encode('utf-8')).hexdigest() + os.path.splitext(filename)[1]
