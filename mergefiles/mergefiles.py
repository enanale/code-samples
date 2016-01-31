"""

Merge a collection sorted files into one combined sorted file.

"""

from os import path
import glob
import heapq


class FileDataIterator:
	"""
	Wrap a file into a iterator of over its integer data
	"""
	def __init__(self, filename):
		self.filename = filename
		self.f = open(filename,"r")

	def __iter__(self):
		return self

	def next(self):
		line = self.f.readline()
		if line == '':
			self.f.close()
			raise StopIteration()
		return int(line)

def mergefiles( infiles, outfile ):
	"""
	Merges sorted data from many sorted files.  Data must be sorted within files.
	Uses iterators and heapq.merge so that everything doesn't have to be loaded into memory
	"""
	sorted_it = heapq.merge(*[FileDataIterator(p) for p in infiles])
	with open( outfile, "wt" ) as of:
		for d in sorted_it:
			of.write(str(d)+"\n")

def test():
	infiles = glob.glob(path.join("testfile","test_*"))
	mergefiles( infiles, "sorted" )ß
	return

if __name__ == "__main__":
	test()