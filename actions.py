from parse_en import *
from nl_to_fol import *

from phidias.Types import *
import configparser
from datetime import datetime
from owlready2 import *


FILE_NAME = config.get('AGENT', 'FILE_NAME')

try:
    my_onto = get_ontology(FILE_NAME).load()
    print("\nLoading existing "+FILE_NAME+" file...")
except IOError:
    my_onto = get_ontology("http://test.org/"+FILE_NAME)
    print("\nCreating new "+FILE_NAME+" file...")
    print("\nPlease Re-Run Qu-LIO-XR.")
    my_onto.save(file=FILE_NAME, format="rdfxml")
    exit()


with my_onto:
    class Id(Thing):
        pass

    class Verb(Thing):
        pass

    class Adjective(Thing):
        pass

    class Adverb(Thing):
        pass

    class Entity(Thing):
        pass

    class Preposition(Thing):
        pass

    class hasAdj(ObjectProperty):
        pass

    class hasAdv(ObjectProperty):
        pass

    class hasObject(ObjectProperty):
        pass

    class hasSubject(ObjectProperty):
        pass

    class hasPrep(ObjectProperty):
        pass

    class hasId(ObjectProperty):
        pass

    class hasDate(DataProperty):
        pass

    class hasPlace(DataProperty):
        pass

    class hasValue(DataProperty):
        range = [int]


owl_obj_dict = {}


config = configparser.ConfigParser()
config.read('config.ini')

cnt = itertools.count(1)
dav = itertools.count(1)

VERBOSE = config.getboolean('PARSING', 'VERBOSE')
LANGUAGE = config.get('PARSING', 'LANGUAGE')
ASSIGN_RULES_LEMMAS = config.get('PARSING', 'ASSIGN_RULES_LEMMAS').split(", ")
ASSIGN_RULES_POS = config.get('PARSING', 'ASSIGN_RULES_POS').split(", ")
AXIOMS_WORDS = config.get('PARSING', 'AXIOMS_WORDS').split(", ")

WAIT_TIME = config.getint('AGENT', 'WAIT_TIME')
LOG_ACTIVE = config.getboolean('AGENT', 'LOG_ACTIVE')

INCLUDE_ACT_POS = config.getboolean('POS', 'INCLUDE_ACT_POS')
INCLUDE_NOUNS_POS = config.getboolean('POS', 'INCLUDE_NOUNS_POS')
INCLUDE_ADJ_POS = config.getboolean('POS', 'INCLUDE_ADJ_POS')
INCLUDE_PRP_POS = config.getboolean('POS', 'INCLUDE_PRP_POS')
INCLUDE_ADV_POS = config.getboolean('POS', 'INCLUDE_ADV_POS')
OBJ_JJ_TO_NOUN = config.getboolean('POS', 'OBJ_JJ_TO_NOUN')

parser = Parse(VERBOSE)
m = ManageFols(VERBOSE, LANGUAGE)



# Ontology creation procedures
class create_onto(Procedure): pass
class process_rule(Procedure): pass
class process_onto(Procedure): pass
class create_adj(Procedure): pass
class create_adv(Procedure): pass
class create_verb(Procedure): pass
class create_assrule(Procedure): pass
class create_gnd_prep(Procedure): pass
class create_prep(Procedure): pass
class aggr_ent(Procedure): pass
class create_body(Procedure): pass
class create_head(Procedure): pass
class finalize_onto(Procedure): pass
class create_ner(Procedure): pass
class valorize(Procedure): pass

# initialize Clauses Kb
# mode reactors
class LISTEN(Belief): pass
class REASON(Belief): pass
class IS_RULE(Belief): pass
class WAIT(Belief): pass
class ANSWER(Reactor): pass

# domotic reactive routines
class r1(Procedure): pass
class r2(Procedure): pass

# domotic direct commands
class d1(Procedure): pass
class d2(Procedure): pass

# domotic sensor simulatons
class s1(Procedure): pass
class s2(Procedure): pass

# Fol reasoning utterances
class c1(Procedure): pass
class c2(Procedure): pass
class c3(Procedure): pass
class c4(Procedure): pass
class c5(Procedure): pass
class c6(Procedure): pass

# Fol query utterance
class q(Procedure): pass

# normal requests beliefs
class GROUND(Belief): pass
class PRE_MOD(Belief): pass
class MOD(Belief): pass
class PRE_INTENT(Belief): pass
class INTENT(Reactor): pass



# action
class ACTION(Belief): pass
# preposition
class PREP(Belief): pass
# ground
class GND(Belief): pass
# adverb
class ADV(Belief): pass
# adjective
class ADJ(Belief): pass
# id individual
class ID(Belief): pass
# rule accumulator
class RULE(Belief): pass
# subject accumulator
class SUBJ(Belief): pass
# subject accumulator
class VALUE(Belief): pass



# parse rule beliefs
class DEP(Belief): pass
class MST_ACT(Belief): pass
class MST_VAR(Belief): pass
class MST_PREP(Belief): pass
class MST_BIND(Belief): pass
class MST_COMP(Belief): pass
class MST_COND(Belief): pass
class parse_deps(Procedure): pass
class feed_mst(Procedure): pass
class PROCESS_STORED_MST(Reactor): pass
class NER(Belief): pass
class feed_sparql(Procedure): pass
class finalize_sparql(Procedure): pass

class SPARQL(Reactor): pass
class PRE_SPARQL(Belief): pass

class log(Action):
    """log direct assertions from keyboard"""
    def execute(self, *args):
        a = str(args).split("'")

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\n"+a[1]+": "+a[5])




class reset_ct(Action):
    """Reset execution time"""
    def execute(self):
        parser.set_start_time()


class show_ct(Action):
    """Show execution time"""
    def execute(self):
        ct = parser.get_comp_time()
        print("\nExecution time: ", ct)

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\nExecution time: "+str(ct))


class preprocess_onto(Action):
    """Producting beliefs to feed the Ontology Builder"""

    def execute(self, *args):
        type = str(args[0]())

        print("\n--------- NEW ONTOLOGY ---------\n ")
        print("type: " + type + "\n")

        deps = parser.get_last_deps()
        ners = parser.get_last_ner()
        print("NER: ", ners)
        for ner in ners:
            n = ner.split(", ")
            self.assert_belief(NER(n[0][1:], n[1][:-1]))

        for i in range(len(deps)):
            governor = self.get_lemma(deps[i][1]).capitalize() + ":" + self.get_pos(deps[i][1])
            dependent = self.get_lemma(deps[i][2]).capitalize() + ":" + self.get_pos(deps[i][2])
            deps[i] = [deps[i][0], governor, dependent]

        print("\n" + str(deps))

        MST = parser.get_last_MST()
        print("\nMST: \n" + str(MST))
        print("\nGMC_SUPP: \n" + str(parser.GMC_SUPP))
        print("\nGMC_SUPP_REV: \n" + str(parser.GMC_SUPP_REV))
        print("\nLCD: \n" + str(parser.LCD))

        # MST varlist correction on cases of adj-obj
        if OBJ_JJ_TO_NOUN is True:
            for v in MST[1]:
                if self.get_pos(v[1]) in ['JJ', 'JJR', 'JJS']:
                    old_value = v[1]
                    new_value = self.get_lemma(v[1]) + ":NNP"
                    v[1] = new_value

                    new_value_clean = parser.get_lemma(new_value.lower())[:-2]
                    print("\nadj-obj correction...", new_value_clean)

                    # checking if the lemma has a disambiguation
                    if new_value_clean in parser.GMC_SUPP_REV:
                        parser.LCD[parser.GMC_SUPP_REV[new_value_clean]] = new_value_clean

                    # binds correction
                    for b in MST[3]:
                        if b[0] == old_value:
                            b[0] = new_value

        vect_LR_fol = m.build_LR_fol(MST, 'e')

        if len(vect_LR_fol) == 0:
            print("\n --- IMPROPER VERBAL PHRASE COSTITUTION ---")
            self.assert_belief(ANSWER("Improper verbal phrase"))
            return

        CHECK_IMPLICATION = m.check_implication(vect_LR_fol)
        dclause = vect_LR_fol[:]

        if CHECK_IMPLICATION:
            dclause[1] = ["==>"]
            self.assert_belief(RULE("->"))

        print("\nvect_LR_fol:\n" + str(dclause))

        ent_root = self.get_ent_ROOT(deps)

        # IMPLICATION CASES
        if dclause[1][0] == "==>":

            print("\nPROCESSING LEFT HAND-SIDE...")
            self.process_fol(dclause[0], "LEFT", ent_root)

            print("\nPROCESSING RIGHT HAND-SIDE...")
            self.process_fol(dclause[2], "RIGHT", ent_root)

        # FLAT CASES
        else:
            self.process_fol(dclause, "FLAT", ent_root)

    def get_ent_ROOT(self, deps):
        for d in deps:
            if d[0] == "ROOT":
                return d[1]

    def get_dav_rule(self, fol, ent_root):
        for f in fol:
            if f[0] == ent_root:
                return f[1]
        return False

    def check_neg(self, word, language):
        pos = wordnet.ADV
        syns = wordnet.synsets(word, pos=pos, lang=language)
        for synset in syns:
            if str(synset.name()) in ['no.r.01', 'no.r.02', 'no.r.03', 'not.r.01']:
                return True
        return False

    def get_nocount_lemma(self, lemma):
        lemma_nocount = ""
        total_lemma = lemma.split("_")

        for i in range(len(total_lemma)):
            if i == 0:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[1]
            else:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[1] + "_" + lemma_nocount
        return lemma_nocount


    def process_fol(self, vect_fol, id, ent_root):

        # prepositions
        for v in vect_fol:
            if len(v) == 3:
                label = self.get_nocount_lemma(v[0])
                if id == "LEFT":
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")

                else:
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")


        # actions
        for v in vect_fol:
            if len(v) == 4:

                label = self.get_nocount_lemma(v[0])
                if INCLUDE_ACT_POS:
                    lemma = label
                else:
                    lemma = parser.get_lemma(label)

                if id == "FLAT" and ent_root == v[0]:
                    self.assert_belief(ACTION("ROOT", str(id), lemma, v[1], v[2], v[3]))
                    print("ACTION(ROOT, " + str(id) + ", " + lemma + ", " + v[1] + ", " + v[2] + ", " + v[3] + ")")
                else:
                    self.assert_belief(ACTION(str(id), lemma, v[1], v[2], v[3]))
                    print("ACTION(" + str(id) + ", " + lemma + ", " + v[1] + ", " + v[2] + ", " + v[3] + ")")


        # nouns
        for v in vect_fol:
            if len(v) == 2:
                if self.get_pos(v[0]) in ['NNP', 'NNPS', 'PRP', 'NN', 'NNS', 'PRP', 'PRP$']:
                    label = self.get_nocount_lemma(v[0])
                    if INCLUDE_NOUNS_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(GND(str(id), v[1], lemma))
                    print("GND(" + str(id) + ", " + v[1] + ", " + lemma + ")")

        # adjectives, adverbs
        for v in vect_fol:
            if self.get_pos(v[0]) in ['JJ', 'JJR', 'JJS']:
                label = self.get_nocount_lemma(v[0])
                if id == "LEFT":
                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADJ(str(id), v[1], lemma))
                    print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                else:
                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADJ(str(id), v[1], lemma))
                    print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

            elif self.get_pos(v[0]) in ['RB', 'RBR', 'RBS', 'RP']:

                label = self.get_nocount_lemma(v[0])

                if id == "LEFT":
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADV(str(id), v[1], lemma))
                    print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                else:
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADV(str(id), v[1], lemma))
                    print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")

        # cardinal numbers
        for v in vect_fol:
            if len(v) == 2:
                if self.get_pos(v[0]) == "CD":
                    label = self.get_nocount_lemma(v[0])
                    if INCLUDE_NOUNS_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(VALUE(str(id), v[1], lemma))
                    print("VALUE(" + str(id) + ", " + v[1] + ", " + lemma + ")")

    def get_pos(self, s):
        first = s.split('_')[0]
        s_list = first.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class create_sparql(Action):
    """create sparql query from MST"""
    def execute(self, *args):
        print("\n--------- MST ---------\n ")

        MST = parser.get_last_MST()
        print("\nMST: \n" + str(MST))
        print("\nGMC_SUPP: \n" + str(parser.GMC_SUPP))
        print("\nGMC_SUPP_REV: \n" + str(parser.GMC_SUPP_REV))
        print("\nLCD: \n" + str(parser.LCD))


# ---------------------- Ontology creation Section


class WFR(ActiveBelief):
    """check if R is a Well Formed Rule"""
    def evaluate(self, arg):

        rule = str(arg).split("'")[3]

        if rule[0] != "-" and rule[-1] != ">":
            return True
        else:
            return False


class declareRule(Action):
    """assert an SWRL rule"""
    def execute(self, arg1):
        rule_str = str(arg1).split("'")[3]

        print("FINALE: ", rule_str)

        with my_onto:
           rule = Imp()
           rule.set_as_rule(rule_str)


class fillActRule(Action):
    """fills a rule with a verbal action"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", ".")
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        # creating subclass of Verb
        types.new_class(verb, (Verb,))

        if rule[0] == "-":
            rule = "hasSubject(?"+dav+", ?"+subj+"), hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasSubject(?"+dav+", ?"+subj+"), hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillPassActRule(Action):
    """fills a rule with a passive verbal action"""
    def execute(self, arg1, arg2, arg3, arg4):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", ".")
        dav = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3].replace(":", ".")

        # creating subclass of Verb
        types.new_class(verb, (Verb,))

        if rule[0] == "-":
            rule = "hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasObject(?"+dav+", ?"+obj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillIntraActRule(Action):
    """fills a rule with an intransitive verbal action"""
    def execute(self, arg1, arg2, arg3, arg4):

        rule = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3].replace(":", ".")
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3].replace(":", ".")

        # creating subclass of Verb
        types.new_class(verb, (Verb,))

        if rule[0] == "-":
            rule = "hasSubject(?"+dav+", ?"+subj+"), "+verb+"(?"+dav+") "+rule
        else:
            rule = "hasSubject(?"+dav+", ?"+subj+"), "+verb+"(?"+dav+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillGndRule(Action):
    """fills a rule with a ground"""
    def execute(self, arg0, arg1, arg2, arg3):

        hand_side = str(arg0).split("'")[1]
        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        value = str(arg3).split("'")[3].replace(":", ".")

        # creating subclass of Entity
        types.new_class(value, (Entity,))

        if hand_side == "LEFT":
            if rule[0] == "-":
                rule = value+"(?"+var+") "+rule
            else:
                rule = value +"(?"+var+"), "+rule
        else:
            if rule[-1] == ">":
                rule = rule+" "+value+"(?"+var+")"
            else:
                rule = rule+", "+value+"(?"+var+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillHeadAdjRule(Action):
    """fills a rule with an adjective"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj_str = str(arg3).split("'")[3].replace(":", ".")

        # creating subclass of Adjective
        types.new_class(adj_str, (Adjective,))

        rule = rule+" "+adj_str+"(?"+var+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillAdjRule(Action):
    """fills a rule with an adjective"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj_str = str(arg3).split("'")[3].replace(":", ".")

        # creating subclass of Adjective
        types.new_class(adj_str, (Adjective,))

        new_var = "x" + str(next(cnt))

        if rule[0] == "-":
            rule = "hasAdj(?"+var+", ?"+new_var+"), "+adj_str+"(?"+new_var+") "+rule
        else:
            rule = "hasAdj(?"+var+", ?"+new_var+"), "+adj_str+"(?"+new_var+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillAdvRule(Action):
    """fills a rule with an adverb"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adv_str = str(arg3).split("'")[3].replace(":", ".")

        # creating subclass of Adverb
        types.new_class(adv_str, (Adverb,))

        new_var = "x" + str(next(cnt))

        if rule[0] == "-":
            rule = "hasAdv(?"+var+", ?"+new_var+"), "+adv_str+"(?"+new_var+") "+rule
        else:
            rule = "hasAdv(?"+var+", ?"+new_var+"), "+adv_str+"(?"+new_var+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillPrepRule(Action):
    """fills a rule with a preposition"""
    def execute(self, arg0, arg1, arg2, arg3, arg4):

        hand_side = str(arg0).split("'")[1]
        rule = str(arg1).split("'")[3]
        var_master = str(arg2).split("'")[3]
        value = str(arg3).split("'")[3].replace(":", ".")
        var_slave = str(arg4).split("'")[3]

        # creating subclass of preposition
        types.new_class(value, (Preposition,))
        new_index_var = str(next(cnt))

        if hand_side == "LEFT":
            if rule[0] == "-":
                rule = "hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+") "+rule
            else:
                rule = "hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+"), " + rule
        else:
            if rule[-1] == ">":
                rule = rule+" hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+")"
            else:
                rule = rule+", hasPrep(?"+var_master+", ?x"+new_index_var+"), "+value+"(?x"+new_index_var+"), hasObject(?x"+new_index_var+", ?"+var_slave+")"

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class fillOpRule(Action):
    """fills with comparison operators"""
    def execute(self, arg1, arg2, arg3):

        rule = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        val_str = str(arg3).split("'")[3]

        new_index_var = str(next(cnt))

        if rule[0] == "-":
            rule = "hasValue(?"+var+", ?x"+new_index_var+"), greaterThan(?x"+new_index_var+", "+val_str+") "+rule
        else:
            rule = "hasValue(?"+var+", ?x"+new_index_var+"), greaterThan(?x"+new_index_var+", "+val_str+"), "+rule

        print("rule: ", rule)
        self.assert_belief(RULE(rule))


class aggrEntity(Action):
    """aggregate two entity beliefs in one"""
    def execute(self, arg1, arg2, arg3, arg4):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label1 = str(arg3).split("'")[3]
        label2 = str(arg4).split("'")[3]

        conc_label = label2 + "_" + label1
        self.assert_belief(GND(id, var, conc_label))


class applyAdv(Action):
    """create an entity and apply an adj to it"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", ".")
        adv_str = str(arg3).split("'")[3].replace(":", ".")

        # creating subclass adjective
        adv = types.new_class(adv_str, (Adverb,))
        # adverb individual
        new_adv_ind = adv(parser.clean_from_POS(adv_str)+"."+id_str)

        # creating subclass entity
        new_sub = types.new_class(verb_str, (Verb,))
        # creating entity individual
        new_ind = new_sub(parser.clean_from_POS(verb_str)+"."+id_str)

        # individual entity - hasAdv - adverb individual
        new_ind.hasAdv.append(new_adv_ind)


class createAdj(Action):
    """create an entity and apply an adj to it"""
    def execute(self, arg0, arg1, arg2):

        id_str = str(arg0).split("'")[3]
        ent_str = str(arg1).split("'")[3].replace(":", ".")
        adj_str = str(arg2).split("'")[3].replace(":", ".")

        # creating subclass adjective
        adv = types.new_class(adj_str, (Adjective,))
        # adverb individual
        new_adj_ind = adv(parser.clean_from_POS(adj_str)+"."+id_str)

        # creating subclass entity
        ent_sub = types.new_class(ent_str, (Entity,))
        # creating entity individual
        new_ind = ent_sub(parser.clean_from_POS(ent_str)+"."+id_str)

        # individual entity - hasAdv - adverb individual
        new_ind.hasAdj.append(new_adj_ind)


class createSubCustVerb(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg1, arg2, arg3, arg4):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", ".")
        subj_str = str(arg3).split("'")[3].replace(":", ".")
        obj_str = str(arg4).split("'")[3].replace(":", ".")

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Verb,))
        new_sub_subj = types.new_class(subj_str, (Entity,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createSubVerb(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg1, arg2, arg3, arg4):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", ".")
        subj_str = str(arg3).split("'")[3].replace(":", ".")
        obj_str = str(arg4).split("'")[3].replace(":", ".")

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Verb,))
        new_sub_subj = types.new_class(subj_str, (Entity,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createEmbVerbs(Action):
    """Creating subclasses of the class Verb/Entity + embedded individuals"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id_str = str(arg1).split("'")[3]
        main_verb_str = str(arg2).split("'")[3].replace(":", ".")
        main_subj_str = str(arg3).split("'")[3].replace(":", ".")
        emb_verb_str = str(arg4).split("'")[3].replace(":", ".")
        emb_subj_str = str(arg5).split("'")[3].replace(":", ".")
        emb_obj_str = str(arg6).split("'")[3].replace(":", ".")

        # subclasses
        main_sub_verb = types.new_class(main_verb_str, (Verb,))
        main_sub_subj = types.new_class(main_subj_str, (Entity,))
        emb_sub_verb = types.new_class(emb_verb_str, (Verb,))
        emb_sub_subj = types.new_class(emb_subj_str, (Entity,))
        emb_sub_obj = types.new_class(emb_obj_str, (Entity,))

        # individuals
        new_ind_id = Id(id_str)
        new_ind_main_verb = main_sub_verb(parser.clean_from_POS(main_verb_str)+"."+id_str)
        new_ind_main_subj = main_sub_subj(parser.clean_from_POS(main_subj_str)+"."+id_str)

        new_ind_emb_verb = emb_sub_verb(parser.clean_from_POS(emb_verb_str)+"."+id_str)
        new_ind_emb_subj = emb_sub_subj(parser.clean_from_POS(emb_subj_str)+"."+id_str)
        new_ind_emb_obj = emb_sub_obj(parser.clean_from_POS(emb_obj_str)+"."+id_str)

        # main
        new_ind_main_verb.hasSubject = [new_ind_main_subj]
        new_ind_main_verb.hasObject = [new_ind_emb_verb]

        # embedded
        new_ind_emb_verb.hasSubject = [new_ind_emb_subj]
        new_ind_emb_verb.hasObject = [new_ind_emb_obj]

        # storing action's id
        new_ind_main_verb.hasId = [new_ind_id]
        new_ind_emb_verb.hasId = [new_ind_id]





class createAssRule(Action):
    """Creating new assignment rule between entities"""
    def execute(self, arg1, arg2):

        ent1 = str(arg1).split("'")[3].replace(":", ".")
        ent2 = str(arg2).split("'")[3].replace(":", ".")

        types.new_class(ent1, (Entity,))
        types.new_class(ent2, (Entity,))

        rule_str = ent1+"(?x) -> "+ent2+"(?x)"

        rule_adj_legacy = ent1+"(?x2), "+ent2+"(?x1), hasAdj(?x1, ?x3), Adjective(?x3) -> hasAdj(?x2, ?x3)"

        print("New assignment rule: ", rule_str)
        print("New legacy rule: ", rule_adj_legacy)

        with my_onto:
           rule1 = Imp()
           rule1.set_as_rule(rule_str)

           rule2 = Imp()
           rule2.set_as_rule(rule_adj_legacy)


class createPassSubVerb(Action):
    """Creating a subclass of the class Verb (passive)"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", ".")
        obj_str = str(arg3).split("'")[3].replace(":", ".")

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Verb,))
        new_sub_obj = types.new_class(obj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_obj = new_sub_obj(parser.clean_from_POS(obj_str)+"."+id_str)

        # individual entity - hasObject - Object individual
        new_ind_verb.hasObject = [new_ind_obj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createIntrSubVerb(Action):
    """Creating a subclass of the class Verb (Intransitive)"""
    def execute(self, arg1, arg2, arg3):

        id_str = str(arg1).split("'")[3]
        verb_str = str(arg2).split("'")[3].replace(":", ".")
        subj_str = str(arg3).split("'")[3].replace(":", ".")

        # subclasses
        new_sub_verb = types.new_class(verb_str, (Verb,))
        new_sub_subj = types.new_class(subj_str, (Entity,))

        # entities individual
        new_ind_id = Id(id_str)
        new_ind_verb = new_sub_verb(parser.clean_from_POS(verb_str)+"."+id_str)
        new_ind_subj = new_sub_subj(parser.clean_from_POS(subj_str)+"."+id_str)

        # individual entity - hasSubject - subject individual
        new_ind_verb.hasSubject = [new_ind_subj]
        # storing action's id
        new_ind_verb.hasId = [new_ind_id]


class createSubPrep(Action):
    """Creating a subclass of depending action preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        verb = str(arg1).split("'")[3].replace(":", ".")
        prep = str(arg2).split("'")[3].replace(":", ".")
        ent = str(arg3).split("'")[3].replace(":", ".")

        v = parser.clean_from_POS(verb) + "." + id_str

        if v in owl_obj_dict:
            print("Getting objects from dict....", owl_obj_dict[v])
            # Getting object from dict
            new_ind_verb = owl_obj_dict[v]
        else:
            print("Creating objects....")
            # Creating subclass of Verb and individual
            new_sub_verb = types.new_class(verb, (Verb,))
            new_ind_verb = new_sub_verb(v)
            # Updating owl object dict
            owl_obj_dict[verb] = new_sub_verb
            owl_obj_dict[v] = new_ind_verb

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating subclass of Entity and individual
        new_sub_ent = types.new_class(ent, (Entity,))
        new_ind_ent = new_sub_ent(parser.clean_from_POS(ent) + "." + id_str)

        # Creating objects properties
        new_ind_verb.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent)




class createSubGndPrep(Action):
    """Creating a subclass of depending gnd preposition"""
    def execute(self, arg0, arg1, arg2, arg3):

        id_str = str(arg0).split("'")[3]
        ent_master = str(arg1).split("'")[3].replace(":", ".")
        prep = str(arg2).split("'")[3].replace(":", ".")
        ent_slave = str(arg3).split("'")[3].replace(":", ".")

        # Creating subclasses of Entity and individuals
        new_sub_ent_master = types.new_class(ent_master, (Entity,))
        new_ind_ent_master = new_sub_ent_master(parser.clean_from_POS(ent_master)+"."+id_str)
        new_sub_ent_slave = types.new_class(ent_slave, (Entity,))
        new_ind_ent_slave = new_sub_ent_slave(parser.clean_from_POS(ent_slave)+"."+id_str)

        # Creating subclass of Preposition and individual
        new_sub_prep = types.new_class(prep, (Preposition,))
        new_ind_prep = new_sub_prep(parser.clean_from_POS(prep) + "." + id_str)

        # Creating objects properties
        new_ind_ent_master.hasPrep.append(new_ind_prep)
        new_ind_prep.hasObject.append(new_ind_ent_slave)


class createPlace(Action):
    """Creating DataProperty from NER Place"""
    def execute(self, arg1, arg2):

        id_str = str(arg1).split("'")[3]
        place_str = str(arg2).split("'")[3]

        # entities individual
        new_ind_id = Id(id_str)

        # storing id features
        new_ind_id.hasPlace = [place_str]


class createDate(Action):
    """Creating DataProperty from NER Date"""
    def execute(self, arg1, arg2):

        id_str = str(arg1).split("'")[3]
        date_str = str(arg2).split("'")[3]

        # entities individual
        new_ind_id = Id(id_str)

        # storing id features
        new_ind_id.hasDate = [date_str]


class createValue(Action):
    """Creating DataProperty fro a given value to entity"""
    def execute(self, arg0, arg1, arg2):

        id_str = str(arg0).split("'")[3]
        ent_str = str(arg1).split("'")[3]
        value_str = str(arg2).split("'")[3]

        # creating subclass of entity
        new_sub_obj = types.new_class(ent_str, (Entity,))

        # entities individual
        new_ind_ent = new_sub_obj(parser.clean_from_POS(ent_str)+"."+id_str)

        # storing value
        new_ind_ent.hasValue = [int(value_str)]


class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):
        with my_onto:
            #sync_reasoner_pellet()
            my_onto.save(file=FILE_NAME, format="rdfxml")


class InitOnto(Action):
    """Generating sentence id individual"""
    def execute(self):
        dateTimeObj = datetime.datetime.now()
        id_ind = str(dateTimeObj.microsecond)
        self.assert_belief(ID(id_ind))


class COP(ActiveBelief):
    """ActiveBelief for checking wether a lemma can generate an assignment rule"""
    def evaluate(self, arg1):

        lemma = str(arg1).split("'")[3]
        lemma_decomposed = lemma.split(":")

        POS_ADMITTED = False

        if len(lemma_decomposed) > 1:
            if lemma_decomposed[1] in ASSIGN_RULES_POS:
                POS_ADMITTED = True
        else:
            POS_ADMITTED = True

        # Checking for proper lemma
        if lemma_decomposed[0] in ASSIGN_RULES_LEMMAS and POS_ADMITTED is True:
           return True
        else:
           return False





# ---------------------- MST Builder Section


class parse_rules(Action):
    """Asserting dependencies related beliefs."""
    def execute(self, arg, dis):

        parser.flush()

        sent = str(arg).split("'")[3]
        if str(dis).split("'")[1] == "DISOK":
            DISOK = True
        else:
            DISOK = False

        print("\n", sent)
        deps = parser.get_deps(sent, True, DISOK)
        print("\n", deps)
        parser.set_last_deps(deps)

        for dep in deps:
            self.assert_belief(DEP(dep[0], str(dep[1]), str(dep[2])))


class create_MST_ACT(Action):
    """Asserting an MST  Action."""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        subj = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        subj_var = "x"+str(next(cnt))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, subj_var, obj_var))
        self.assert_belief(MST_VAR(subj_var, subj))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_ACT_PASS(Action):
    """Asserting an MST PASSIVE Action."""
    def execute(self, arg1, arg2):
        verb = str(arg1).split("'")[3]
        subj = str(arg2).split("'")[3]

        davidsonian = "e" + str(next(dav))
        subj_var = "x"+str(next(cnt))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, obj_var, subj_var))
        self.assert_belief(MST_VAR(subj_var, subj))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_PREP(Action):
    """Asserting an MST preposition."""
    def execute(self, arg1, arg2):
        dav = str(arg1).split("'")[3]
        prep = str(arg2).split("'")[3]

        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_PREP(prep, dav, obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class COND_WORD(ActiveBelief):
    """Checking for conditionals related words."""
    def evaluate(self, x):

        word = str(x).split("'")[3]
        # Check for conditional word
        if word.upper()[0:4] in AXIOMS_WORDS:
            return True
        else:
            return False


class NBW(ActiveBelief):
    """Checking for not blacklisted words."""
    def evaluate(self, x):

        word = str(x).split("'")[3]

        # Check for conditional word
        if self.get_lemma(word)[:-2].lower() not in ["that"]:
            return True
        else:
            return False

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class feed_mst_actions_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1, arg2, arg3, arg4):
        dav = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        subj = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]

        action = []
        action.append(dav)
        action.append(verb)
        action.append(subj)
        action.append(obj)

        parser.feed_MST(action, 0)


class feed_mst_vars_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1, arg2):
        var = str(arg1).split("'")[3]
        val = str(arg2).split("'")[3]

        variable = []
        variable.append(var)
        variable.append(val)

        parser.feed_MST(variable, 1)


class feed_mst_preps_parser(Action):
    """Feed MST preps parser"""
    def execute(self, arg1, arg2, arg3):
        label = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        var_obj = str(arg3).split("'")[3]

        prep = []
        prep.append(label)
        prep.append(var)
        prep.append(var_obj)

        parser.feed_MST(prep, 2)


class feed_mst_binds_parser(Action):
    """Feed MST binds parser"""
    def execute(self, arg1, arg2):
        related = str(arg1).split("'")[3]
        relating = str(arg2).split("'")[3]

        bind = []
        bind.append(related)
        bind.append(relating)

        parser.feed_MST(bind, 3)


class feed_mst_comps_parser(Action):
    """Feed MST comps parser"""
    def execute(self, arg1, arg2):
        related = str(arg1).split("'")[3]
        relating = str(arg2).split("'")[3]

        comp = []
        comp.append(related)
        comp.append(relating)

        parser.feed_MST(comp, 4)


class feed_mst_conds_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1):
        cond = str(arg1).split("'")[3]

        parser.feed_MST(cond, 5)


class flush_parser_cache(Action):
    """Flushing parser cache"""
    def execute(self):
        parser.flush()


class concat_mst_verbs(Action):
    """Concatenate composite verbs"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        verb1 = str(arg1).split("'")[3]
        verb2 = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        self.assert_belief(MST_ACT(verb1+"_"+verb2, dav, subj, obj))


class Past_Part(ActiveBelief):
    """Checking for Past Participle tense"""
    def evaluate(self, x):

        label = str(x).split("'")[3]

        if label.split(':')[1] == "VBN":
            return True
        else:
            return False


class Wh_Det(ActiveBelief):
    """Checking for Wh-determiner"""
    def evaluate(self, x):

        label = str(x).split("'")[3]

        if label != "?":
            if label.split(':')[1] == "WDT":
                return True
            else:
                return False
        else:
            return False


class create_MST_ACT_SUBJ(Action):
    """Asserting an MST Action with custom var subj"""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        subj_var = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, subj_var, obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_ACT_EX(Action):
    """Asserting an MST Existencial"""
    def execute(self, arg1):

        verb = str(arg1).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x" + str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, "_", obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_IMP_MST_ACT(Action):
    """Asserting an Imperative MST Action."""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        obj = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, "_", obj_var))
        self.assert_belief(MST_VAR(obj_var, obj))


# ----------------------------------
# --------- SPARQL Section ---------
# ----------------------------------


class submit_query_sparql(Action):
    """Submit a Query Sparql to Reasoner"""
    def execute(self, arg1):

        query = str(arg1).split("'")[3]

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        sync_reasoner_hermit(my_world)
        graph = my_world.as_rdflib_graph()
        result = list(graph.query(query))

        print("\nResult: ", result)


class feed_query_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        # print(arg1)
        # print(arg2)
        # print(arg3)
        # print(arg4)
        # print(arg5)
        # print(arg6)

        v = str(arg1).split("'")[3]
        e = str(arg2).split("'")[3]
        x = str(arg3).split("'")[3]
        y = str(arg4).split("'")[3]
        val_x = str(arg5).split("'")[3]
        val_y = str(arg6).split("'")[3]

        verb = v.split(":")[0][:-2]
        subject = val_x.split(":")[0][:-2]
        object = val_y.split(":")[0][:-2]

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX lodo: <http://test.org/west.owl#> "

        # +QUERY("Colonel West sells missiles?")

        q = p + " ASK WHERE { "

        q = q + f"?{e} rdf:type lodo:{verb}. ?{e} lodo:hasSubject ?{x}. ?{e} lodo:hasObject ?{y}. ?{x} rdf:type lodo:{subject}. ?{y} rdf:type lodo:{object}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class feed_cop_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]
        val_x = str(arg4).split("'")[3]
        val_y = str(arg5).split("'")[3]

        subject = val_x.split(":")[0][:-2]
        object = val_y.split(":")[0][:-2]

        p = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        p = p + "PREFIX lodo: <http://test.org/west.owl#> "

        q = p + "ASK WHERE { "

        q = q + f"?{y} rdf:type lodo:{subject}. ?{y} rdf:type lodo:{object}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))


class feed_cop_prep_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        # print(arg1)
        # print(arg2)
        # print(arg3)
        # print(arg4)
        # print(arg5)
        # print(arg6)
        # print(arg7)

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]

        p = str(arg4).split("'")[3]
        prep = p.split(":")[0][:-2]

        prep_obj = str(arg5).split("'")[3]

        prep_obj_val = str(arg6).split("'")[3]
        prep_obj_val = prep_obj_val.split(":")[0][:-2]

        q = str(arg7).split("'")[3][:-1]

        # +QUERY("Colonel West is President of Cuba?")

        q = q + f" ?{y} lodo:hasPrep ?p{y}. ?p{y} rdf:type lodo:{prep}. ?p{y} lodo:hasObject ?{prep_obj}. ?{prep_obj} rdf:type lodo:{prep_obj_val}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_prep_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        # print(arg1)
        # print(arg2)
        # print(arg3)
        # print(arg4)
        # print(arg5)
        # print(arg6)
        # print(arg7)

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]

        p = str(arg4).split("'")[3]
        prep = p.split(":")[0][:-2]

        prep_obj = str(arg5).split("'")[3]

        prep_obj_val = str(arg6).split("'")[3]
        prep_obj_val = prep_obj_val.split(":")[0][:-2]

        q = str(arg7).split("'")[3][:-1]

        # +QUERY("Colonel West sells missiles to Cuba?")

        q = q + f" ?{e} lodo:hasPrep ?p{e}. ?p{e} rdf:type lodo:{prep}. ?p{e} lodo:hasObject ?{prep_obj}. ?{prep_obj} rdf:type lodo:{prep_obj_val}."+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class feed_adj_sparql(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        # print(arg1)
        # print(arg2)
        # print(arg3)
        # print(arg4)
        # print(arg5)
        # print(arg6)

        e = str(arg1).split("'")[3]
        x = str(arg2).split("'")[3]
        y = str(arg3).split("'")[3]

        target = str(arg4).split("'")[3]

        adj = str(arg5).split("'")[3]
        adj = adj.split(":")[0][:-2]

        q = str(arg6).split("'")[3][:-1]

        # +QUERY("Colonel West sells long missiles?")
        # +QUERY("The good Colonel West sells missiles?")
        # +QUERY("The good Colonel West sells long missiles?")

        q = q + f" ?{target} lodo:hasAdj ?a{target}. ?a{target} rdf:type lodo:{adj}. "+"}"

        self.assert_belief(PRE_SPARQL(e, x, y, q))



class join_cmps(Action):
    """Feed Query Sparql parser"""
    def execute(self, arg1, arg2, arg3):

        var = str(arg1).split("'")[3]
        val1 = str(arg2).split("'")[3]
        val2 = str(arg3).split("'")[3]

        new_var = val2.split(":")[0][:-2]+"_"+val1
        self.assert_belief(MST_VAR(var, new_var))
