import math

from modules import RGSubModule
from functions import RGFunctionFactory
import base
module = RGSubModule('m')
#__all__ = ["module"]
apply = base.apply
apply1_2 = lambda *a: base.apply1_n(*a, 2)
apply1_n = base.apply1_n
applyn_1 = base.applyn_1
@module
@RGFunctionFactory('a', 1)
def ma(stack):
	"sin"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.sin(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('A', 1)
def mA(stack):
	"asin"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.asin(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('b', 1)
def mb(stack):
	"cos"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.cos(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('B', 1)
def mB(stack):
	"acos"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.acos(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('c', 1)
def mc(stack):
	"tan"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.tan(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('C', 1)
def mC(stack):
	"atan"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.atan(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('d', 1)
def md(stack):
	"(sin, cos)"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.sin(float(item)), math.cos(float(item))
		else:
			raise TypeError
	item = stack.pop()
	sines, coses = apply1_2(func, item)
	stack.append(sines)
	stack.append(coses)
@module
@RGFunctionFactory('D', 2)
def mD(stack):
	"atan2: y, x -> angle"
	def func(s, c):
		if isinstance(s, (int, float, str)) and isinstance(c, (int, float, str)):
			return math.atan2(float(s), float(c))
		else:
			raise TypeError
	itemC = stack.pop()
	itemS = stack.pop()
	stack.append(applyn_1(func, itemS, itemC))
@module
@RGFunctionFactory('e', 1)
def me(stack):
	"csc"
	def func(item):
		if isinstance(item, (int, float, str)):
			return 1/math.sin(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('E', 1)
def mE(stack):
	"acsc"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.asin(1/float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('f', 1)
def mf(stack):
	"sec"
	def func(item):
		if isinstance(item, (int, float, str)):
			return 1/math.cos(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('F', 1)
def mF(stack):
	"asec"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.acos(1/float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('g', 1)
def mg(stack):
	"cot"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.tan((math.pi/2)-float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('G', 1)
def mG(stack):
	"acot"
	def func(item):
		if isinstance(item, (int, float, str)):
			return (math.pi/2)-math.atan(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('h', 1)
def mh(stack):
	"(cos, sin)"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.cos(float(item)), math.sin(float(item))
		else:
			raise TypeError
	item = stack.pop()
	coses, sines = apply1_2(func, item)
	stack.append(coses)
	stack.append(sines)
@module
@RGFunctionFactory('H', 2)
def mH(stack):
	"acot2: x,y -> angle"
	def func(c, s):
		if isinstance(s, (int, float, str)) and isinstance(c, (int, float, str)):
			return math.atan2(float(s), float(c))
		else:
			raise TypeError
	itemS = stack.pop()
	itemC = stack.pop()
	stack.append(applyn_1(func, itemC, itemS))
@module
@RGFunctionFactory('i', 1)
def mi(stack):
	"natural log"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.log(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('I', 1)
def mI(stack):
	"e**x"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.e**float(item)
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('j', 1)
def mj(stack):
	"log base 10"
	def func(item):
		if isinstance(item, (int, float, str)):
			return math.log10(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('J', 1)
def mJ(stack):
	"10**x"
	def func(item):
		if isinstance(item, (int, float, str)):
			return 10**float(item)
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('k', 2)
def mk(stack):
	"log base n: a, b -> math.log(a, b)"
	def func(a, b):
		if isinstance(a, (int, float, str)) and isinstance(b, (int, float, str)):
			return math.log(float(a), float(b))
		else:
			raise TypeError
	b = stack.pop()
	a = stack.pop()
	stack.append(applyn_1(func, a, b))
@module
@RGFunctionFactory('l', 1)
def ml(stack):
	"sign"
	def func(item):
		if isinstance(item, (int, float, str)):
			item = float(item)
			if item < 0:
				return -1
			elif item > 0:
				return 1
			else:
				return 0
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('L', 1)
def mL(stack):
	"abs"
	def func(item):
		if isinstance(item, (int, float, str)):
			return abs(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('m', 1)
def mm(stack):
	"log base 2"
	def func(a):
		if isinstance(a, (int, float, str)):
			return math.log(float(a), 2)
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('M', 1)
def mM(stack):
	"2**x"
	def func(a):
		if isinstance(a, (int, float, str)):
			return 2**float(a)
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))





@module
@RGFunctionFactory('w', 1)
def ms(stack):
	"apply collatz function once, ignoring 1 -> 4"
	def func(a):
		if (isinstance(a, (int, str)) and int(a) >= 1) or (isinstance(a, float) and a >= 1 and (a%1 == 0)):
			if int(a) == 1:
				return int(a)
			elif int(a)%2: # odd
				return 3*int(a)+1
			else:
				return int(a)//2
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))
@module
@RGFunctionFactory('W')
def mW(stack):
	"apply inverse collatz function once, ignoring 4 -> 1"
	def func(a):
		if (isinstance(a, (int, str)) and int(a) >= 1) or (isinstance(a, float) and a >= 1 and (a%1 == 0)):
			if int(a)%6 == 4 and int(a) != 4:
				return [int(a)*2, (int(a)-1)//3]
			else:
				return int(a)*2
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))



@module
@RGFunctionFactory('x')
def mx(stack):
	"pi"
	stack.append(math.pi)
@module
@RGFunctionFactory('X')
def mX(stack):
	"tau"
	stack.append(2*math.pi)
@module
@RGFunctionFactory('y')
def my(stack):
	"e"
	stack.append(math.pi)
@module
@RGFunctionFactory('Y')
def mY(stack):
	"e**(-1)"
	stack.append(1/math.e)
@module
@RGFunctionFactory('z')
def mz(stack):
	"phi (golden ratio)"
	stack.append((1+5**(1/2))/2)
@module
@RGFunctionFactory('Z')
def mZ(stack):
	"conjugate of phi"
	stack.append((1-5**(1/2))/2)


base.base(module)