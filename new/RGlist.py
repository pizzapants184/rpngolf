from modules import RGSubModule
from functions import RGFunctionFactory
import base
module = RGSubModule('l')
base.base(module)
#__all__ = ["module"]
apply = base.apply
@module
@RGFunctionFactory('a', 2)
def la(stack):
	"append item to list"
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
@module
@RGFunctionFactory('A', 1)
def lA(stack):
	"pop item from list, keeping list"
	A = stack.pop()
	item = A[-1]
	A = A[:-1]
	stack.append(A)
	stack.append(item)
@module
@RGFunctionFactory('B', 1)
def lB(stack):
	"pop item from list, keeping list"
	A = stack.pop()
	item = A[-1]
	stack.append(item)
@module
@RGFunctionFactory('c', 1)
def lc(stack):
	"max value of list"
	A = stack.pop()
	item = max(A)
	stack.append(item)
@module
@RGFunctionFactory('C', 1)
def lC(stack):
	"min value of list"
	A = stack.pop()
	item = min(A)
	stack.append(item)
@module
@RGFunctionFactory('d', 1)
def ld(stack):
	"all values of list are truthy"
	A = stack.pop()
	item = all(A)
	stack.append(item)
@module
@RGFunctionFactory('D', 1)
def lD(stack):
	"all values of list are falsy"
	A = stack.pop()
	item = all(not x for x in A)
	stack.append(item)
@module
@RGFunctionFactory('e', 1)
def le(stack):
	"any value of list is truthy"
	A = stack.pop()
	item = any(A)
	stack.append(item)
@module
@RGFunctionFactory('E', 1)
def lE(stack):
	"any value of list is falsy"
	A = stack.pop()
	item = any(not x for x in A)
	stack.append(item)
@module
@RGFunctionFactory('G', 2)
def lG(stack):
	"remove item at an index from list, keeping the item"
	B = stack.pop()
	A = stack.pop()
	stack.append(A[int(B)])
@module
@RGFunctionFactory('i', 2)
def li(stack):
	"(a b c li): insert c into a at index b, keeping a"
	C = stack.pop()
	B = stack.pop()
	A = stack.pop()
	A.insert(int(B), C)
	stack.append(A)
@module
@RGFunctionFactory('I', 2)
def lI(stack):
	"remove item from list, keeping list and item"
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	item = A[B]
	A = A[:B]+A[B+1:]
	stack.append(A)
	stack.append(item)
@module
@RGFunctionFactory('J', 2)
def lJ(stack):
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	item = A[B]
	stack.append(item)
@module
@RGFunctionFactory('k', 1)
def lk(stack):
	A = stack.pop()
	try:
		length = len(A)
	except TypeError:
		length = 1
	stack.append(length)
@module
@RGFunctionFactory('K', 2)
def lK(stack):
	B = stack.pop()
	A = stack.pop()
	B = int(B)
	stack.append([A]*B)
@module
@RGFunctionFactory('l', 1)
def ll(stack):
	A = stack.pop()
	try:
		length = len(A)
	except TypeError:
		length = 1
	stack.append(A)
	stack.append(length)
@module
@RGFunctionFactory('L', 1)
def lL(stack):
	A = stack.pop()
	A = int(A)
	stack.append([0]*A)
