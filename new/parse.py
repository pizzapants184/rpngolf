import state
import modules
import functions
def parse(source):
	if len(source)<1:
		return []
	if source[0] == "'":
		pass
	elif source[0] == '(':
		pass
	else:
		lookup = state.base[source[0]]
		if isinstance(lookup, modules.RGSubModuleBase):
			depth = 1
			trace = [lookup]
			while True:
				lookup = lookup[source[depth]]
				depth += 1
				trace.append(lookup)
				if isinstance(lookup, functions.RGFunction):
					return [lookup]+parse(source[depth:])

		elif isinstance(lookup, functions.RGFunction):
			return [lookup]+parse(source[1:])