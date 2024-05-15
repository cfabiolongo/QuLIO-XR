from phidias.Lib import *
from actions import *


# Logical form BUILDER from LODO KGs

# +Q("Colonel_NNP_West_NNP"), +Q("Cat_NN"), +FEED("the cat ate the food voraciously")

+EXPLO_SPARQL(X) >> [show_line("\nLaunching explorative query SPARQL: \n", X), log("SPARQL: ", X), submit_explo_sparql(X), proc_logform()]

# Initialiting explorative queries

# seek_prep(V), seek_adj(S), seek_prep(S), seek_adj(O), seek_prep(O)

# process_logform() / LF(I, V, S, O) >> [show_line(f"\nProcessing ",I,"..."), -LF(I, V, S, O), seek_adv(V), seek_prep(V), seek_adj(S), seek_adj(O), seek_prep(S), process_logform()]
proc_logform() / LF(I, V, S, O) >> [show_line(f"\nProc. ",I,"..."), -LF(I, V, S, O), +LF_ORIGIN(I, V, S, O), build_pre(I, V, S, O), seek_adj(S), proc_logform()]

proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_ADJ(I, X, A) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. adj. sub:",A), -LF_ADJ(I, X, A), -PRE_LF(I, V, S, O), join_adj_subj(I, E, S, O, A), proc_logform()]
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_ADJ(I, Y, A) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. adj. obj:",A), -LF_ADJ(I, Y, A), -PRE_LF(I, V, S, O), join_adj_obj(I, E, S, O, A), proc_logform()]

#proc_logform() / LF_PREP(I, P, O) >> [show_line(f"\nProc. prep.  ",A,"..."), -LF_PREP(I, P, O), seek_adj(O), seek_prep(S), proc_logform()]
# proc_logform() / (PRE_LF(I, V, S, O) & LF_ADV(I, A)) >> [show_line(f"\nProc. adv. ",A,"..."), -LF_ADV(I, A), proc_logform()]

proc_logform() / LF(I, V, S, O) >> [show_line(f"\nEnd of operations related to ",I,".")]