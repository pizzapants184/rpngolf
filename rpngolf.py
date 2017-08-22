import math
import re
import operator
import sys

# Each command is one letter, lowercase means execute, uppercase means push its routine to the stack
# For multi-char commands, the first char's case determines this, the second char determines what command it is (case-sensitively)
# Multiple commands can also be surrounded in parentheses to push them together as a routine to the stack
# e.g.
# > (aaa)
# stack: [Routine('aaa')]
# > AAA
# stack: [Routine('a'), Routine('a'), Routine('a')]
# Routines can be added together and multiplied by integers:
# > A2c
# stack: [Routine('aa')]
# > ABa
# stack: [Routine('ab')]

class Routine:
	def __init__(self, source):
		self.source = source
		self.calls = parse_line(source)
	def __call__(self):
		if debug:
			print("Routine.__call__: %s"%self)
		if not isinstance(self, Routine):
			self = cr(self) # defined later
		do(self)
	def __repr__(self):
		return "(%s)" % self.source
	def __add__(self, other):
		return Routine(self.source + cr(other).source)
	def __radd__(self, other):
		return Routine(cr(other).source + self.source)
	def __mul__(self, other):
		if debug:
			print("Routine.__mul__: %s %s" % (self, other))
		return Routine(self.source*ci(other))
	def __rmul__(self, other):
		if debug:
			print("Routine.__rmul__: %s %s" % (self, other))
		return Routine(self.source*ci(other))


def coerce(item, type_): # type_ is int, float, str, list, or Routine
	if isinstance(item, int):
		if type_ is Routine:
			return Routine('%d' % item)
		else:
			return type_(item)
	elif isinstance(item, float):
		if type_ is Routine:
			return Routine('%f' % item)
		else:
			return type_(item)
	elif isinstance(item, str):
		if type_ is Routine:
			return Routine(item)
		else:
			return type_(item)
	elif isinstance(item, list):
		if type_ is Routine:
			raise NotImplementedError
		elif type_ is int:
			return len(item)
		elif type_ is float:
			return float(len(item))
		elif type_ is str:
			s = '['
			for q in item:
				s += str(q)+','
			s = s[:-1] + ']'
			return s
		else:
			return type_(item)
	elif isinstance(item, Routine):
		if type_ is Routine:
			return Routine(item.source)
		elif type_ is str:
			return item.source
		elif type_ is list:
			return item.calls
		else:
			raise NotImplementedError
ci = lambda a: coerce(a, int)
cf = lambda a: coerce(a, float)
cs = lambda a: coerce(a, str)
cl = lambda a: coerce(a, list)
cr = lambda a: coerce(a, Routine)

# name: (function, argc),
#  argc >= 0: number of args
#  argc == -1: top of stack is # of args
#  argc == -2: whole stack as individual args
#  argc == -3: whole stack as list is only arg
#  argc == -4: next character in line is arg (2-char command) # NOTE: implemented as name: None
defaults = {
	'a': (operator.add, 2),
	'b': (operator.sub, 2),
	'c': (operator.mul, 2),
	'd': (operator.truediv, 2),
	'e': (operator.pow, 2),
	'f': (operator.floordiv, 2),
	'g': (operator.mod, 2),
	'h': ((lambda a: a-1), 1),
	'i': ((lambda a: a+1), 1),
	'j': ((lambda a: call(a)), 1), # call a routine
	'k': { # coersion 2-char
		'a': (ci, 1),  # int
		'b': (cf, 1),  # float
		'c': (cs, 1),  # string
		'd': (cl, -3), # convert stack to list
		'e': (cr, 1),  # Routine
		'f': (cl, 1),  # top to list
		'r': (repr, 1),# python3 __repr__
		
		
	},
	'l': { # list 2-char
		'a': ((lambda a,b: a.append(b) or a), 2), # append item to list
		'A': ((lambda a: (a, a.pop())), 1), # pop item from list, keeping list
		'B': ((lambda a: a.pop()), 1), # last item from list
		'c': ((lambda a: max(cl(a))), 1), # max
		'C': ((lambda a: min(cl(a))), 1), # min
		'd': ((lambda a: all(cl(a))), 1), # all
		'D': ((lambda a: all(not i for i in cl(a))), 1), # none
		'e': ((lambda a: any(cl(a))), 1), # any
		'E': ((lambda a: any(not i for i in cl(a))), 1), # any not
		'G': ((lambda a,b: a.pop(b)), 2), # remove item b from list, keeping item
		'i': ((lambda a,b,c: a.insert(ci(b),c) or a), 3), # insert c into a at b
		'I': ((lambda a,b: (a, a.pop(b))), 2), # remove item b from list a, keeping list and item
		'J': ((lambda a,b: (a.pop(ci(b)) and 0) or a), 2), # remove item b from list, keeping list
		'k': (list.__len__, 1), # length of list
		'K': ((lambda a,b: [a]*ci(b)), 2), # create an a-initialized list of length b
		'l': ((lambda a: (a, len(a))), 1), # length of list, keeping list
		'L': ((lambda a: [0]*ci(a)), 1), # create a 0-initialized list of length a
		'o': ((lambda a,b: a[b:]), 3), # slice a list
		'p': ((lambda a,b: (a,a[b:])), 3), # slice a list, keeping list
		'O': ((lambda a,b,c: a.__setitem__(slice(b,None), c) or a), 3), # set a list slice
		'q': ((lambda a,b: a[:b]), 3), # slice a list
		'r': ((lambda a,b: (a,a[:b])), 3), # slice a list, keeping list
		'Q': ((lambda a,b,c: a.__setitem__(slice(None,b), c) or a), 3), # set a list slice
		's': ((lambda a,b,c: a[b:c]), 3), # slice a list
		't': ((lambda a,b,c: (a,a[b:c])), 3), # slice a list, keeping list
		'S': ((lambda a,b,c,d: a.__setitem__(slice(b,c), d) or a), 3), # set a list slice
		'u': ((lambda a,b,c,d: a[b:c:d]), 3), # slice a list
		'v': ((lambda a,b,c,d: (a,a[b:c:d])), 3), # slice a list, keeping list
		'U': ((lambda a,b,c,d,e: a.__setitem__(slice(b,c,d), e) or a), 3), # set a list slice
	},
	'm': { # math 2-char: 'mX' is inverse of 'mx' in most cases
		'a': (math.sin, 1),
		'A': (math.asin, 1),
		'b': (math.cos, 1),
		'B': (math.acos, 1),
		'c': (math.tan, 1),
		'C': (math.atan, 1),
		'd': ((lambda a: (math.sin(a),math.cos(a))), 1),
		'D': (math.atan2, 2),
		'e': ((lambda a: 1/math.sin(a)), 1), # csc
		'E': ((lambda a: math.asin(1/a)), 1),# acsc
		'f': ((lambda a: 1/math.cos(a)), 1), # sec
		'F': ((lambda a: math.acos(1/a)), 1),# asec
		'g': ((lambda a: math.cos(a)/math.sin(a)), 1),# cot
		'G': ((lambda a: math.pi/2-math.atan(a)), 1), # acot
		'h': ((lambda a: (math.cos(a), math.sin(a))), 1),
		'H': ((lambda a,b: math.pi/2-math.atan2(a,b)), 2), # acot2 
		'i': (math.log, 1), # ln
		'I': ((lambda a: math.e**a), 1), # e^x
		'j': (math.log10, 1),
		'J': ((lambda a: 10**a), 1),
		'k': (math.log, 2), # logb, inverse is 'e'
		'l': ((lambda a: 1 if a>0 else -1 if a<0 else 0), 1), #sign
		'L': (abs, 1), # abs
		'
	},
	'n': ((lambda a: list(range(a))), 1), # range
	'o': ((lambda a: None), 1), # pop
	'p': ((lambda a: (a,a)), 1), # dup
	'q': ((lambda: quit_(0)), 0),
	's': ((lambda a,b: (b,a)), 2), # swp
	't': { # control and i/o commands
		'a': (input, 0), # user input as string
		'b': ((lambda: ci(input())), 0), # user input as an integer
		'c': ((lambda: cf(input())), 0), # user input as a float
		'd': ((lambda: cl(input())), 0), # user input as a list
		'e': ((lambda: cr(input())), 0), # user input as a routine
		'f': ((lambda: eval(input())), 0), # user input as python (list, str, whatever)
		'A': ((lambda a: print(cs(a))), 1), # print top of stack as string, removing it
		'B': ((lambda a: print(cs(a)) or a), 1), # print top of stack as string, leaving it
		'C': ((lambda: print(stack)), 0), # print stack
		'q': ((lambda: quit_(1)), 0), # quit and print stack
		'Q': ((lambda a: quit_(a)), 1), # quit printing or not depending of arg
		'r': ((lambda a: quit_() if a else None), 1), # conditional quit based on arg
		'R': ((lambda a,b: quit_(a) if b else None), 1), # conditional quit based on b, printing or not based on a
		
		'z': ((lambda: debug_()), 0),
	},
	'u': None, # implemented otherwhere
	'v': None,
	'w': None,
	'x': ((lambda a,b,c: if_(a,b,c)), 3),
}
stack = []
variables = {
	
}
debug = False
running = True
def quit_(arg=0):
	global running
	if arg == 1:
		print(stack)
	elif arg == 2:
		print(*stack,sep='')
	running = False
def if_(true, false, condition):
	do(condition)
	if stack[-1]:
		do(true)
	else:
		do(false)
def debug_():
	global debug
	debug = not debug
def storer(var):
	def _store(val):
		variables[var] = val
	return _store
def parse_line(line):
	def _err_loc(i):
		return '\n'+line+'\n' + ' '*i + '^'
	items = []
	s = ''
	nest = 0
	quoted = ''
	escaped = False
	partial = ''
	isroutine = False
	numeric = False
	number = 0
	place = 0
	sign = 1
	for i in range(len(line)):
		c = line[i]
		if numeric and c.isnumeric() and not place:
			number = 10 * number + sign*int(c)
			continue
		elif numeric and c.isnumeric():
			number = number + sign*int(c)*(10**place)
			place -= 1
			continue
		elif numeric and c == '.' and not place:
			place = -1
			continue
		elif numeric and c == '.':
			raise SyntaxError("Invalid number literal."+_err_loc(i))
		elif numeric:
			items.append(number)
			number = 0
			place = 0
			numeric = False
			sign = 1
		if partial:
			#print(".partial is %s"%partial)
			if isinstance(defaults[partial], dict) and c in defaults[partial]:
				if isroutine:
					items.append(Routine(partial+c))
				else:
					items.append(defaults[partial][c])
			elif defaults[partial] is None:
				if isroutine:
					items.append(Routine(partial+c))
				elif partial == 'w':
					items.append(((lambda name: (lambda: variables[name]))(c),0))
					items.append(defaults['j'])
				elif partial == 'v':
					items.append((storer(c),1)) # (func, argc)
				elif partial == 'u':
					temp = c
					items.append(((lambda name: (lambda: variables[name]))(c),0))
				else:
					raise SyntaxError("Unknown variable 2-char: %s" % (partial+c))
			else:
				raise SyntaxError("Invalid partial continuation: %s" % (s+c))
			s = ''
			partial = ''
		elif quoted:
			if c == quoted and not escaped:
				quoted = ''
				if c == "'": # single quote is quoted string
					items.append(s[:])
				else: # double quote is routine to push quoted string
					items.append(Routine("'"+s+"'"))
				s = ''
			elif c == '\\' and not escaped:
				escaped = True
			else:
				s += c
				escaped = False
		elif nest > 0:
			if c == ')':
				nest -= 1
				if not nest:
					items.append(Routine(s[1:]))
					s = ''
					continue
			elif c == '(':
				nest += 1
			s += c
		elif c == '(' and nest == 0:
			if s:
				raise SyntaxError("Opening parenthesis")
			nest = 1
			s = c
		elif c == "'" or c == '"':
			if s != '':
				raise SyntaxError("Opening quote")
			quoted = c
		elif c.islower() and c in defaults:
			isroutine = False
			cmd = defaults[c]
			if isinstance(cmd, (dict,type(None))):
				partial = c
				#print("partial is %s"%c)
				continue
			else:
				items.append(cmd)
		elif c.isupper() and c.lower() in defaults:
			isroutine = True
			c = c.lower()
			cmd = defaults[c]
			if isinstance(cmd, (dict,type(None))):
				partial = c
				continue
			else:
				items.append(Routine(c))
		elif c.isnumeric():
			number = int(c)
			numeric = True
		elif c == '.':
			numeric = True
			place = -1
		elif c == '-':
			numeric = True
			sign = -1
		elif c in '; ':
			pass
		else:
			raise SyntaxError("Unknown character: %s"%c)
	if numeric:
		items.append(number)
	if quoted:
		raise SyntaxError("Unclosed quote"+_err_loc(i))
	if nest:
		raise SyntaxError("Unclosed parenthesis"+_err_loc(i))
	if partial:
		raise SyntaxError("Unterminated partial"+_err_loc(i))
	return items
def do_line(line):
	items = parse_line(line)
	do_items(items)
def do_file(name):
	itemslist = []
	with open(name, "r") as file:
		for line in file.readlines():
			if debug:
				print(line)
			itemslist.append(parse_line(line))
	for items in itemslist:
		do_items(items)
	quit_(2)

def do_items(items):
	stack_ = stack[:]
	try:
		for item in items:
			do(item)
	except (ArithmeticError, ValueError, IndexError) as e:
		stack[:] = stack_
		if debug:
			print("do_items: %s"%e)
			raise
def pop_n(n):
	if len(stack) < n:
		raise ValueError("Not enough items on stack: %d < %d" % (len(stack), n))
	items = []
	for i in range(n):
		items.append(stack.pop())
	return reversed(items)
def call(routine):
	if not isinstance(routine, Routine):
		routine = cr(routine)
	for item in routine.calls:
		do(item)
def do(item):
	if not running:
		return
	if debug:
		print(item)
	if isinstance(item, (int, float, str, Routine, list)):
		stack.append(item)
	elif isinstance(item, tuple):
		func, argc = item
		if argc >= 0:
			argv = pop_n(argc)
			ret = func(*argv)
			if ret is None:
				pass
			elif isinstance(ret, tuple):
				for i in ret:
					stack.append(i)
			else:
				stack.append(ret)
		elif argc == -1:
			if not len(stack):
				raise ValueError("Not enough items on stack: %d < %d" % (len(stack), n))
			argc = stack.pop()
			try:
				argv = pop_n(argc)
			except ValueError:
				stack.append(argc)
				raise
			ret = func(*argv)
			if ret is None:
				pass
			elif isinstance(ret, tuple):
				for i in ret:
					stack.append(i)
			else:
				stack.append(ret)
if __name__ == "__main__":
	import sys
	import getopt
	opts, args = getopt.getopt(sys.argv[1:], 'idc:')
	opts = dict(opts)
	if '-i' in opts:
		while running:
			do_line(input('> '))
		sys.exit()
	if '-d' in opts:
		debug = True
	if '-c' in opts:
		if len(args)>1:
			stack_ = args[1][1:-1].split(',')
			for item in stack_:
				if re.match("^-?[0-9]*$", item):
					stack.append(int(item))
				elif re.match("^-?([0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)$", item):
					stack.append(float(item))
				elif re.match("^('[^']*'|"+'"[^"]*")$', item):
					stack.append(item[1:-1])
				else:
					raise ValueError("IDK %s" % item)
		do_line(opts['-c'])
		if running:
			quit_(2)
	else:
		if len(args) == 1:
			do_file(args[0])
		elif len(args) == 2:
			stack_ = args[1][1:-1].split(',')
			for item in stack_:
				if re.match("^-?[0-9]*$", item):
					stack.append(int(item))
				elif re.match("^-?([0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)$", item):
					stack.append(float(item))
				elif re.match("^('[^']*'|"+'"[^"]*")$', item):
					stack.append(item[1:-1])
				else:
					raise ValueError("IDK %s" % item)
			do_file(args[0])
		elif len(args)==0:
			print("Usage:\n\t%s [file] <initial stack>\n\t%s -c [actual code] <initial stack>" % ((sys.argv[0],)*2))
	