from phidias.Lib import *
from actions import *
from sensors import *
from qa_shifter import *


# Clauses KB manual feeding beliefs
class FEED(Reactor): pass
class QUERY(Reactor): pass
class QUESTION(Reactor): pass

# Front-End STT

# SIMULATING EVENTS


# sentences for reasoning purposes
c1() >> [+FEED("The Colonel West is an American")]
c2() >> [+FEED("Cuba is a hostile nation")]
c3() >> [+FEED("missiles are weapons")]
c4() >> [+FEED("the Colonel West sells missiles to Cuba")]
c5() >> [+FEED("When an American sells weapons to a hostile nation, that American is a criminal")]

# Query
#q() >> [+QUERY("The Colonel West is a criminal")]
q() >> [+FEED("Most of these therapeutic agents require intracellular uptake for their therapeutic effect because their site of action is within the cell")]


# testing rules
+FEED(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), log("Feed",X), show_ct(), +LISTEN("TEST")]
+QUERY(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), log("Query",X), show_ct(), +REASON("TEST")]
+PROCESS_STORED_MST("OK") / LISTEN("TEST") >> [show_line("\nGot it.\n"), create_onto("NOMINAL"), process_rule(), -LISTEN("TEST")]
+PROCESS_STORED_MST("OK") / REASON("TEST") >> [show_line("\nGot it.\n"), create_onto("NOMINAL"), -REASON("TEST")]
+QUESTION(X) >> [reset_ct(),  log("Query", X), assert_sequence(X), getcand(), tense_debt_paid(), show_ct()]


+STT(X) / (WAKE("ON") & LISTEN("ON")) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), show_ct(), +ANSWER(X), Timer(W).start()]
+STT(X) / (WAKE("ON") & REASON("ON")) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), show_ct(), Timer(W).start()]


# Query KB
+PROCESS_STORED_MST("OK") / (WAKE("ON") & REASON("ON")) >> [show_line("\nGot it.\n"), create_onto("NOMINAL")]

# Nominal ontology assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+PROCESS_STORED_MST("OK") / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nGot it.\n"), create_onto("NOMINAL"), process_rule()]
# processing rule
process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!\n"), -IS_RULE("TRUE"), create_onto("RULE")]

# Ontology creation
create_onto(T) >> [preprocess_onto(T), InitOnto(), process_onto(), show_line("\n------------- Done:", T, "\n")]

