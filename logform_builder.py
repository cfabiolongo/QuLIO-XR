from phidias.Lib import *
from actions import *


# Logical form BUILDER from LODO KGs

# +Q("Colonel_NNP_West_NNP"), +Q("Cat_NN"), +FEED("the cat ate the food voraciously")

+EXPLO_SPARQL(X) >> [show_line("\nLaunching explorative query SPARQL: \n", X), log("SPARQL: ", X), submit_explo_sparql(X), process_logform()]

# Initialiting explorative queries

# eek_prep(V), seek_adj(S), seek_prep(S), seek_adj(O), seek_prep(O)

process_logform() / LF(I, V, S, O) >> [show_line(f"\nProcessing ",I,"..."), -LF(I, V, S, O), seek_adv(V), seek_adj(S), seek_adj(O), process_logform()]

process_logform() / LF_ADV(I, A) >> [show_line(f"\nProcessing adverb ",A,"..."), -LF_ADV(I, A), process_logform()]
process_logform() / LF_ADJ(I, A) >> [show_line(f"\nProcessing adjective ",A,"..."), -LF_ADJ(I, A), process_logform()]