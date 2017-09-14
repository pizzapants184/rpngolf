import abc
from collections import defaultdict
from functions import RGFunction
from routines import Routine
class RGModuleBase(abc.ABC):
	@abc.abstractmethod
	def __init__(self):
		pass
	@abc.abstractmethod
	def __call__(self, func):
		return func
	def fullname(self):
		if self.module is None:
			return self.name
		else:
			return self.module.fullname() + self.name
class RGBase(RGModuleBase): # Maybe make this a singleton?
	def __init__(self):
		self.name = ''
		self.identifiers = {}
		self.module = None
	def __call__(self, func):
		if isinstance(func, (RGFunction, RGSubModuleBase)):
			#if func.name in 'abcdefghijklmnopqrstuvwxyz' and len(func.name) == 1:
			if len(func.name) == 1:
				if func.name not in self.identifiers:
					self.identifiers[func.name] = func
					self.identifiers[func.name].module = self
				else:
					print(self.identifiers[func.name], func.name)
					raise ValueError("Name already used: %s" % func.name)
			else:
				raise ValueError("Invalid Name")
		else:
			raise TypeError
		return func
	def __getitem__(self, item):
		if not isinstance(item, str):
			raise TypeError
		if len(item) < 1:
			raise TypeError
		elif len(item) == 1:
			ret = self.identifiers[item]
			return ret
		elif len(item) > 1:
			ret = self.identifiers[item[0]]
			return ret[item[1:]]
class RGSubModuleBase(RGModuleBase):
	pass

class RGSubModule(RGSubModuleBase):
	def __init__(self, name):
		self.name = name
		self.identifiers = {}
		self.module = None
	def __call__(self, func):
		if isinstance(func, (RGFunction, RGSubModuleBase)):
			if len(func.name) == 1:
				if func.name not in self.identifiers:
					self.identifiers[func.name] = func
					self.identifiers[func.name].module = self
				else:
					print(self.identifiers[func.name], func.name)
					raise ValueError("Name already used: %s" % func.name)
					#self.identifiers['!'] = self.identifiers[func.name]
					#self.identifiers['!'].module = self
					#self.identifiers[func.name] = func
					#self.identifiers[func.name].module = self
			else:
				raise ValueError("Invalid Name")
		else:
			raise TypeError
		return func
	def __getitem__(self, item):
		if not isinstance(item, str):
			raise TypeError
		if len(item) < 1:
			raise TypeError
		elif len(item) == 1:
			ret = self.identifiers[item]
			return ret
		elif len(item) > 1:
			ret = self.identifiers[item[0]]
			return ret[item[1:]]
class RGSpecialModuleBase(RGSubModuleBase):
	pass
class Reader(RGSpecialModuleBase):
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
		self.module = None
	def __getitem__(self, item):
		return Value(self, item)
	def __call__(self, func):
		raise TypeError
class Setter(RGSpecialModuleBase):
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
		self.module = None
	def __getitem__(self, item):
		return Value(self, item)
	def __call__(self, func):
		raise TypeError
class Caller(RGSpecialModuleBase):
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
		self.module = None
	def __getitem__(self, item):
		return Value(self, item)
	def __call__(self, func):
		raise TypeError
class Value(RGFunction):
	def __init__(self, parent, name):
		self.parent = parent
		self.module = parent
		self.name = name
	def __call__(self, stack):
		if isinstance(self.parent, Reader):
			stack.append(self.parent.parent[self.name])
		elif isinstance(self.parent, Setter):
			self.parent.parent[self.name] = stack.pop()
		elif isinstance(self.parent, Caller):
			item = self.parent.parent[self.name]
			item = Routine(item)
			item(stack)
class VarModule:
	def __init__(self):
		self.vars = {}
	def reader(self, name):
		return Reader(self, name)
	def setter(self, name):
		return Setter(self, name)
	def caller(self, name):
		return Caller(self, name)
	def __getitem__(self, item):
		return self.vars[item]
	def __setitem__(self, item, val):
		self.vars[item] = val
	def __delitem__(self, item):
		del self.vars[item]
		