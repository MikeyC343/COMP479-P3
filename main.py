import sys
from preprocesser import preProcess
from merge import mergeBlocks
from calculateWeights import calculate


def indexGeneration(memorysize):
	preProcess(memorysize)

	mergeBlocks()

	calculate()

if __name__ == "__main__":
	indexGeneration(int(sys.argv[1]))