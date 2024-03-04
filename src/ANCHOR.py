from ANCHOR_Utils import *
import argparse as ap

if __name__ == "__main__":
	parser = ap.ArgumentParser(description="ANCHOR: vAriant Normalization by Coverage and deptH Of Reads. "+
											"ANCHOR is a statistical framework to compare the variants detected by MetaCarvel"+
											" from two samples of different depths of coverages")
	parser.add_argument("-g", "--graph", help="Path to the oriented.gml obtained by running MetaCarvel.", required=True)
	parser.add_argument("-b", "--bubbles", help="Path to the bubbles.txt obtained by running MetaCarvel.", required=True)
	parser.add_argument("-o", "--output", help="File to write outputs to.", required=True)
	parser.add_argument("-n", "--NL", help="Number of reads you want to downsample to.", required=True)
	parser.add_argument("-N", "--NH", help="Number of reads in the sample.", required=True)
	parser.add_argument("-m", "--matepair_support", help="Number of mates used to link two contigs. (default=3)", required=False, default = "3")
	parser.add_argument("-x", "--bootstrap", help="Number of times to run ANCHOR. (default=1000)", required=False, default = "1000")
	
	args = parser.parse_args()

	graphpath = args.graph
	bubblespath = args.bubbles
	output = args.output
	NL = int(args.NL)
	NH = int(args.NH)
	m = int(args.matepair_support)
	bootstrap_support = int(args.bootstrap)

	G = nx.read_gml(graphpath)
	bubbles = open(bubblespath).readlines()
	p = NL/(1.0*NH)

	variant_counts = Get_Bubble_Counts(G, bubbles)
	df_anchor = ANCHOR(G, bubbles, p, m, bootstrap_support)
	d_mean = df_anchor.mean().to_dict()
	d_std = df_anchor.std().to_dict()
	
	o = open(output,'w')
	for k in X:
		o.write(k +'\tObserved\tCounts\t' + str(variant_counts[k]))
		o.write(k +'\tANCHOR\tMean\t' + str(d_mean[k]))
		o.write(k +'\tANCHOR\tSD\t' + str(d_std[k]))
	o.write(k +'\tNH\t' + str(NH))
	o.write(k +'\tNL\t' + str(NH))
	o.close()