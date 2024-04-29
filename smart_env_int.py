from phidias.Lib import *
from actions import *



# SMART ENVIRONMENT INTERFACE

+SENSOR(V, X, Y) >> [check_conds()]
check_conds() / (SENSOR(V, X, Y) & COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nconditional met!"), -COND(I, V, X, Y), +START_ROUTINE(I), check_conds()]
check_conds() / SENSOR(V, X, Y) >> [show_line("\nbelief sensor not more needed..."), -SENSOR(V, X, Y)]

+START_ROUTINE(I) / (COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nroutines not ready!")]
+START_ROUTINE(I) / ROUTINE(I, K, J, L, T) >> [show_line("\nexecuting routine..."), -ROUTINE(I, K, J, L, T), +INTENT(K, J, L, T), +START_ROUTINE(I), say("executing routine")]


# after:
# +FEED("Robinson Crusoe is a patient")
# +FEED("Robinson Crusoe has diastolic blood pressure equal to 150")
# +FEED("When a patient has diastolic blood pressure greater than 140, the patient is hypertensive")
# d2()
+INTENT(X, "Rinazina", Z, T) / (lemma_in_syn(X, "give.v.19") & eval_sem(T, "Hypertensive")) >> [show_ct(), say("I cannot execute the task. The patient is hypertensive")]
+INTENT(X, "Rinazina", Z, T) / lemma_in_syn(X, "give.v.19") >> [exec_cmd(X, "Rinazina", Z, T), show_ct(), say("execution successful")]

# any other commands
+INTENT(V, X, L, T) >> [show_line("\n---- Result: failed to execute the command: ", V), show_ct(), say("execution failed")]

