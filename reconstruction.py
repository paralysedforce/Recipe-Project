#reconstruction

import Recipe_Classes
import Transform

# consider inpmilmenting cooking time/prep time, etc

# ingredient list and quantities

# procedure text

def reconstruct(recipe r):
	fs = ''
	fs.append(r.name + '    ' + 'transformed to fit the following criteria: ' + r.transormation + '\n\nIngredients.\n')
	for ing in r.in_list:
		line = '\t-' + ing.name + '  ' + ing.amount + ' ' + ing.amount_unit +'\n'
		fs.append(line)
	fs.append('\nSteps\n')
	tr = ['Next', 'Now', 'After that']
	i = 1
	j = 0
	for proc in r.pr_list:
		line = ''
		if i==1:
			line = 'First, '
		elif i = len(r.pr_list):
			line = 'Finally, '
		else:
			if j>=len(tr):
				j = 0
			line.append(tr[j])
			j+=1
		if is_cooking_method(proc):
			line.append('with ' + proc.cookware + ',' + proc.name + ' ' + (for i in proc.in_list i + ' and ') + '.')
		else:
			line.append(proc.name + ' ' + (for i in proc.in_list i + ' and ') + '.')
		fs.append(line + '\n')
		i+=1
	print(fs)


		
