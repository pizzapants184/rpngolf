import functions
import parse
import base as base_
import routines
class Stack:
	def __init__(self):
		self.stack = []
		self.stacktrace = []
	def zoomin(self):
		if len(self.stack) < 1:
			self.stack.append([])
		if not isinstance(self.stack[-1], list):
			item = self.stack.pop()
			self.stack.append([item])
		self.stacktrace.append(self.stack)
		self.stack = self.stack[-1]
	def zoomout(self):
		if len(self.stacktrace) < 1:
			self.stack = [self.stack]
			return
		if self.stack not in self.stacktrace[-1]:
			raise ValueError(self, self.stack, self.stacktrace)
		self.stack = self.stacktrace.pop()
	def __len__(self):
		return len(self.stack)
	def append(self, item):
		self.stack.append(item)
	def pop(self):
		return self.stack.pop()
	def insert(self, index, obj):
		self.stack.insert(index, obj)
	def __str__(self):
		return str(self.stack)
	def __repr__(self):
		return repr(self.stack)
	def __getitem__(self, index):
		return self.stack[index]
	def __setitem__(self, index, item):
		self.stack[index] = item
running = True
debug_ = False
stack = Stack()
#base = None
stacktrace = []

def s_do_items(items, _stack):
	for item in items:
		if running:
			if debug_:
				print("_stack: %s\nitem: %s" % (_stack, item))
			if isinstance(item, functions.RGFunction):
				item(_stack)
			else:
				_stack.append(item)
			if debug_:
				print("_stack: %s\n" % _stack)
#		s_do(item, _stack) # inlining for perfomance
def s_do(item, _stack):
	if running:
		if debug_:
			print("_stack: %s\nitem: %s" % (_stack, item))
		if isinstance(item, functions.RGFunction):
			item(_stack)
		else:
			_stack.append(item)
		if debug_:
			print("_stack: %s\n" % _stack)
def s_do_line(line, _stack):
	items = parse.parse(line)
	s_do_items(items, _stack)


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
	if running:
		print(*stack, sep=' ')
def debug():
	print("stack: ",stack)
	print("running: ",running)
	print("base: ",base)
	print("base_: ",base_)
	print("vars: ",base_.vars.vars)
