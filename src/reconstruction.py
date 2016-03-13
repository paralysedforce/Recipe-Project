#reconstruction

import recipe_classes
import transform

# consider inpmilmenting cooking time/prep time, etc

# ingredient list and quantities

# procedure text

def reconstruct(r):
	fs = ''
	fs += r.name + '    ' + 'transformed to fit the following criteria: ' + r.transformation + '\n\nIngredients:\n'
	for ing in r.in_list:
		line = '\t-' + ing.name + '  ' + str(ing.amount) + ' ' + ing.amount_unit +'\n'
		fs += line
	fs += '\nSteps:\n'
	tr = ['Next', 'Now', 'After that']
	i = 1
	j = 0
	for proc in r.pr_list:
		line = ''
		if i==1:
			line = 'First, '
		elif i == len(r.pr_list):
			line = 'Finally, '
		else:
			if j>=len(tr):
				j = 0
			line += tr[j]
			j+=1
		if transform.is_cooking_method(proc):
			line += 'with ' + ''.join([i_ + ' and ' for i_ in proc.cookware]) + ',' + proc.name + ' '.join([i_ + ' and ' for i_ in proc.in_list]) + ' for ' + proc.time + ' at ' + proc.temp + '.'
		else:
			line += proc.name + ' ' + ''.join([i_ + ' and ' for i_ in proc.in_list]) + '.'
		fs += line + '\n'
		i += 1
	print str(fs)


		
