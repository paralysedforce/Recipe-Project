from pymongo import MongoClient
import recipe_classes
import sys

# i is indicator for which transformation to do
# fucntion for performing tranformations will be found in knowledge base
# not sure how to access knowledge base yet
# look into changing portions (easy, and gives extra credit)

client = MongoClient()

db = client["k_base"]

def transform(r):
    i = r.transformation
    if i.lower() == 'pescatarian':
        ret = pescatarianize(r)
    elif i.lower() == 'vegetarian':
        ret = vegatarianize(r)
    elif i.lower() == 'east asian':
        ret = eastasianize(r)
    elif i.lower() == 'italian':
        ret = italianize(r)
    elif i.lower() == 'easy':
        ret = easyize(r)
    elif i.lower() == 'low sodium':
        ret = lowsodiumize(r)
    elif i.lower() == 'low carb':
        ret = lowcarbize(r)
    else:
        raise RuntimeError('Error! Wrong transformation name')
    return ret

def replace_ing_in_proc(proc_list, old, new):
    new_proc_list = []
    print "\n\n\nREPLACING ING " + old.name + "WITH " + new
    for proc in proc_list:
        if old.name in proc.in_list:
            proc.in_list.remove(old.name)
            proc.in_list.append(new)
        new_proc_list.append(proc)
    return new_proc_list

def vegatarianize(r):
    i = 0
    for ing in r.in_list:
        if is_meat(ing):
            if is_protein(ing):
                r.in_list[i] = replace_ing(ing, 'tofu')
                r.pr_list = replace_ing_in_proc(r.pr_list, ing, 'tofu')
            elif is_sauce(ing):
                r.in_list[i] = replace_ing(ing, 'vegetable broth')              
                r.pr_list = replace_ing_in_proc(r.pr_list, ing, 'vegetable broth')
        i+=1
    return r

def pescatarianize(r):
    i = 0
    for ing in r.in_list:
        if is_protein(ing):
            if not is_fish(ing):
                print "HULLABALLO", ing.name
                r.in_list[i] = replace_ing(ing, 'cod')
                r.pr_list = replace_ing_in_proc(r.pr_list, ing, 'cod')
        elif is_sauce(ing) and is_meat(ing):
            r.in_list[i] = replace_ing(ing, 'vegetable broth')
            r.pr_list = replace_ing_in_proc(r.pr_list, ing, 'vegetable broth')
        i+=1
    return r

# want to replace spices
# startch should be rice or noodles
def eastasianize(r):
    i = 0
    j = 0
    k = 0
    asian_spices = ['ginger','cilantro','sweet basil','red pepper']
    asian_sauces = ['soy sauce', 'sesame oil', 'fish sauce', 'rice wine']
    for ing in r.in_list:
        if is_spice(ing):
            if not is_east_asian(ing):
                if j>=len(asian_spices):
                    del r.in_list[i]
                    i-=1
                else:
                    r.in_list[i] = replace_ing(ing, asian_spices[j])
                    r.pr_list = replace_ing_in_proc(r.pr_list, ing, asian_spices[j])
                j+=1    
        if is_sauce(ing):
            if not is_east_asian(ing):
                if k>=len(asian_sauces):
                    del r.in_list[i]
                    i-=1
                else:
                    r.in_list[i] = replace_ing(ing, asian_sauces[k])
                    r.pr_list = replace_ing_in_proc(r.pr_list, ing, asian_spices[k])
                k+=1
        i+=1
    return r

def italianize(r):
    i = 0
    j = 0
    k = 0
    italian_spices = ['oregano','basil','thyme','parsley','black pepper']
    italian_sauces = ['alfredo sauce']
    for ing in r.in_list:
        if is_spice(ing):
            if not is_italian(ing):
                if j>=len(italian_spices):
                    del r.in_list[i]
                    i-=1
                else:
                    r.in_list[i] = replace_ing(ing, italian_spices[j])
                    r.pr_list = replace_ing_in_proc(r.pr_list, ing, italian_spices[j])
                    j+=1
        if is_sauce(ing):
            if k>=len(italian_sauces):
                del r.in_list[i]
                i-=1
            else:
                r.in_list[k] = replace_ing(ing, italian_spices[k])
                r.pr_list = replace_ing_in_proc(r.pr_list, ing, italian_spices[k])
                k+=1
        i+=1
    return r

def lowsodiumize(r):
    i = 0
    for ing in r.in_list:
        if is_salty(ing):
            r.in_list[i].amount /= 2
        i+=1
    print r
    return r

def lowcarbize(r):
    i = 0
    j = 0
    for ing in r.in_list:
        if is_starch(ing):
            if j==0:
                r.in_list[i] = replace_ing(ing, 'quinoa')
                r.pr_list = replace_ing_in_proc(r.pr_list, ing, 'quinoa')
                j+=1
            else:
                del r.in_list[i]
                i-=1
        i+=1
    return r

#############
## helpers ##
#############


def replace_ing(old, new_name):
    return recipe_classes.Ingredient(new_name, old.amount, old.amount_unit)

def is_cooking_method(p):
    cursor = db.procedures.find({'name':p.name})
    try:
        document = cursor[0]        
        if document['category'] == 'cooking method':
            return True
    except IndexError:
        return False
    return False

def replace_proc(p, new_name):
    new_temp = ''
    if p.temp == 'low':
        new_temp = '350F'
    elif p.temp == 'med':
        new_temp = '375F'
    elif p.temp == 'high':
        new_temp = '400F'
    else:
        new_temp = '375F'

    new_time = 0
    if p.name == 'slow cook':
        new_time = p.time/12
    else:
        new_time = p.time*2

    new_cookware = '9"x13" baking pan'  
    
    return recipe_classes.Procedure(new_name, p.in_list, new_cookware, new_time, new_temp)

def is_starch(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        if 'starch' in document['category']:
            return True
    except IndexError:
        return False
    return False

def is_east_asian(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        flags = document['flags']
        if 'east asian' in flags:
            return True
    except IndexError:
        return False
    
    return False

def is_salty(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        flags = document['flags']
        if 'salty' in flags:
            return True
    except IndexError:
        return False    
    return False

def is_italian(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        flags = document['flags']
        if 'italian' in flags:
            return True
    except IndexError:
        return False    
    return False

def is_fish(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        if 'fish' in document['category']:
            return True
    except IndexError:
        return False
    return False

def is_meat(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        flags = document['flags']
        if 'meat' in flags:
            return True
    except:
        return False
    return False

def is_protein(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]        
        if 'protein' in document['category']:
            return True
    except IndexError:
        return False
    return False

def is_spice(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        if 'spice' in document['category']:
            return True
    except IndexError:
        return False
    return False
    
def is_sauce(i):
    cursor = db.ingredients.find({'name':i.name})
    try:
        document = cursor[0]
        if 'sauce' in document['category']:
            return True
    except IndexError:
        return False    
    return False
