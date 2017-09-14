import state
import base
import parse
import RGmath
import RGlist
import RGloops
import RGcontrol

version = (0, 8, 0, 0)

if __name__ == "__main__":
	import sys
	import getopt
	opts, args = getopt.getopt(sys.argv[1:], 'iVdc:')
	opts = dict(opts)
	if '-V' in opts:
		print("RPNGolf v%d.%d.%d.%d\nhttps://github.com/pizzapants184/rpngolf" % version)
		sys.exit()
	if '-d' in opts:
		state.debug_ = True
	if '-i' in opts:
		while state.running:
			state.do_line(input('> '))
			if state.debug_:
				print(state.stack)
		sys.exit()
	if '-d' in opts:
		state.debug_ = True
	if '-c' in opts:
		if len(args)>1:
			stack_ = args[1][1:-1].split(',')
			for item in stack_:
				if re.match("^-?[0-9]*$", item):
					state.stack.append(int(item))
				elif re.match("^-?([0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)$", item):
					state.stack.append(float(item))
				elif re.match("^('[^']*'|"+'"[^"]*")$', item):
					state.stack.append(item[1:-1])
				else:
					raise ValueError("IDK %s" % item)
		state.do_line(opts['-c'])
		if state.running:
			print(*state.stack)
	else:
		if len(args) == 1:
			state.do_file(args[0])
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
			state.do_file(args[0])
		elif len(args)==0:
			print("Usage:\n\t%s [file] <initial stack>\n\t%s -c [actual code] <initial stack>\n\t%s -i\n\t%s -V" % ((sys.argv[0],)*2))
	
"""import sys
#import getopt
state.do_file(sys.argv[1])
if state.running:
	print(state.stack)"""
