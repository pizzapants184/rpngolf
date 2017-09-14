import re
from modules import RGSubModule
from functions import RGFunctionFactory
import base
import state
module = RGSubModule('t')
base.base(module)
#__all__ = ["module"]
apply = base.apply
@module
@RGFunctionFactory('a')
def ta(stack):
	stack.append(input())
@module
@RGFunctionFactory('b')
def tb(stack):
	stack.append(int(input()))
@module
@RGFunctionFactory('c')
def tc(stack):
	stack.append(float(input()))
@module
@RGFunctionFactory('d')
def td(stack):
	item = input()
	item_ = eval(item, {"__buitins__": None}, {})
	if not isinstance(item_, list):
		raise TypeError
	stack.append(item_)
@module
@RGFunctionFactory('e')
def te(stack):
	stack.append(Routine(input()))
@module
@RGFunctionFactory('f')
def tf(stack):
	item = input()
	stack.append(eval(item, {"__buitins__": None}, {}))
@module
@RGFunctionFactory('A')
def tA(stack):
	"print(stack.pop())"
	print(stack.pop())
@module
@RGFunctionFactory('B')
def tB(stack):
	"print(stack[-1])"
	print(stack[-1])
@module
@RGFunctionFactory('C')
def tC(stack):
	"print(stack)"
	print(stack)
@module
@RGFunctionFactory('D')
def tD(stack):
	"print(stack) separated by spaces"
	for i in range(len(stack)):
		print(item, end=' '*(i==len(stack)-1))
	print()
@module
@RGFunctionFactory('E')
def tE(stack):
	"print(stack) as concatenated strings"
	for i in range(len(stack)):
		print(item, end='')
	print()
@module
@RGFunctionFactory('F')
def tF(stack):
	"print(stack), emptying stack"
	print(stack)
	stack[:] = []
@module
@RGFunctionFactory('G')
def tG(stack):
	"print(stack) separated by spaces, emptying stack"
	print(*stack, sep=' ')
	stack[:] = []
@module
@RGFunctionFactory('H')
def tH(stack):
	"print(stack) as concatenated strings, emptying stack"
	for i in range(len(stack)):
		print(item, end='')
	print()
	stack[:] = []

@module
@RGFunctionFactory('p')
def tp(stack):
	"unconditional immediate quit (no printing)"
	state.running = False
@module
@RGFunctionFactory('P')
def tP(stack):
	"conditional immediate quit (no printing) based on top of stack"
	b = False
	if len(stack) > 0:
		b = stack.pop()
	state.running = bool(b) and state.running
@module
@RGFunctionFactory('q')
def tq(stack):
	"unconditional quit, printing space separated"
	tG(stack) # print space separated
	state.running = False
@module
@RGFunctionFactory('Q')
def tQ(stack):
	"unconditional quit, printing based on arg"
	if len(stack) < 1:
		pass
	elif float(stack[-1]) <= 1.0:
		tG(stack) # print space separated
	elif float(stack[-1]) <= 2.0:
		tH(stack) # print concatenated
	elif float(stack[-1]) <= 3.0:
		tF(stack) # print as list
	state.running = False
@module
@RGFunctionFactory('r')
def tr(stack):
	"conditional quit, printing space separated"
	if len(stack) < 1 or bool(stack[-1]):
		tG(stack) # print space separated
		state.running = False
	else:
		tD(stack) # print space separated, leaving stack
@module
@RGFunctionFactory('R', 1)
def tR(stack):
	"conditional quit, printing based on arg: (bool arg tR) will quit if bool and print if arg (even if it doesnt quit)"
	arg = stack.pop()
	b = False
	if len(stack) > 0:
		b = stack.pop()
	elif float(arg) <= 1.0:
		tD(stack) # print space separated
	elif float(arg) <= 2.0:
		tE(stack) # print concatenated
	elif float(arg) <= 3.0:
		tC(stack) # print as list
	state.running = bool(b) and state.running
	if not state.running:
		stack[:] = []
@module
@RGFunctionFactory('t')
def tt(stack):
	"reverse stack"
	stack[:] = stack[::-1]
@module
@RGFunctionFactory('y')
def ty(stack):
	state.debug_ = True
@module
@RGFunctionFactory('Y')
def tY(stack):
	state.debug_ = False
@module
@RGFunctionFactory('z')
def tz(_):
	"zoom in to top of stack"
	state.stack.zoomin()
	
@module
@RGFunctionFactory('Z')
def tZ(_):
	"zoom out from stack to parent stack"
	state.stack.zoomout()
		