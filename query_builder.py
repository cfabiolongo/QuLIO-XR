from phidias.Lib import *
from actions import *

class SPARQL(Reactor): pass

# ----- Modelling MST_BINDS shape -----
feed_sparql() / (MST_VAR(X, Y) & MST_BIND(Y, Z)) >> [show_line("\nModelling MTS_BINDS shape..."), -MST_BIND(Y, Z), +MST_BIND(X, Z), feed_sparql()]

# ----- Joining compound entities -----
feed_sparql() / (MST_VAR(X, Y) & MST_COMP(Y, Z)) >> [show_line("\nJoining compound..."), -MST_VAR(X, Y), -MST_COMP(Y, Z), join_cmps(X, Y, Z), feed_sparql()]

# ----- WHO questions -----
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, "Who01:WP")) >> [show_line("\nWHO detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, "Who01:WP"), feed_query_sparql(X, Y), feed_sparql()]

# ----- WHAT questions -----
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, "What01:WP")) >> [show_line("\nWHAT detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, "What01:WP"), feed_query_sparql(X, Y), feed_sparql()]

# ----- WHERE questions -----

# Active (Where does Colonel West live?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "Where01:WRB") & MST_VAR(Z, W) & MST_VAR(T, "?")) >> [show_line("\nWHERE (active) detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "Where01:WRB"), -MST_VAR(Z, W), -MST_VAR(T, "?"), feed_query_sparql(X, Y)]
# Passive (Where Colonel West was born?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "Where01:WRB") & MST_VAR(Z, "?") & MST_VAR(T, K)) >> [show_line("\nWHERE (passive) detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "Where01:WRB"), -MST_VAR(Z, K), -MST_VAR(T, "?"), feed_query_sparql(X, Y)]

# ----- WHEN questions -----

# Active (When does Colonel West leave?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "When01:WRB") & MST_VAR(Z, W) & MST_VAR(T, "?")) >> [show_line("\nWHEN (active) detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "When01:WRB"), -MST_VAR(Z, W), -MST_VAR(T, "?"), feed_query_sparql(X, Y)]
# Passive (When Colonel West was born?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "When01:WRB") & MST_VAR(Z, "?") & MST_VAR(T, K)) >> [show_line("\nWHEN (passive) detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "When01:WRB"), -MST_VAR(Z, K), -MST_VAR(T, "?"), feed_query_sparql(X, Y)]

# ----- POLAR questions -----

# Copular verbs (Colonel West is American?")
feed_sparql() / (MST_ACT("Be01:VBZ", E, X, Y) & MST_VAR(X, W) & MST_VAR(Y, K)) >> [show_line("\nPOLAR (copular) detected..."), -MST_ACT("Be01:VBZ", E, X, Y), -MST_VAR(X, W), -MST_VAR(Y, K), feed_cop_sparql(E, X, Y, W, K), finalize_sparql()]

# Non-copular verbs (Colonel sells missiles to Nono?")
feed_sparql() / (MST_ACT(Z, E, X, Y) & MST_VAR(X, W) & MST_VAR(Y, K)) >> [show_line("\nPOLAR detected..."), -MST_ACT(Z, E, X, Y), -MST_VAR(X, W), -MST_VAR(Y, K), feed_query_sparql(Z, E, X, Y, W, K), finalize_sparql()]


# adding preposition triples for copular
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, Y, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular) + obj-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, Y, O), -MST_VAR(O, V), feed_cop_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, X, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular) + subj-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, X, O), -MST_VAR(O, V), feed_cop_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]

# adding preposition triples for non-copular
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, E, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (non-copular) + verb-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, E, O), -MST_VAR(O, V), feed_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]

# adding adjective triples
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_BIND(X, A)) >> [show_line("\nAdding adjective to verb subject..."), -PRE_SPARQL(E, X, Y, Q), -MST_BIND(X, A), feed_adj_sparql(E, X, Y, X, A, Q), finalize_sparql()]
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_BIND(Y, A)) >> [show_line("\nAdding adjective to verb object..."), -PRE_SPARQL(E, X, Y, Q), -MST_BIND(Y, A), feed_adj_sparql(E, X, Y, Y, A, Q), finalize_sparql()]


finalize_sparql() / PRE_SPARQL(E, X, Y, Q) >> [show_line("\nFinalizing SPARQL..."), -PRE_SPARQL(E, X, Y, Q), +SPARQL(Q)]


+SPARQL(X) >> [show_line("\nQuery SPARQL built: \n", X), log("SPARQL: ", X), submit_query_sparql(X)]
