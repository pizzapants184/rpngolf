import state
import base
import parse
import RGmath
import RGlist
import RGloops
import RGcontrol

if __name__ != "__main__":
	raise ImportWarning("Why are you importing main instead of running it?")
import sys
#import getopt
state.do_file(sys.argv[1])
if state.running:
	print(state.stack)