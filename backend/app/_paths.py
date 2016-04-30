import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# register externals
EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR, "_externals", "libs")
EXTERNAL_APPS_PATH = os.path.join(BASE_DIR, "_externals", "apps")
APPS_PATH = os.path.join(BASE_DIR, "apps")

# sys path
sys.path = ["", EXTERNAL_APPS_PATH, EXTERNAL_LIBS_PATH, APPS_PATH] + sys.path

# TEST PATH
TEST_ASSETS = os.path.join(BASE_DIR, "_test")
