from ANCHOR_Utils import *
import multiprocessing as mpl

def Job(args):
	graph, bubbles, sample, Bodysite, NL, NH = args[0], args[1], args[2], args[3], args[4], args[5]
	G = nx.read_gml(graph)
	bubbles = open(bubbles).readlines()
	p = NL/(1.0*NH)

	X = Get_Bubble_Counts(G, bubbles)
	df_anchor = ANCHOR(G, bubbles, p)
	d_mean = df_anchor.mean().to_dict()
	d_std = df_anchor.std().to_dict()
	d = {}

	for k in X:
		d[(k,'Observed','Counts')] = X[k]
		d[(k,'Anchor','Mean')] = d_mean[k]
		d[(k,'Anchor','Std')] = d_std[k]
		d[('Sample','','')] = sample
		d[('Bodysite','','')] = Bodysite
		d[('NH','','')] = NH
		d[('NL','','')] = NL
	return d
		
bodysites = ['stool','buccal_mucosa','supragingival_plaque','tongue_dorsum']

data_dir = '/fs/cbcb-lab/mpop/MetaCarvel_paper/hmp_scaffolds/'
outpath = '/fs/cbcb-scratch/hsmurali/Motif-Analysis/Data/ANCHOR/'
read_counts = '/fs/cbcb-scratch/hsmurali/Motif-Analysis/Data/ANCHOR/metacarvel_sample_feature_counts.xlsx'
num_threads = 32

df_read_counts = pd.read_excel(read_counts)
df_grp = df_read_counts.groupby('BODYSITE').median()
df_grp = df_grp.loc[bodysites]
NL = df_grp['READ_COUNT_R1'].min()

print(df_grp)
print(NL)

df_read_counts = df_read_counts.set_index(['BODYSITE'])
multithread_params = []

for b in bodysites:
	df_sel = df_read_counts.loc[b]
	samples = df_sel['#SAMPLE'].tolist()
	Read_Counts = df_sel['READ_COUNT_R1'].tolist()
	for i in range(len(samples)):
		graph_path = data_dir+b+'/'+samples[i]+'/'+samples[i]+'_scaffolds/oriented.gml'
		bubbles_path = data_dir+b+'/'+samples[i]+'/'+samples[i]+'_scaffolds/bubbles.txt'
		args = (graph_path, bubbles_path, b, samples[i], NL, Read_Counts[i])
		multithread_params.append(args)

pool = mpl.Pool(int(num_threads))
result = pool.map(func=Job, iterable=multithread_params)
pool.close()
pool.join()

df = pd.DataFrame(result)
df.columns = pd.MultiIndex.from_tuples(df.columns)
df.to_excel(outpath+"/ANCHOR.counts.xlsx")
