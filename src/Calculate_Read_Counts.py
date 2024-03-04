import pandas as pd
import argparse as ap
from os import listdir,mkdir
from os.path import isdir
import multiprocessing as mpl
from subprocess import check_output

def linecount(filename):
	return int(check_output(['wc', '-l', filename]).split()[0])

def Job(args):
	filepath, sample, bodysite = args[0], args[1], args[2]
	read_counts = linecount(filepath)
	print({'Bodysite':bodysite, 'Sample':sample, 'Reads':read_counts})
	return {'Bodysite':bodysite, 'Sample':sample, 'Reads':read_counts}

bodysites = ['stool','buccal_mucosa','supragingival_plaque','tongue_dorsum']

data_dir = '/fs/cbcb-lab/mpop/MetaCarvel_paper/hmp_scaffolds/'
outpath = '/fs/cbcb-scratch/hsmurali/Motif-Analysis/Data/ANCHOR/'
num_threads = 32
multithread_params = []
for b in bodysites:
	samples = listdir(data_dir+b+"/")
	for s in samples:
		if s.startswith("SRS"):
			args = (data_dir+b+"/"+s+"/"+s+"_scaffolds/alignment.bed", s, b)
			multithread_params.append(args)

pool = mpl.Pool(int(num_threads))
result = pool.map(func=Job, iterable=multithread_params)
pool.close()
pool.join()

if not isdir(outpath):
	mkdir(outpath)
df = pd.DataFrame(result)
df = df.set_index(['Bodysite','Sample'])
df.to_csv(outpath+"/Read_Counts.txt", sep = "\t")