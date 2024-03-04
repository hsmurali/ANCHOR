# ANCHOR

ANCHOR is a statistical method to determine the mean number of variants that would be detected if reads from one sample were down-sampled to the average sequencing depth of another sample. Briefly, ANCHOR determines the probability that each edge in a bubble, and ultimately the bubble itself, would survive at a lower depth of coverage. The algorithm runs multiple iterations, using probabilities to determine the presence of each edge in a graph and to count the number of bubbles that are retained. The survival characteristics of a bubble are not obvious (Figure 1B). For instance, after down-sampling, an indel can remain an indel, disappear, or transform into a simple or complex structural variant, depending on how the structure of the graph changes as coverage is reduced. 
<tr> 
    <p align="center"><img src="img/ANCHOR.pdf" width=750 /></p>
</tr>

