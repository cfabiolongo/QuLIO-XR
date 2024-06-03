from phidias.Lib import *
from actions import *

class QUERY(Belief): pass

# ------- PRE-PROCESSING RULES -------

# Initialiting explorative queries
feed_sparql() / ALL(X) >> [-ALL(X), proc_logform(X)]

# Modelling MST_BINDS shape -----
feed_sparql() / (MST_VAR(X, Y) & MST_BIND(Y, Z)) >> [show_line("\nModelling MTS_BINDS shape..."), -MST_BIND(Y, Z), +MST_BIND(X, Z), feed_sparql()]

# Joining compound entities -----
feed_sparql() / (MST_VAR(X, Y) & MST_COMP(Y, Z)) >> [show_line("\nJoining compound..."), -MST_VAR(X, Y), -MST_COMP(Y, Z), join_cmps(X, Y, Z), feed_sparql()]

# ----- WHO questions -----
# Copular (e.g. Who is Colonel West? )
feed_sparql() / (MST_ACT("Be01:VBZ", E, X, Y) & MST_VAR(Y, "Who01:WP") & MST_VAR(X, Z)) >> [show_line("\nWHO (copular, active) detected..."), -MST_ACT("Be01:VBZ", E, X, Y), -MST_VAR(Y, "Who01:WP"), -MST_VAR(X, Z), feed_who_cop_query_sparql(E, X, Y, "Who", Z), feed_sparql(), finalize_sparql()]
# Transitive (e.g. Who joins the group? Who submitted the article?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(X, "Who01:WP") & MST_VAR(Y, Z)) >> [show_line("\nWHO (active) detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(X, "Who01:WP"), -MST_VAR(Y, Z), feed_who_query_sparql(V, E, X, Y, "Who", Z), feed_sparql(), finalize_sparql()]

# ----- WHAT questions -----
# (e.g. What does Colonel West sell?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(X, W) & MST_VAR(Y, "What01:WP")) >> [show_line("\nWHAT detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(X, W), -MST_VAR(Y, "What01:WP"), feed_what_query_sparql(V, E, X, Y, W), feed_sparql(), finalize_sparql()]

# ----- WHERE questions -----

# Active (Where does Colonel West live?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(E, "Where01:WRB") & MST_VAR(X, W) & MST_VAR(Y, "?")) >> [show_line("\nWHERE (active) detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(E, "Where01:WRB"), -MST_VAR(Y, W), -MST_VAR(Y, "?"), feed_where_sparql(V, E, X, Y, W), finalize_sparql()]
# Passive (Where Colonel West was born?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(E, "Where01:WRB") & MST_VAR(X, "?") & MST_VAR(Y, K)) >> [show_line("\nWHERE (passive) detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(E, "Where01:WRB"), -MST_VAR(Y, K), -MST_VAR(Y, "?"), feed_where_pass_sparql(V, E, X, Y, K), finalize_sparql()]

# ----- WHEN questions -----

# Active (When does Colonel West leave?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(E, "When01:WRB") & MST_VAR(X, W) & MST_VAR(Y, "?")) >> [show_line("\nWHEN (active) detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(E, "When01:WRB"), -MST_VAR(Y, W), -MST_VAR(Y, "?"), feed_when_sparql(V, E, X, Y, W), finalize_sparql()]
# Passive (When Colonel West was born?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(E, "When01:WRB") & MST_VAR(X, "?") & MST_VAR(Y, K)) >> [show_line("\nWHEN (passive) detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(E, "When01:WRB"), -MST_VAR(Y, K), -MST_VAR(Y, "?"), feed_when_pass_sparql(V, E, X, Y, K), finalize_sparql()]



# ----- POLAR questions (Response: True | False) -----

# Copular verbs (Colonel West is American?)
feed_sparql() / (MST_ACT("Be01:VBZ", E, X, Y) & MST_VAR(X, W) & MST_VAR(Y, K)) >> [show_line("\nPOLAR (copular) detected..."), -MST_ACT("Be01:VBZ", E, X, Y), -MST_VAR(X, W), -MST_VAR(Y, K), feed_cop_sparql(E, X, Y, W, K), finalize_sparql()]

# Non-copular verbs (Colonel sells missiles to Nono?)
feed_sparql() / (MST_ACT(V, E, X, Y) & MST_VAR(X, W) & MST_VAR(Y, K)) >> [show_line("\nPOLAR detected..."), -MST_ACT(V, E, X, Y), -MST_VAR(X, W), -MST_VAR(Y, K), feed_query_sparql(V, E, X, Y, W, K), finalize_sparql()]



# ------- FINALIZATION RULES -------

# adding preposition triples for copular
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, Y, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular) + obj-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, Y, O), -MST_VAR(O, V), feed_cop_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, X, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (copular) + subj-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, X, O), -MST_VAR(O, V), feed_cop_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]

# adding preposition triples for non-copular
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_PREP(P, E, O) & MST_VAR(O, V)) >> [show_line("\nEnriching POLAR (non-copular) + verb-prep..."), -PRE_SPARQL(E, X, Y, Q), -MST_PREP(P, E, O), -MST_VAR(O, V), feed_prep_sparql(E, X, Y, P, O, V, Q), finalize_sparql() ]

# adding adjective triples
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_BIND(X, A)) >> [show_line("\nAdding adjective to verb subject..."), -PRE_SPARQL(E, X, Y, Q), -MST_BIND(X, A), feed_adj_sparql(E, X, Y, X, A, Q), finalize_sparql()]
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_BIND(Y, A)) >> [show_line("\nAdding adjective to verb object..."), -PRE_SPARQL(E, X, Y, Q), -MST_BIND(Y, A), feed_adj_sparql(E, X, Y, Y, A, Q), finalize_sparql()]

# adding adverbs triples
finalize_sparql() / (PRE_SPARQL(E, X, Y, Q) & MST_VAR(E, D)) >> [show_line("\nAdding adverb..."), -PRE_SPARQL(E, X, Y, Q), -MST_VAR(E, D), feed_adv_sparql(E, X, Y, D, Q), finalize_sparql()]

# finalizing sparql
finalize_sparql() / PRE_SPARQL(E, X, Y, Q) >> [show_line("\nFinalizing SPARQL..."), -PRE_SPARQL(E, X, Y, Q), +SPARQL(Q)]

+SPARQL(X) >> [show_line("\nQuery SPARQL built: \n", X), submit_sparql(X)]
+PREXR(X) / QUERY(Y) >> [show_line("\nPre-expressive response: \n", X), -QUERY(Y), llm_get(X, Y), show_ct()]


