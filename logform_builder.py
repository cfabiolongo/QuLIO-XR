from phidias.Lib import *
from actions import *


# Logical form BUILDER from LODO KGs

# +Q("Colonel_NNP_West_NNP"), +Q("Cat_NN"), +FEED("the cat ate the food voraciously")

proc_logform(X) >> [show_line("\nLaunching explorative query SPARQL: \n", X), log("SPARQL: ", X), submit_explo_sparql(X), proc_logform()]
# proc_logform(X) >> [show_line("\nLaunching explorative intr. verbs SPARQL: \n", X), log("SPARQL: ", X), submit_intr_explo_sparql(X), proc_logform()]

# Initialiting explorative queries

# seek_prep(V), seek_adj(S), seek_prep(S), seek_adj(O), seek_prep(O)

#  seek_adj(S), seek_adj(O), seek_prep(S), seek_prep(V), seek_adv(V)
proc_logform() / VF(I, V, S, O) >> [show_line(f"\nProc. ",I,"..."), -VF(I, V, S, O), +LF_ORIGIN(I, V, S, O), build_pre(I, V, S, O), seek_prep(V), proc_logform()]

# subject/object related adjective
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_ADJ(I, X, A) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. adj. sub:",A), -LF_ADJ(I, X, A), -PRE_LF(I, E, S, O), join_adj_subj(I, E, S, O, A), proc_logform()]
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_ADJ(I, Y, A) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. adj. obj:",A), -LF_ADJ(I, Y, A), -PRE_LF(I, E, S, O), join_adj_obj(I, E, S, O, A), proc_logform()]

# verb related preposition
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_PREP(I, V, P, K) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. prep. verb:",P), -LF_PREP(I, V, P, K), -PRE_LF(I, E, S, O), join_prep_verb(I, E, S, O, P, K), proc_logform()]
# subject related preposition
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_PREP(I, X, P, K) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. prep. subj:",P), -LF_PREP(I, X, P, K), -PRE_LF(I, E, S, O), join_prep_subj(I, E, S, O, P, K), proc_logform()]
# object related preposition
proc_logform() / (LF_ORIGIN(I, V, X, Y) & LF_PREP(I, Y, P, K) & PRE_LF(I, E, S, O)) >> [show_line(f"\nProc. prep. obj:",P), -LF_PREP(I, Y, P, K), -PRE_LF(I, E, S, O), join_prep_obj(I, E, S, O, P, K), proc_logform()]

# Adverbs
proc_logform() / (PRE_LF(I, V, S, O) & LF_ADV(I, A)) >> [show_line(f"\nProc. adv. ",A,"..."), -LF_ADV(I, A), proc_logform()]

proc_logform() / (LF_ORIGIN(I, V, X, Y) & PRE_LF(I, E, S, O)) >> [show_line(f"\nEnd of operations related to ",I,"."), -LF_ORIGIN(I, V, X, Y), -PRE_LF(I, E, S, O), build_pre_lf(E, S, O), proc_logform()]