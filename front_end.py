from phidias.Lib import *
from actions import *

# Clauses KB manual feeding beliefs
class FEED(Reactor): pass
class QUERY(Belief): pass
class Q(Reactor): pass


# sentences for reasoning purposes
c1() >> [+FEED("Colonel West is American")]
c2() >> [+FEED("Nono is a hostile nation")]
c3() >> [+FEED("Missiles are weapons")]
c4() >> [+FEED("Colonel West sells missiles to Nono")]
c5() >> [+FEED("When an American sells weapons to a hostile nation, that American is a criminal")]

# start RESTful agent
start() >> [show_line("\n--- Starting RESTful agent...\n"), +MODE(AGENT_MODE)]

+Q(X) / MODE("LLM") >> [reset_ct(), log("Q", X), show_ct(), +ALL(X), feed_sparql()]
+QUERY(X) / MODE("LLM") >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_sparql(), log("Query", X), show_ct()]
#+QUERY(X) / MODE("LLM") >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), log("Query",X), show_ct()]

+Q(X) >> [reset_ct(), log("Q", X), show_ct(), +ALL(X), feed_sparql()]
+QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_sparql(), log("Query", X), show_ct()]
#+QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), log("Query",X), show_ct()]

# testing rules
+FEED(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), log("Feed", X), show_ct(), +LISTEN("TEST")]
+PROCESS_STORED_MST("OK") / LISTEN("TEST") >> [show_line("\nGot it.\n"), create_onto(), process_rule(), -LISTEN("TEST")]
+PROCESS_STORED_MST("OK") / REASON("TEST") >> [show_line("\nProcessing query.....\n"), create_sparql(), -REASON("TEST")]

# Nominal ontology assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+PROCESS_STORED_MST("OK") / LISTEN("ON") >> [show_line("\nGot it.\n"), create_onto(), process_rule()]
# processing rule
process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!\n"), -IS_RULE("TRUE"), create_onto("RULE")]

# Ontology creation
create_onto() >> [preprocess_onto(), InitOnto(), process_onto(), show_line("\n------------- Done:", T, "\n")]
