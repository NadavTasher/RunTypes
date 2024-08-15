import pytest

from runtypes import hintcheck, hintchecker

def test_no_hints():

	@hintchecker
	def my_function(a, b, c, d):
		return (a, b, c, d)

	assert my_function(1, 2, 3, 4) == (1, 2, 3, 4)

def test_some_hints():

	@hintchecker
	def my_function(a, b:str, c, d):
		return (a, b, c, d)

	assert my_function(1, "2", 3, 4) == (1, "2", 3, 4)

	with pytest.raises(TypeError):
		my_function(1, 2, 3, 4)

def test_default_values():

	@hintchecker
	def my_function(a, b:str, c, d: int = 1):
		return (a, b, c, d)

	assert my_function(1, "2", 3) == (1, "2", 3, 1)

	with pytest.raises(TypeError):
		my_function(1, "2", 3, "4")

def test_bad_default_values():

	@hintchecker
	def my_function(a, b:str, c, d: int = "1"):
		return (a, b, c, d)

	assert my_function(1, "2", 3, 1) == (1, "2", 3, 1)

	with pytest.raises(TypeError):
		my_function(1, "2", 3)

def test_kwargs():
	@hintchecker
	def my_function(a, b:str, c = None, d: int = "1"):
		return (a, b, c, d)

	assert my_function(1, "2", 3, d=1) == (1, "2", 3, 1)

	with pytest.raises(TypeError):
		my_function(1, "2", d="A")