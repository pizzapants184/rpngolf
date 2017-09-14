import state
import modules
import functions
import routines

import re
def parse(source):
	if '\n' in source:
		r = []
		for item in source.split('\n'):
			r += parse(item)
		return r
	elif len(source) == 0:
		return []
	elif source[0] in ' \t':
		return parse(source[1:])
	elif source[0] == "'":
		length = 0
		source = source[1:]
		while True:
			try:
				if source[length] == '\\':
					length += 1
					if len(source) == length:
						return [source[:-1]+'\n']
					elif source[length] == "'":
						source = source[:length-1]+source[length:]
					elif source[length] == 'n':
						source = source[:length-1] + '\n' + source[length+1:]
					elif source[length] == 't':
						source = source[:length-1] + '\t' + source[length+1:]
					elif source[length] == 'r':
						source = source[:length-1] + '\r' + source[length+1:]
					elif source[length] == 'x':
						source = source[:length-1] + chr(int(source[length+1:length+3], 16)) + source[length+3:]
					elif source[length] == 'u':
						source = source[:length-1] + chr(int(source[length+1:length+5], 16)) + source[length+5:]
					elif source[length] == 'U':
						source = source[:length-1] + chr(int(source[length+1:length+9], 16)) + source[length+9:]
					elif source[length] == 'b':
						source = source[:length-1] + '\b' + source[length+1:]
					elif source[length] == 'a':
						source = source[:length-1] + '\a' + source[length+1:]
					elif source[length] == 'f':
						source = source[:length-1] + '\f' + source[length+1:]
					elif source[length] == 'v':
						source = source[:length-1] + '\v' + source[length+1:]
					elif source[length] in '01234567':
						if len(source) > length+1 and source[length+1] in '01234567':
							if len(source) > length+2 and source[length+2] in '01234567':
								source = source[:length-1] + chr(int(source[length:length+3], 8)) + source[length+3:]
							else:
								source = source[:length-1] + chr(int(source[length:length+2], 8)) + source[length+2:]
						else:
							source = source[:length-1] + chr(int(source[length:length+1], 8)) + source[length+1:]
					else:
						length += 1
				elif source[length] == "'":
					return [source[:length]] + parse(source[length+1:])
				else:
					length += 1
			except IndexError:
				return [source[:length]]
	elif source[0] == '(':
		nest = 1
		length = 1
		try:
			while True:
				if source[length] == '(':
					nest += 1
				elif source[length] == ')':
					nest -= 1
				if nest:
					length += 1
				else:
					return [routines.Routine(source[1:length])] + parse(source[length+1:])
		except IndexError:
			while nest > 0:
				source += ')'
				nest -= 1
				print(source)
			return [routines.Routine(source[1:-1])]
	elif source[0] == '[':
		nest = 1
		length = 1
		while True:
			if length >= len(source):
				pass
			elif source[length] == '[':
				nest += 1
			elif source[length] == ']':
				nest -= 1
			if nest and (length < len(source)):
				length += 1
			else:
				items = parse(source[1:length])
				substack = state.Stack()
				state.s_do_items(items, substack)
				return [substack.stack] + parse(source[length+1:])
	#elif source[0] == '[':
	#	match = re.match("^[[][^]]*([]]|$)", source)
	#	raise ValueError
					
	elif re.match("^(_?[0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+)(.*)$", source):
		match = re.match("^(_?[0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+)(.*)$", source)
		groups = match.groups()
		return [float(groups[0].replace("_", "-"))] + parse(groups[1])
	elif re.match("^_?(@[01]*)(.*)$", source):
		match = re.match("^(_?)(@[01]*)(.*)$", source)
		groups = match.groups()
		return [int(groups[0].replace("_", "-")+'0'+groups[1][1:], 2)] + parse(groups[2])
	elif re.match("^(_?[0-9]+)(.*)$", source):
		match = re.match("^(_?[0-9]+)(.*)$", source)
		groups = match.groups()
		return [int(groups[0].replace("_", "-"))] + parse(groups[1])
	elif source[0] == '#':
		return []
	else:
		lookup = state.base[source[0]]
		if isinstance(lookup, modules.RGSubModuleBase):
			depth = 1
			trace = [lookup]
			while True:
				lookup = lookup[source[depth]]
				depth += 1
				trace.append(lookup)
				if not isinstance(lookup, modules.RGSubModuleBase):
					return [lookup]+parse(source[depth:])
		elif isinstance(lookup, functions.RGFunction):
			return [lookup]+parse(source[1:])
def parselist(source):
	"returns list of items, rest of string; expects input to start with [ and end with ]"
	