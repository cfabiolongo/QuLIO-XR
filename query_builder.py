from phidias.Lib import *
from actions import *

class SPARQL(Reactor): pass

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
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, K)) >> [show_line("\nPOLAR detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, K), feed_query_sparql(X, Y), finalize_sparql()]


# finalizing sqarql with satellite conditions
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, Y, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular)+prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, Y, O), -MST_VAR(O, V), feed_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, X, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular)+prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, X, O), -MST_VAR(O, V), feed_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]

finalize_sparql() / PRE_SPARQL(E, X, Y, Q) >> [show_line("\nFinalizing POLAR verb-prep (copular)..."), -PRE_SPARQL(E, X, Y, Q), +SPARQL(Q)]


# finalize_sparql() / (MST_ACT("Be01:VBZ", X, Z, T, W, K) & MST_PREP(T, D, I) & MST_VAR(I, V)) >> [show_line("\nFinalizing POLAR verb-prep (copular) question..."), -MST_ACT("Be01:VBZ", X, Z, T, W, K), -MST_PREP(T, D, I), -MST_VAR(I, V), feed_cop_sparql(W, K)]
# finalize_sparql() / MST_ACT("Be01:VBZ", X, Z, T, W, K) >> [show_line("\nFinalizing POLAR (copular) question..."), -MST_ACT("Be01:VBZ", X, Z, T, W, K), feed_cop_sparql(W, K)]


+SPARQL(X) >> [show_line("\nQuery SPARQL built: \n", X), log("SPARQL: ", X), submit_query_sparql(X)]
