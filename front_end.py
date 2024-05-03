from actions import *
from qa_shifter import *


# Clauses KB manual feeding beliefs
class FEED(Reactor): pass
class QUERY(Reactor): pass

# sentences for reasoning purposes
c1() >> [+FEED("Colonel West is an American")]
c2() >> [+FEED("Cuba is a hostile nation")]
c3() >> [+FEED("missiles are weapons")]
c4() >> [+FEED("the Colonel West sells missiles to Cuba")]
c5() >> [+FEED("When an American sells weapons to a hostile nation, that American is a criminal")]

# Query
q() >> [+QUERY("Colonel West sells missiles to Cuba")]

# testing rules
+FEED(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), log("Feed",X), show_ct(), +LISTEN("TEST")]
+QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_sparql(), log("Query",X), show_ct()]
+PROCESS_STORED_MST("OK") / LISTEN("TEST") >> [show_line("\nGot it.\n"), create_onto("NOMINAL"), process_rule(), -LISTEN("TEST")]
+PROCESS_STORED_MST("OK") / REASON("TEST") >> [show_line("\nProcessing query.....\n"), create_sparql(), -REASON("TEST")]

# Nominal ontology assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+PROCESS_STORED_MST("OK") / LISTEN("ON") >> [show_line("\nGot it.\n"), create_onto("NOMINAL"), process_rule()]
# processing rule
process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!\n"), -IS_RULE("TRUE"), create_onto("RULE")]

# Ontology creation
create_onto(T) >> [preprocess_onto(T), InitOnto(), process_onto(), show_line("\n------------- Done:", T, "\n")]
