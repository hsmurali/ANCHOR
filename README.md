# ANCHOR

ANCHOR is a statistical method to determine the mean number of variants that would be detected if reads from one sample were down-sampled to the average sequencing depth of another sample. Briefly, ANCHOR determines the probability that each edge in a bubble, and ultimately the bubble itself, would survive at a lower depth of coverage. The algorithm runs multiple iterations, using probabilities to determine the presence of each edge in a graph and to count the number of bubbles that are retained. The survival characteristics of a bubble are not obvious (Figure 1B). For instance, after down-sampling, an indel can remain an indel, disappear, or transform into a simple or complex structural variant, depending on how the structure of the graph changes as coverage is reduced. 
<tr> 
    <p align="center"><img src="img/ANCHOR.png" width=750 /></p>
</tr>

To run ```ANCHOR``` simply run ```ANCHOR.py```
```
ANCHOR: vAriant Normalization by Coverage and deptH Of Reads. ANCHOR is a
statistical framework to compare the variants detected by MetaCarvel from two
samples of different depths of coverages

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        A fasta file of sequences to cluster
  -g GRAPH, --graph GRAPH
                        Path to the oriented.gml obtained by running
                        MetaCarvel.
  -b BUBBLES, --bubbles BUBBLES
                        Path to the bubbles.txt obtained by running
                        MetaCarvel.
  -o OUTPUT, --output OUTPUT
                        File to write outputs to.
  -n NL, --NL NL        Number of reads you want to downsample to.
  -N NH, --NH NH        Number of reads in the sample.
  -m MATEPAIR_SUPPORT, --matepair_support MATEPAIR_SUPPORT
                        Number of mates used to link two contigs. (default=3)
  -x BOOTSTRAP, --bootstrap BOOTSTRAP
                        Number of times to run ANCHOR
```
