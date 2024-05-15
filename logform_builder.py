from phidias.Lib import *
from actions import *


# Logical form BUILDER from LODO KGs

# +Q("Colonel_NNP_West_NNP")

+EXPLO_SPARQL(X) >> [show_line("\nLaunching explorative query SPARQL: \n", X), log("SPARQL: ", X), submit_explo_sparql(X), process_logform()]

# Initialiting explorative queries
process_logform() / LF(V, S, O) >> [show_line(f"\nProcessing ",V," with subject: ",S," / object: ",O,"..."), -LF(V, S, O), process_logform()]