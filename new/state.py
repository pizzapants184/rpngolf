import functions
import parse
import base as base_
import routines

running = True
debug_ = False
stack = []
#base = None

def do_items(items):
	for item in items:
		do(item)
def do(item):
	if running:
		if debug_:
			print("stack: %s\nitem: %s" % (stack, item))
		if isinstance(item, functions.RGFunction):
			item(stack)
		else:
			stack.append(item)
		if debug_:
			print("stack: %s\n" % stack)
def do_line(line):
	items = parse.parse(line)
	do_items(items)
def do_file(name):
	f = open(name, "r")
	for line in f.readlines():
		do_line(line.strip('\n'))
def debug():
	print("stack: ",stack)
	print("running: ",running)
	print("base: ",base)
	print("base_: ",base_)
	print("vars: ",base_.vars.vars)
