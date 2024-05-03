from phidias.Lib import *
from actions import *


# ----- WHO questions -----
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, "Who01:WP")) >> [show_line("\nWHO question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, "Who01:WP"), feed_query_sparql(X, Y), feed_sparql()]

# ----- WHAT questions -----
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, "What01:WP")) >> [show_line("\nWHAT question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, "What01:WP"), feed_query_sparql(X, Y), feed_sparql()]

# ----- WHERE questions -----
# Active (Where does Colonel West live?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "Where01:WRB") & MST_VAR(Z, W) & MST_VAR(T, "?")) >> [show_line("\nWHERE (active) question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "Whre01:WRB"), -MST_VAR(Z, W), -MST_VAR(T, "?"), feed_query_sparql(X, Y), feed_sparql()]
# Passive (Where Colonel West was born?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "Where01:WRB") & MST_VAR(Z, "?") & MST_VAR(T, K)) >> [show_line("\nWHERE (passive) question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "Whre01:WRB"), -MST_VAR(Z, K), -MST_VAR(T, "?"), feed_query_sparql(X, Y), feed_sparql()]

# ----- WHEN questions -----
# Active (When does Colonel West leave?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "When01:WRB") & MST_VAR(Z, W) & MST_VAR(T, "?")) >> [show_line("\nWHEN (active) question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "When01:WRB"), -MST_VAR(Z, W), -MST_VAR(T, "?"), feed_query_sparql(X, Y), feed_sparql()]
# Passive (When Colonel West was born?)
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Y, "When01:WRB") & MST_VAR(Z, "?") & MST_VAR(T, K)) >> [show_line("\nWHEN (passive) question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Y, "When01:WRB"), -MST_VAR(Z, K), -MST_VAR(T, "?"), feed_query_sparql(X, Y), feed_sparql()]

# ----- POLAR questions -----
# Copular verbs (Colonel West is American?")
feed_sparql() / (MST_ACT(X, "Be01:VBZ", Z, T) & MST_VAR(Z, W) & MST_VAR(T, K)) >> [show_line("\nPOLAR question detected..."), -MST_ACT(X, "Be01:VBZ", Z, T), -MST_VAR(Z, W), -MST_VAR(T, K), feed_query_sparql(X, Y), feed_sparql()]
# Non-copular verbs (Colonel sells missiles to Nono?")
feed_sparql() / (MST_ACT(X, Y, Z, T) & MST_VAR(Z, W) & MST_VAR(T, K)) >> [show_line("\nPOLAR question detected..."), -MST_ACT(X, Y, Z, T), -MST_VAR(Z, W), -MST_VAR(T, K), feed_query_sparql(X, Y), feed_sparql()]
