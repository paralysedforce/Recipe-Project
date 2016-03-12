

# i is indicator for which transformation to do
# fucntion for performing tranformations will be found in knowledge base
# not sure how to access knowledge base yet
# look into changing portions (easy, and gives extra credit)


def transform(recipe r, i):
	if i == 'pescatarian':
		r = pescatarianize(r)
	if i == 'vegatarian'
		r = vegatarianize(r)
	if i == 'east asian':
		r = eastasianize(r)
	if i == 'italian':
		r = italianize(r)
	if i = 'easy':
		r = easyize(r)
	if i == 'low sodium':
		r = lowsodiumize(r)
	if i == 'low carb':
		r = lowcalorieize(r)


def vegatarianize(recipe r):
	i = 0
	for ing in r.in_list:
		if is_meat(ing):
			r.in_list[i] = replace_ing(ing, 'tofu')
			i+=1

def pescatarianize(recipe r):
	i = 0
	for ing in r.in_list:
		if is_protein(ing):
			if !is_fish():
				r.in_list[i] = replace_ing(ing, 'cod')
				i+=1

# want to replace spices
# startch should be rice or noodles
def eastasianize(recipe r):
	i = 0
	j = 0
	k = 0
	asian_spices = ['ginger','cilantro','sweet basil','red pepper']
	asian_sauces = ['soy sauce', 'sesame oil', 'fish sauce', 'rice wine']
	for ing in r.in_list:
		if is_spice(ing):
			if !is_east_asian(ing):
				if j>=len(asian_spices):
					del r.in_list[i]
					i-=1
				else:
					r.in_list[i] = replace_ing(ing, asian_spices[j])
				j+=1	
		if is_sauce(ing):
			if !is_east_asian(ing):
				if k>=len(asian_sauces):
					del r.in_list[i]
					i-=1
				else:
					r.in_list[i] = replace_ing(ing, asian_sauces[k])
				k+=1
		i+=1

def italianize(recipe r):
	i = 0
	j = 0
	k = 0
	italian_spices = ['oregano','basil','thyme','parsley','black pepper']
	italian_sauces = ['alfredo sauce']
	for ing in r.in_list:
		if is_spice(ing):
			if !is_italian(ing):
				if j>=len(italian_spices):
					del r.in_list[i]
					i-=1
				else:
					r.in_list[i] = replace_ing(ing, italian_spices[j])
					j+=1
		if is_sauce(ing):
			if k>=len(italian_sauces):
				del r.in_list[i]
				i-=1
			else:
				r.in_list[k] = replace_ing(ing, italian_spices[k])
				k+=1
		i+=1


def lowsodiumize(recipe r):
	i = 0
	for ing in r.in_list:
		if is_salty(ing):
			r.in_list[i] = half(ing)
		i+=1

def lowcarbize(recipe r):
	i = 0
	j = 0
	for ing in r.in_list:
		if is_starch(ing):
			if j==0:
				r.in_list[i] = replace_ing[ing, 'quinoa']
				j+=1
			else:
				del r.in_list[i]
				i-=1
			i+=1

def easyize(recipe r):
	i = 0
	for proc in r.pr_list:
		if is_cooking_method(proc):
			r.pr_list[i] = replace_proc(proc, 'bake')
		i+=1


#############
## helpers ##
#############


def replace_ing(ing old, new_name):
	ing new
	new.name = new_name
	new.amount = old.amount
	new.amount_unit = old.amount_unit
	return new

def is_cooking_method(procedure p):

def replace_proc(procedure p, new_name):

def is_starch(ingredient i):

def is_east_asian(ingredient i):

def is_salty(ingredient i):

def is_italian(ingredient i):

def is_fish(ingredient i):

def is_meat(ingredient i):

def is_protein(ingredient i):

def is_spice(ingredient i):

def is_sauce(ingredient i):






















