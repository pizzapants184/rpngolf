from modules import RGSubModule
from functions import RGFunctionFactory
import base
import routines
module = RGSubModule('r')
base.base(module)
#__all__ = ["module"]
apply = base.apply

class RGBreak(Exception):
	pass

@module
@RGFunctionFactory('a', 2)
def ra(stack):
	"while"
	condition = stack.pop()
	action = stack.pop()
	routines.Routine.__call__(condition, stack)
	cond = stack.pop()
	while cond:
		routines.Routine.__call__(action, stack)
		routines.Routine.__call__(condition, stack)
		cond = stack.pop()
@module
@RGFunctionFactory('A', 2)
def rA(stack):
	"until"
	condition = stack.pop()
	action = stack.pop()
	routines.Routine.__call__(condition, stack)
	cond = stack.pop()
	while not cond:
		routines.Routine.__call__(action, stack)
		routines.Routine.__call__(condition, stack)
		cond = stack.pop()
@module
@RGFunctionFactory('b', 2)
def rb(stack):
	"action, items: for item in items, do(action)"
	items = stack.pop()
	action = stack.pop()
	if isinstance(items, (list, str)):
		try:
			for item in items:
				routines.Routine.__call__(action, stack)
		except RGBreak:
			pass
	else:
		raise TypeError
@module
@RGFunctionFactory('B', 2)
def rB(stack):
	"action, items: for item in items, push(item), do(action)"
	items = stack.pop()
	action = stack.pop()
	if isinstance(items, (list, str)):
		try:
			for item in items:
				stack.append(item)
				routines.Routine.__call__(action, stack)
		except RGBreak:
			pass
	else:
		raise TypeError
@module
@RGFunctionFactory('c', 2)
def rc(stack):
	"action, end: for item in range(end), do(action)"
	end = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(end):
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass
@module
@RGFunctionFactory('C', 2)
def rC(stack):
	"action, end: for item in range(end), push(item), do(action)"
	end = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(end):
			stack.append(item)
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass
@module
@RGFunctionFactory('d', 2)
def rd(stack):
	"action, start, end: for item in range(start, end), do(action)"
	end = int(stack.pop())
	start = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(start, end):
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass
@module
@RGFunctionFactory('D', 2)
def rD(stack):
	"action, start, end: for item in range(start, end), push(item), do(action)"
	end = int(stack.pop())
	start = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(start, end):
			stack.append(item)
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass
@module
@RGFunctionFactory('e', 2)
def re(stack):
	"action, start, end, step: for item in range(start, end, step), do(action)"
	step = int(stack.pop())
	end = int(stack.pop())
	start = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(start, end, step):
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass
@module
@RGFunctionFactory('E', 2)
def rE(stack):
	"action, start, end, step: for item in range(start, end, step), push(item), do(action)"
	step = int(stack.pop())
	end = int(stack.pop())
	start = int(stack.pop())
	action = stack.pop()
	try:
		for item in range(start, end, step):
			stack.append(item)
			routines.Routine.__call__(action, stack)
	except RGBreak:
		pass



@module
@RGFunctionFactory('w', 2)
def rw(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a<b))
@module
@RGFunctionFactory('W', 2)
def rW(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a>=b))
@module
@RGFunctionFactory('x', 2)
def rx(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a>b))
@module
@RGFunctionFactory('X', 2)
def rX(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a<=b))
@module
@RGFunctionFactory('y', 2)
def ry(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a==b))
@module
@RGFunctionFactory('Y', 2)
def rY(stack):
	a = stack.pop()
	b = stack.pop()
	stack.append(int(a!=b))
@module
@RGFunctionFactory('z')
def rz(stack):
	raise RGBreak
@module
@RGFunctionFactory('Z', 1)
def rZ(stack):
	item = stack.pop()
	if item:
		raise RGBreak



