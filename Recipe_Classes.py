# Master Classes

class Recipe:
	def __init__(self, url='', name='', transformation='', original_text='', parsed_text='', in_list=[], pr_list=[]):
		self.url = url
		self.name = name
		self.transformation = transformation
		self.original_text = original_text
		self.parsed_text = parsed_text
		self.in_list = in_list
		self.pr_list = pr_list

class Ingredient:
	def __init__(self, name='', amount=0, amount_unit=''):
		self.name = name
		self.amount = amount
		self.amount_unit = amount_unit

class Procedure:
	def __init__(self, name='', in_list=[], time='', temp='', cookware=[]):
		self.name = ''
		self.in_list = []
		self.time = ''
		self.temp = ''
		self.cookware = []




