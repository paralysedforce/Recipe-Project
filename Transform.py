

# i is indicator for which transformation to do
# fucntion for performing tranformations will be found in knowledge base
# not sure how to access knowledge base yet


def transform(recipe r, i):
	if i == 'vegan':
		r = veganize(r)
	if i == 'vegatarian'
		r = vegatarianize(r)
	if i == 'gluten free'
		r = glutenfreeize(r)
	if i == 'indian':
		r = indianize(r)
	if i == 'east asian':
		r = eastasianize(r)
	if i == 'italian':
		r = italianize(r)
	if i == 'DIY':
		r = diyize(r)
	if i = 'easy':
		r = easyize(r)
	if i == 'low sodium':
		r = lowsodiumize(r)
	if i == 'low calorie':
		r = lowcalorieize(r)
	if i == 'deep fry':
		r = deepfryize(r)
	if i == 'bake':
		r = bakeize(r)


def veganize(recipe r):
	for ing in r.ing_list:
		if is_meat(ing):
			ing = 'tofu'
			# update rest of recipe structure??
		else if is_from_animal(ing)
			if is_egg_pasta(ing):
				ing = 'flour pasta'
			else:
				remove_ing(ing)

def vegatarianize(recipe r):
	for ing in r.ing_list:
		if is_meat(ing):
			ing = 'tofu'

def glutenfreeize(recipe r):
	for ing in r.ing_list:
		if contains_gluten(ing):
			if ing.type == startch: #not sure how to impliment this
				ing = 'rice'

def indianize(recipe r):
	stop_list = ('oregano', 'parsley')
	for ing in r.ing_list:
		if ing is in stop_list
			#remove it
	r.ing_list+= 'paprika, cumin, curry' #keep quanities, not identities





#############
## helpers ##
#############



















