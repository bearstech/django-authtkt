import os, glob

# import all test_*.py files
dirname = os.path.dirname(__file__)
for filename in glob.glob(os.path.join(dirname, 'test_*.py')):
    filename = os.path.split(filename)[-1]
    mod, ext = os.path.splitext(filename)
    exec 'from %s import *' % mod
