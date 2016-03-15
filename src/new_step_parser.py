from data import *
import scrape

import sys
#from collections import namedtuple
from string import punctuation
import re
import nltk
from pymongo import MongoClient
import recipe_classes
import reconstruction
import transform

client = MongoClient()

db = client["k_base"]

def parse_step(step):
	tokens = nltk.word_tokenize(step)

	ingredient_indices = []
	ingredients = []
	action_indices = []
	actions = []
	cookware_indices = []
	cookware = []

	all_actions = []
	action_cursor = db.procedures.find()
	for doc in action_cursor:
		name = doc['name']
		all_actions.append(name)

	all_ing = []
	ing_cursor = db.ingredients.find()
	for doc in ing_cursor:
		name = doc['name']
		all_ing.append(name)

	all_separators = [',',';','.','and','then']
	separator_indices = []
	separators = []

	used_indices = []

	for i in range(len(tokens)):
		if i == 0:
			prev = ''
			prev2 = ''
		elif i == 1:
			prev2 = ''
			prev = t
		else:
			prev2 = prev
			prev = t

		t = tokens[i]
		tokens[i] = t.lower()

		if prev2.join(' '+prev.join(' '+t)) in all_ing and prev2 and prev and i-1 not in used_indices and i-2 not in used_indices:
			ingredients.append(prev2.join(' '+prev.join(' '+t)))
			ingredient_indices.append([i-2, i-1, i])
			used_indices.append(i-2)
			used_indices.append(i-1)
			used_indices.append(i)
		elif prev.join(' '+t) in all_ing and prev and i-1 not in used_indices:
			ingredients.append(prev.join(' '+t))
			ingredient_indices.append([i-1, i])
			used_indices.append(i-1)
			used_indices.append(i)
		elif t in all_ing:
			ingredients.append(t)
			ingredient_indices.append(i)
			used_indices.append(i)
		if prev.join(' '+t) in all_actions and prev and i-1 not in used_indices:
			actions.append(prev.join(' '+t))
			action_indices.append([i-1, i])
			used_indices.append(i-1)
			used_indices.append(i)
		elif t in all_actions:
			if i in used_indices:
				print "INGREDIENT AND PROCEDURE!!!!"
			else:
				actions.append(t)
				action_indices.append(i)
				used_indices.append(i)
		elif prev.join(' '+t) in COOKWARE and prev and i-1 not in used_indices:
			cookware.append(prev.join(' '+t))
			cookware_indices.append([i-1, i])
			used_indices.append(i-1)
			used_indices.append(i)
		elif t in COOKWARE:
			cookware.append(t)
			cookware_indices.append(i)
			used_indices.append(i)
		elif t in all_separators and i != len(tokens):
			separators.append(t)
			separator_indices.append(i)
			used_indices.append(i)

	print ingredients
	print actions
	print cookware
	print separators





	name = ''
	in_list = []
	cookware = []
	time = ''
	temp = ''
	new_r = recipe_classes.Procedure(name, in_list, cookware, time, temp)
	all_actions.append(new_r)



