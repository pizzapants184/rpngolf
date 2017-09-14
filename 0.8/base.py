from modules import RGBase, RGSubModule, VarModule
from functions import RGFunction, RGFunctionFactory, coerce
import routines
import state
import copy
def apply(func, item):
	if isinstance(item, list):
		ret = []
		for i in item:
			ret.append(apply(func, i))
		return ret
	else:
		return func(item)
def apply1_2(func, item):
	if isinstance(item, list):
		a = []
		b = []
		for i in item:
			a_, b_ = apply1_2(func, i)
			a.append(a_)
			b.append(b_)
		return a, b
	else:
		return func(item)
def applyn_1(func, *items):
	if isinstance(items[0], list):
		ret = []
		for i in range(len(items[0])):
			ret.append(applyn_1(func, *(item[i] for item in items)))
		return ret
	else:
		return func(*items)
def apply1_n(func, item, n):
	if isinstance(item, list):
		rets = [[] for i in range(n)]
		for i in item:
			it = apply1_n(func, i, n)
			for j in range(n):
				rets[j].append(it[j])
		return tuple(rets)
	else:
		return func(item)

base = RGBase()
state.base = base
@base
@RGFunctionFactory('+', 2)
def add(stack):
	"a+b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A+B)
@base
@RGFunctionFactory('-', 2)
def sub(stack):
	"a-b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A-B)
@base
@RGFunctionFactory('*', 2)
def mul(stack):
	"a*b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A*B)
@base
@RGFunctionFactory('/', 2)
def div(stack):
	"a/b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A/B)
@base
@RGFunctionFactory('^', 2)
def pow_(stack):
	"a**b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A**B)
@base
@RGFunctionFactory('f', 2)
def floordiv(stack):
	"a//b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A//B)
@base
@RGFunctionFactory('%', 2)
def mod(stack):
	"a%b, basic, no coercion"
	B = stack.pop()
	A = stack.pop()
	stack.append(A%B)
@base
@RGFunctionFactory('g')
def rotatedown(stack):
	"rotate bottom of stack to top"
	if len(stack) > 0:
		stack.append(stack.pop(0))
@base
@RGFunctionFactory('G')
def rotateup(stack):
	"rotate top of stack to bottom"
	if len(stack) > 0:
		stack.insert(0, stack.pop())
@base
@RGFunctionFactory('h', 1)
def dec(stack):
	"decrement: a-1"
	A = stack.pop()
	stack.append(A-1)
@base
@RGFunctionFactory('i', 1)
def inc(stack):
	"increment: a+1"
	A = stack.pop()
	stack.append(A+1)
@base
@RGFunctionFactory('j', 1)
def call(stack):
	"call as Routine"
	A = stack.pop()
	A = routines.Routine(A)
	A(stack)
#k is coercion module
#l is list/string module
#m is math module
@base
@RGFunctionFactory('n', 1)
def n(stack):
	"range(a)"
	def range_(A):
		if isinstance(A, int):
			return list(range(A))
		elif isinstance(A, float):
			if not A % 1:
				return list(range(int(A)))
			else:
				raise ValueError("range of a non-integral float")
		elif isinstance(A, str):
			r = []
			for i in range(len(A)):
				r.append(A[:i+1])
			return r
		elif hasattr(A, "__iter__"):
			r = []
			for item in A:
				r.append(range_(item))
			return r
		else:
			raise TypeError("range of %r" % type(A))
	A = stack.pop()
	stack.append(range_(A))
@base
@RGFunctionFactory('o', 1)
def o(stack):
	"pop"
	stack.pop()
@base
@RGFunctionFactory('p', 1)
def p(stack):
	"duplicate"
	A = stack.pop()
	stack.append(A)
	_A = copy.deepcopy(A)
	stack.append(_A)
@base
@RGFunctionFactory('q')
def quitnow(stack):
	"quit without printing"
	state.running = False
@base
@RGFunctionFactory('Q')
def quit(stack):
	"quit with printing"
	print(*stack, sep=' ')
	state.running = False
#r is condition/loop module
@base
@RGFunctionFactory('s', 2)
def swap(stack):
	"swap top two elements"
	B = stack.pop()
	A = stack.pop()
	stack.append(B)
	stack.append(A)
#t is control module
#u is recall vars
#v is store vars
#w is call vars
@base
@RGFunctionFactory('x', 3)
def if1(stack):
	"(T F C x): if the top of the stack is truthy after C is called, call T, else call F"
	C = stack.pop()
	F = stack.pop()
	T = stack.pop()
	condition_routine = coerce(C, Routine)
	false_routine = coerce(F, Routine)
	true_routine = coerce(T, Routine)
	condition_routine(stack)
	condition = stack.pop()
	if condition:
		true_routine(stack)
	else:
		false_routine(stack)
@base
@RGFunctionFactory('y', 3)
def if2(stack):
	"(F T C y): if the top of the stack is truthy after C is called, call T, else call F"
	C = stack.pop()
	T = stack.pop()
	F = stack.pop()
	condition_routine = coerce(C, Routine)
	true_routine = coerce(T, Routine)
	false_routine = coerce(F, Routine)
	condition_routine(stack)
	condition = stack.pop()
	if condition:
		true_routine(stack)
	else:
		false_routine(stack)
@base
@RGFunctionFactory('z')
def z(stack):
	raise NotImplementedError


vars = VarModule()
u = vars.reader('u')
base(u)
v = vars.setter('v')
base(v)
w = vars.caller('w')
base(w)



k = RGSubModule('k')
base(k)
@k
@RGFunctionFactory('a', 1)
def ka(stack):
	"coerce to int"
	A = stack.pop()
	try:
		A_ = int(A)
	except ValueError:
		if False:
			pass
		else:
			raise
	stack.append(A_)
@k
@RGFunctionFactory('b', 1)
def kb(stack):
	"coerce to float"
	A = stack.pop()
	try:
		A_ = float(A)
	except ValueError:
		if False:
			pass
		else:
			raise
	stack.append(A_)
@k
@RGFunctionFactory('c', 1)
def kc(stack):
	"coerce to string"
	A = stack.pop()
	A_ = str(A)
	stack.append(A_)
@k
@RGFunctionFactory('d')
def kd(stack):
	"convert whole stack to list"
	stack_ = copy.deepcopy(stack)
	stack[:] = [stack_]
@k
@RGFunctionFactory('e', 1)
def ke(stack):
	"coerce to Routine"
	A = stack.pop()
	A_ = Routine(A)
	stack.append(A_)
@k
@RGFunctionFactory('f', 1)
def kf(stack):
	"wrap top of stack in list"
	A = stack.pop()
	stack.append([A])
@k
@RGFunctionFactory('h', 1)
def kh(stack):
	"coerce to char by code point"
	def func(i):
		if not isinstance(i, list):
			return chr(int(i))
	A = stack.pop()
	out = apply(func, A)
	if not isinstance(out, list):
		return out
	else:
		ret = []
		if len(out) < 1:
			return ret
		else:
			ret.append(out[0])
		for item in out[1:]:
			if isinstance(item, str) and isinstance(ret[-1], str):
				ret[-1] += item
			else:
				ret.append(item)
	return ret
@k
@RGFunctionFactory('H', 1)
def kH(stack):
	"coerce str to list of ints by code point"
	def func(s):
		return [ord(c) for c in s]
	A = stack.pop()
	stack.append(apply(func, A))
@k
@RGFunctionFactory('r', 1)
def kr(stack):
	"coerce to string by python3 repr()"
	A = stack.pop()
	A_ = repr(A)
	stack.append(A_)
#from lists import 