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

    temp_words = ['degrees f', 'medium heat', 'low heat', 'high heat', 'degrees F']
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

        if prev2+' '+prev+' '+t in all_ing:
            if i-2 in ingredients
            ingredients.append(prev2+' '+prev+' '+t)
            ingredient_indices.append(i-2)
            ingredient_indices.append(i-1)
            ingredient_indices.append(i)
            used_indices.append(i-2)
            used_indices.append(i-1)
            used_indices.append(i)
        elif prev+' '+t in all_ing:
            ingredients.remove(prev)
            ingredients.append(prev+' '+t)
            ingredient_indices.append(i-1)
            ingredient_indices.append(i)
            used_indices.append(i-1)
            used_indices.append(i)
        elif t in all_ing:
            ingredients.append(t)
            ingredient_indices.append(i)
            used_indices.append(i)
        if prev+' '+t in all_actions and prev and i-1 not in used_indices and i not in used_indices:
            actions.append(prev+' '+t)
            action_indices.append(i-1)
            action_indices.append(i)
            used_indices.append(i-1)
            used_indices.append(i)
        elif t in all_actions:
            if i in used_indices:
                poo = 1
            else:
                actions.append(t)
                action_indices.append(i)
                used_indices.append(i)
        if prev+' '+t in COOKWARE and prev and i-1 not in used_indices and i not in used_indices:
            cookware.append(prev+' '+t)
            cookware_indices.append(i-1)
            cookware_indices.append(i)
            used_indices.append(i-1)
            used_indices.append(i)
        if t in COOKWARE and i not in used_indices:
            cookware.append(t)
            cookware_indices.append(i)
            used_indices.append(i)
        if t in TIME and i not in used_indices:
            times.append(prev+' '+t)
            used_indices.append(i-1)
            used_indices.append(i)
            time_indices.append(i-1)
        if prev+' '+t in temp_words and i not in used_indices:
            if t is 'heat':
                temperatures.append(prev+' '+t)
                temperature_indices.append(i-1)
                temperature_indices.append(i)
                used_indices.append(i-1)
                used_indices.append(i)              
            else:
                temperatures.append(prev2+' '+prev+' '+t)
                temperature_indices.append(i-2)
                temperature_indices.append(i-1)
                temperature_indices.append(i)
                used_indices.append(i-2)
                used_indices.append(i-1)
                used_indices.append(i)  
        if t in all_separators and i != len(tokens) and i not in used_indices:
            separators.append(t)
            separator_indices.append(i)
            used_indices.append(i)

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
        else:
            poo = 1

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
        else:
            poo = 1

        if i in ingredient_indices and tokens[i] not in clause_ingredients:
            if i+1 in ingredient_indices:
                if i+2 in ingredient_indices:
                    clause_ingredients.append(tokens[i]+' '+tokens[i+1]+' '+tokens[i+2])
                    i += 3
                    continue
                else:
                    clause_ingredients.append(tokens[i]+' '+tokens[i+1])
                    i += 2
                    continue
            else:
                clause_ingredients.append(tokens[i])
                i += 1
                continue
        else:
            poo = 1

        if t is 'them':
            clause_ingredients = prev_ings
            i += 1
            continue
        else:
            poo = 1

        if i in time_indices:
            clause_time = tokens[i]+' '+tokens[i+1]
            if i+3 in time_indices:
                clause_time += tokens[i+3]+' '+tokens[i+4]
                i += 5
                continue
            i += 2
            continue
        else:
            poo = 1

        if i in temperature_indices:
            clause_temp = tokens[i]+' '+tokens[i+1]
            if i+2 in temperature_indices:
                clause_temp += ' '+tokens[i+2]
                i += 3
                continue
            i += 2
            continue
        else:
            poo = 1
        i += 1

    return step_procedures