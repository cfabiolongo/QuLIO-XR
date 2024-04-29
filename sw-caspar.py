from phidias.Main import *
from phidias.Types import *



def_vars('X', 'Y', 'Z', 'T', 'W', 'K', 'J', 'M', 'N', "D", "I", "V", "L", "O", "E", "U", "S", "R", "H", "A")

from actions import *
from onto_builder import *
from mst_builder import *
from direct_cmd_parser import *
from routines_parser import *
from smart_env_int import *
from front_end import *



# instantiate the engine
PHIDIAS.run()
# run the engine shell
PHIDIAS.shell(globals())
