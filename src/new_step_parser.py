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

	temp_words = ['degrees F', 'medium heat', 'low heat', 'high heat']
	temperatures = []
	temperature_indices = []

	times = []
	time_indices = []

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
			ingredient_indices.append(i-2)
			ingredient_indices.append(i-1)
			ingredient_indices.append(i)
			used_indices.append(i-2)
			used_indices.append(i-1)
			used_indices.append(i)
		elif prev.join(' '+t) in all_ing and prev and i-1 not in used_indices:
			ingredients.append(prev.join(' '+t))
			ingredient_indices.append(i-1)
			ingredient_indices.append(i)
			used_indices.append(i-1)
			used_indices.append(i)
		elif t in all_ing:
			ingredients.append(t)
			ingredient_indices.append(i)
			used_indices.append(i)
		if prev.join(' '+t) in all_actions and prev and i-1 not in used_indices:
			actions.append(prev.join(' '+t))
			action_indices.append(i-1)
			action_indices.append(i)
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
			cookware_indices.append(i-1)
			cookware_indices.append(i)
			used_indices.append(i-1)
			used_indices.append(i)
		elif t in COOKWARE:
			cookware.append(t)
			cookware_indices.append(i)
			used_indices.append(i)
		elif t in TIME:
			times.append(prev.join(' '+t))
			used_indices.append(i-1)
			used_indices.append(i)
			time_indices.append(i-1)
		elif prev.join(' '+t) in temp_words:
			if t is 'heat':
				temperatures.append(prev.join(' '+t))
				temperature_indices.append(i-1)
				temperature_indices.append(i)
				used_indices.append(i-1)
				used_indices.append(i)				
			else:
				temperatures.append(prev2.join(' '+prev.join(' '+t)))
				temperature_indices.append(i-2)
				temperature_indices.append(i-1)
				temperature_indices.append(i)
				used_indices.append(i-2)
				used_indices.append(i-1)
				used_indices.append(i)	
		elif t in all_separators and i != len(tokens):
			separators.append(t)
			separator_indices.append(i)
			used_indices.append(i)

	print "\n\n\nSTEP: "
	print ingredients
	print actions
	print cookware
	print separators
	print temperatures
	print times

	clause = 1
	clause_actions = []
	clause_ingredients = []
	clause_cookware = []
	clause_time = ''
	clause_temp = ''
	prev_ings = []
	step_procedures = []
	i = 0
	procedure = recipe_classes.Procedure()
	while i < (len(tokens)):

		t = tokens[i]

		if i in action_indices:
			if i < len(tokens)-2:
				if tokens[i+1] is 'and' or tokens[i+1] is 'then':
					if i+2 in action_indices:
						clause_actions.append(t)
						clause_actions.append(tokens[i+2])
						i += 3
						continue
					if i < len(tokens)-3:
						if tokens[i+2] is 'and' or tokens[i+2] is 'then':
							if i+3 in action_indices:
								clause_actions.append(t)
								clause_actions.append(tokens[i+3])
								i += 4
								continue
			clause_actions.append(t)
			i += 1
			continue

		if t in separators and i+1 not in ingredient_indices and clause_actions:
			clause += 1
			prev_ings = clause_ingredients
			actions = clause_actions[0]
			for action in clause_actions[1:]:
				actions += ', '+action
			procedure.name = actions
			if clause_ingredients:
				procedure.in_list = clause_ingredients
			else:
				procedure.in_list = prev_ings
			if clause_cookware:
				procedure.cookware = clause_cookware
			else:
				procedure.cookware = []
			if clause_time:
				procedure.time = clause_time
			else:
				procedure.time = ''
			if clause_temp:
				procedure.temp = clause_temp
			else:
				procedure.temp = ''
			step_procedures.append(procedure)
			clause_actions = []
			clause_ingredients = []
			clause_cookware = []
			clause_time = ''
			clause_temp = ''
			procedure = recipe_classes.Procedure()
			i += 1
			continue

		if i in ingredient_indices:
			if i < len(tokens)-1:
				if i+1 in ingredient_indices:
					if i < len(tokens)-2
						if i+2 in ingredient_indices:
							# do something with three worded ingredient
							i += 3
							continue
						else:
							# do something with two worded ingredient
							i += 2
							continue
				else:
					# do something with one worded ingredient
					i += 1
					continue

		if t is 'them':
			clause_ingredients = prev_ings
			i += 1
			continue

		if i in time_indices:
			clause_time = tokens[i]+' '+tokens[i+1]
			if i+3 in time_indices:
				clause_time += tokens[i+3]+' '+tokens[i+4]
				i += 5
				continue
			i += 2
			continue

		if i in temperature_indices:
			clause_temp = tokens[i]+' '+tokens[i+1]
			if i+2 in temperature_indices:
				clause_temp += ' '+tokens[i+2]
				i += 3
				continue
			i += 2
			continue

		print "---------ALERT END---------"
		i += 1

	return step_procedures




