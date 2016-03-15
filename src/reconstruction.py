#reconstruction

import recipe_classes
import transform

# consider inpmilmenting cooking time/prep time, etc

# ingredient list and quantities

# procedure text

def reconstruct(r):
    fs = ''
    print r
    fs += '%s\ttransformed to fit the following criteria: %s' % (r.name, r.transformation)
    fs += "\n\nIngredients:\n"
    for ing in r.in_list:
        fs += '\t-%s  %s %s\n' % (ing.name, str(ing.amount), ing.amount_unit)
    fs += '\nSteps:\n'
    transitions = ['Next, ', 'Now, ', 'After that, ']
    step_count = 1
    j = 0
    for proc in r.pr_list:
        line = ''
        if step_count == 1:
            line = 'First, '
        elif step_count == len(r.pr_list):
		    line = 'Finally, '
        else:
            line += transitions[step_count % len(transitions)]

        if transform.is_cooking_method(proc):
            if proc.cookware:
                line += 'with ' 
                line += ' and cookware: '.join(cookware for cookware in proc.cookware)
            line += ' ' + proc.name
            if proc.in_list:
                line += ', '.join(i for i in proc.in_list[:-1]) + ', and %s ' % proc.in_list[-1]
            if proc.time:
            	line += ' for {time}'.format(time=proc.time)
            if proc.temp:
            	line += ' at {temp}'.format(temp=proc.temp)
            line += '.'
        else:
            line += proc.name 
            if proc.in_list:
                line += ' ' + ', '.join(ing for ing in proc.in_list) 
            if proc.time:
            	line += ' for {time}'.format(time=proc.time)
            if proc.temp:
            	line += ' at {temp}'.format(temp=proc.temp)
            line += '.'

        fs += line + '\n'
        step_count += 1
    print str(fs)
