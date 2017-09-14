import numbers
import copy
def coerce(val, typ):
	if isinstance(val, typ):
		return val
	elif typ is list:
		if hasattr(val, '__iter__'):
			return list(val)
		else:
			return [val]
	else:
		return typ(val)

class RGFunctionFactory:
	def __init__(self, name, argc=None):
		if len(name) != 1:
			raise ValueError("Invalid name: %s"%name)
		self.argc = argc if argc is not None else 0
		self.name = name
	def __call__(self, func):
		return RGFunction(func, self.name, self.argc)
class RGFunction:
	def __init__(self, func, name, argc):
		self.func = func
		self.__doc__ = func.__doc__
		self.name = name
		self.argc = argc
		self.module = None
	def __call__(self, stack):
		if len(stack) < self.argc:
			raise ValueError("not enough items on stack for %s: %d < %d" % (self.fullname(), len(stack), self.argc))
		#_s = copy.deepcopy(stack)
		self.func(stack)
	def __repr__(self):
		return "<RGFunction: %r>" % self.fullname()
	def fullname(self):
		if self.module is None:
			return self.name
		else:
			return self.module.fullname() + self.name
		