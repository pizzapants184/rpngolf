import functions
import parse
import base as base_
import routines

running = True
debug_ = False
stack = []
#base = None
stacktrace = []

def s_do_items(items, stack):
	for item in items:
		s_do(item, stack)
def s_do(item, stack):
	if running:
		if debug_:
			print("stack: %s\nitem: %s" % (stack, item))
		if isinstance(item, functions.RGFunction):
			item(stack)
		else:
			stack.append(item)
		if debug_:
			print("stack: %s\n" % stack)
def s_do_line(line, stack):
	items = parse.parse(line)
	s_do_items(items, stack)


def do_items(items):
	s_do_items(items, stack)
#	for item in items:
#		do(item)
def do(item):
	s_do(item, stack)
#	if running:
#		if debug_:
#			print("stack: %s\nitem: %s" % (stack, item))
#		if isinstance(item, functions.RGFunction):
#			item(stack)
#		else:
#			stack.append(item)
#		if debug_:
#			print("stack: %s\n" % stack)
def do_line(line):
	s_do_line(line, stack)
#	items = parse.parse(line)
#	do_items(items)
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
