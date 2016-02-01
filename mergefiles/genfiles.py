"""
Generate some test files for mergefiles.py
"""

import random
from os import path

NUM_FILES = 100
NUM_ITEMS_PER_FILE = 100
FILENAME_FORMAT = path.join("testfile","test_%03d")

for n in range(NUM_FILES):
	name = FILENAME_FORMAT % (n)
	print name
	data = [random.randint(1,9999) for i in range(NUM_ITEMS_PER_FILE)]
	data.sort()
	with open(name, "wt") as f:
		for d in data:
			f.write(str(d)+"\n")

