import parse
import state
class Routine:
	def __init__(self, source):
		self.source = str(source)
		self.calls = parse.parse(self.source)
	def __repr__(self):
		return '('+self.source+')'
	def __call__(self, stack):
		state.do_items(self.calls)
	def __mul__(self, other):
		if isinstance(other, (int, float, str)) and int(other) >= 0:
			return Routine(self.source*int(other))
		else:
			raise NotImplemented
	def __rmul__(self, other):
		if isinstance(other, (int, float, str)) and int(other) >= 0:
			return Routine(self.source*int(other))
		else:
			raise NotImplemented