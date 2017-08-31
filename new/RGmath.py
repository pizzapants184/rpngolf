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
			return math.log(a, b)
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
def ML(stack):
	"abs"
	def func(item):
		if isinstance(item, (int, float, str)):
			return abs(float(item))
		else:
			raise TypeError
	item = stack.pop()
	stack.append(apply(func, item))

base.base(module)