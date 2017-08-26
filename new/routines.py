import parse
class Routine:
	def __init__(self, source):
		self.source = str(source)
		self.calls = parse.parse(self.source)
		