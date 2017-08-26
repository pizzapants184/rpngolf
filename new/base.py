from modules import RGBase, RGSubModule
from functions import RGFunction, RGFunctionFactory, coerce
#from routines import Routine
import state
import copy

base = RGBase()
state.base = base
@base
@RGFunctionFactory('a', 2)
def a(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A+B)
@base
@RGFunctionFactory('b', 2)
def b(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A-B)
@base
@RGFunctionFactory('c', 2)
def c(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A*B)
@base
@RGFunctionFactory('d', 2)
def d(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A/B)
@base
@RGFunctionFactory('e', 2)
def e(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A**B)
@base
@RGFunctionFactory('f', 2)
def f(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A//B)
@base
@RGFunctionFactory('g', 2)
def g(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A%B)
@base
@RGFunctionFactory('h', 1)
def h(stack):
	A = stack.pop()
	stack.append(A-1)
@base
@RGFunctionFactory('i', 1)
def i(stack):
	A = stack.pop()
	stack.append(A+1)
@base
@RGFunctionFactory('j', 1)
def j(stack):
	A = stack.pop()
	A = Routine(A)
	A(stack)
#k is coercion module
#l is list/string module
#m is math module
@base
@RGFunctionFactory('n', 1)
def n(stack):
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
	stack.pop()
@base
@RGFunctionFactory('p', 1)
def p(stack):
	A = stack.pop()
	stack.append(A)
	_A = copy.deepcopy(A)
	stack.append(_A)
@base
@RGFunctionFactory('q')
def q(stack):
	state.running = False
#r is condition/loop module
@base
@RGFunctionFactory('s', 2)
def s(stack):
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
def x(stack):
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
def y(stack):
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


k = RGSubModule('k')
base(k)
@k
@RGFunctionFactory('a', 1)
def ka(stack):
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
	A = stack.pop()
	A_ = str(A)
	stack.append(A_)
@k
@RGFunctionFactory('d')
def kd(stack):
	stack_ = copy.deepcopy(stack)
	stack[:] = [stack_]
@k
@RGFunctionFactory('e', 1)
def ke(stack):
	A = stack.pop()
	A_ = Routine(A)
	stack.append(A_)
@k
@RGFunctionFactory('f', 1)
def kf(stack):
	A = stack.pop()
	stack.append([A_])
@k
@RGFunctionFactory('h', 1)
def kh(stack):
	A = stack.pop()
	A_ = int(A)
	stack.append(chr(A))
@k
@RGFunctionFactory('r', 1)
def kr(stack):
	A = stack.pop()
	A_ = repr(A)
	stack.append(A_)

l = RGSubModule('l')
base(l)
@l
@RGFunctionFactory('a', 2)
def la(stack):
	B = stack.pop()
	A = stack.pop()
	if isinstance(A, list):
		A.append(B)
		stack.append(A)
	elif isinstance(A, str):
		A += str(B)
		stack.append(A)
	else:
		raise TypeError("Can only append to list or string")
@l
@RGFunctionFactory('A', 1)
def lA(stack):
	A = stack.pop()
	item = A[-1]
	A = A[:-1]
	stack.append(A)
	stack.append(item)
@l
@RGFunctionFactory('B', 1)
def lB(stack):
	A = stack.pop()
	item = stack[-1]
	stack.append(item)
@l
@RGFunctionFactory('c', 1)
def lc(stack):
	A = stack.pop()
	item = max(A)
	stack.append(item)
@l
@RGFunctionFactory('C', 1)
def lC(stack):
	A = stack.pop()
	item = min(A)
	stack.append(item)
@l
@RGFunctionFactory('d', 1)
def ld(stack):
	A = stack.pop()
	item = all(A)
	stack.append(item)
@l
@RGFunctionFactory('D', 1)
def lD(stack):
	A = stack.pop()
	item = all(not x for x in A)
	stack.append(item)
@l
@RGFunctionFactory('e', 1)
def le(stack):
	A = stack.pop()
	item = any(A)
	stack.append(item)
@l
@RGFunctionFactory('E', 1)
def lE(stack):
	A = stack.pop()
	item = any(not x for x in A)
	stack.append(item)
@l
@RGFunctionFactory('G', 2)
def lG(stack):
	B = stack.pop()
	A = stack.pop()
	stack.append(A[int(B)])
@l
@RGFunctionFactory('i', 2)
def li(stack):
	C = stack.pop()
	B = stack.pop()
	A = stack.pop()
	A.insert(int(B), C)
	stack.append(A)
@l
@RGFunctionFactory('I', 2)
def lI(stack):
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	item = A[B]
	A = A[:B]+A[B+1:]
	stack.append(A)
	stack.append(item)
@l
@RGFunctionFactory('J', 2)
def lJ(stack):
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	item = A[B]
	stack.append(item)
@l
@RGFunctionFactory('k', 1)
def lk(stack):
	A = stack.pop()
	try:
		length = len(A)
	except TypeError:
		length = 1
	stack.append(length)
@l
@RGFunctionFactory('K', 2)
def lK(stack):
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	stack.append([A]*B)
@l
@RGFunctionFactory('l', 1)
def ll(stack):
	A = stack.pop()
	try:
		length = len(A)
	except TypeError:
		length = 1
	stack.append(A)
	stack.append(length)
@l
@RGFunctionFactory('L', 1)
def lL(stack):
	A = stack.pop()
	A = int(A)
	stack.append([0]*A)
