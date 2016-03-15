#!usr/bin/python

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

# Quantity = namedtuple("Quantity", ["value", "unit"])
# Ingredient = namedtuple("Ingredient", ['name', 'quantity', 'descriptors'])
# Step = namedtuple("Step", ["ingredients", "processes", "cookware"])

#TODO: unit tests for recipes
#TODO: improve recognize_descriptors

def parse_ingredient(ingredients):
    """ingredients is a string scraped from the web site. This function
    processes the string and returns an ingredient object"""
    number = recognize_number(ingredients)
    unit = recognize_unit(ingredients)
    ingredients = ingredients.replace(unit, '')
    ingredients = ingredients.replace(str(number), '')
    ingredient_name = recognize_ingredient(ingredients)
    # descriptors = recognize_descriptors(ingredients)
    ingredient = recipe_classes.Ingredient(ingredient_name, number, unit)
    return ingredient

def recognize_number(ingredients):
    number_pattern = re.compile("^(\.?\d+)([ \/\.]\d+)?([ \/\.]\d+)?")
    matches = re.findall(number_pattern, ingredients)
    if not matches: return 1
    match = matches[0]
    if match[1] == '':
        return int(match[0])
    elif match[1][0] == '/':
        return float(match[0]) / float(match[1][1:])
    elif match[1][0] == ' ' and match[2][0] == '/':
        return int(match[0]) + (float(match[1][1:]) / float(match[2][1:]))
    else:
        match = ''
    return match

def recognize_unit(ingredients):
    for unit in UNITS:
        variations = UNITS[unit]
        for variation in variations:
            if variation in ingredients:
                return unit
    return 'unit'

def recognize_ingredient(ingredients):
    # preprocessing
    ingredient = _strip_punctuation((ingredients.replace('-', ' ')).lower())
    all_ing_cursor = db.ingredients.find()
    longest_match = ''
    for doc in all_ing_cursor:
        if doc['name'] in ingredient:
            if len(doc['name']) > len(longest_match):
                longest_match = doc['name']
    if longest_match:
        return longest_match
    else:
        return ingredient

def recognize_descriptors(ingredients, data = None):
    stopwords = nltk.corpus.stopwords.words('english')
    descriptors = []
    common_ingredients = db.ingredients.find()

    for word in ingredients.split():
        stripped = _strip_punctuation(word).lower()
        no_numerals = all(map(lambda c: c not in '123456789', word))
        no_stopwords = not word.lower() in stopwords 
        no_ingredients = not (stripped in common_ingredients or word.lower() in
                common_ingredients)
        no_units = all([stripped not in UNITS[unit] for unit in UNITS])
        if no_numerals and no_stopwords and no_ingredients and no_units:
            descriptors.append(word.lower())
    return descriptors

# Step parsing
def parse_step(step):
    step_procedures = []
    step_ingredients = []
    step_cookware = []

    # for direction in DIRECTIONS:
    #     if direction in step:
    #         step_directions.append(direction)
    # for ingredient in ingredients:
    #     if ingredient.name in step:
    #         step_ingredients.append(ingredient.name)
    # for cookware in COOKWARE:
    #     if cookware in step:
    #         step_cookware.append(cookware)
    # return Step(step_ingredients, step_directions, step_cookware)

    ing_cursor = db.ingredients.find()
    proc_cursor = db.procedures.find()
    step = _strip_punctuation(step.lower())
    longest_match = ''
    for document in ing_cursor:
        if isinstance(document['name'], basestring):
            if document['name'] in step:
                step_ingredients.append(document['name'])
    for document in proc_cursor:
        if isinstance(document['name'], basestring):
            if document['name'] in step:
                if len(document['name']) > len(longest_match):
                    longest_match = document['name']
                    step_procedures.append(document['name'])

    cookware_set = set()
    for cookware in COOKWARE:
        for variation in COOKWARE[cookware]:
            if variation in step:
                cookware_set.add(unicode(cookware))
    step_cookware = list(cookware_set)

    #GET TIME AND TEMP FROM STEP
    time = recognize_time(step)
    temp = recognize_temp(step)
    if not step_procedures:
        step_procedures = ['placeholder proc']
    proc = recipe_classes.Procedure(step_procedures[0], step_ingredients, step_cookware, time, temp)
    return proc

def double_action(step):
    i = 0
    proc_step = _strip_punctuation(step.lower()).split()
    ing = []
    proc1 = ''
    proc2 = ''
    flag = ''
    ret = []
    for word in proc_step:
        if word is 'and' or word is 'then':
            if word is 'and':
                flag = 'a'
            elif word is 'then':
                flag = 't'
            proc1 = proc_step[i-1]
            proc2 = proc_step[i+1]
            c1 = db.procedures.find({"name":proc1})
            c2 = db.procedures.find({"name":proc2})
            try:
                c1[0]
                c2[0]
                for ing in proc_step:
                    cursor = db.ingredients.find({"name":ing})
                    try:
                        doc = cursor[0]
                        ings.append(ing)
                    except:
                        pass
            except:
                pass
        i += 1
    if flag is 'a':
        split_step = step.split('and')
        for s in split_step:
            for ing in ings:
                s += ' '.join(ing)
            ret.append(s)
    elif flag is 't':
        split_step = step.split('then')
        for s in split_step:
            for ing in ings:
                s += ' '.join(ing)
            ret.append(s)
    return ret

def recognize_time(step):
    processed_step = _strip_punctuation(step.lower()).split()
    time = ''
    for i in xrange(len(processed_step)):
        word = processed_step[i]
        if word in TIME and i > 0:
            prev_word = processed_step[i-1]
            if all(map(lambda c: c in '1234567890' or c in punctuation, prev_word)):
                time += prev_word + ' ' +  word 
    return time


def recognize_temp(step):
    lower_step = step.lower()
    if 'degrees' in lower_step:
        ind = lower_step.split().index('degrees')
        return " ".join(i for i in step.split()[ind-1: ind+2])
    elif 'low heat' in lower_step:
        return 'low heat'
    elif 'medium heat' in lower_step:
        return 'medium heat'
    elif 'high heat' in lower_step:
        return 'high heat'
    return ''

## Helper
def _strip_punctuation(string):
    return "".join(char for char in string if char not in punctuation)

def contains_procedure(step):
    count = 0
    step = _strip_punctuation(step.lower()).split()
    for w in step:
        cursor = db.procedures.find({"name":w})
        try:
            doc = cursor[0]
            count += 1
        except:
            pass
    return count



def main(original_recipe):
    # urls = ['http://allrecipes.com/recipe/easy-meatloaf/',
    #         'http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/',
    #         'http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/',
    #         'http://allrecipes.com/Recipe/Meatball-Nirvana/']
    if original_recipe.url:
        scraped_ing, scraped_steps = scrape.scrape(original_recipe.url)

        # parse ingredient info, create objects
        ingredients = []
        for ingredient in scraped_ing:
            new_ing = parse_ingredient(ingredient)
            cursor = db.ingredients.find({"name":new_ing.name})
            i = 0
            for document in cursor:
                i += 1
            if i == 0:
                # add to DB
                db.ingredients.insert({"name":new_ing.name, "category":"????", "flag":"none"})
            ingredients.append(new_ing)

        steps = []
        for step in scraped_steps:
            #SPLIT STEP CONTENTS BEFORE PARSING
            if not step:
                continue # HANDLE EMPTY
        # for new_parser
            # parsed_steps = parse_step(step)
            # for p in parsed_steps:
            #     steps.append(p)
        #for new_parser
            step_sent = nltk.sent_tokenize(step)
            for sent in step_sent:
                if contains_procedure(sent) == 1:
                    new_proc = parse_step(sent)
                    steps.append(new_proc)
                elif contains_procedure(sent) > 1:
                    actions = double_action(sent)
                    if actions:
                        for a in actions:
                            new_proc = parse_step(a)
                            steps.append(new_proc)
                        if contains_procedure(sent) == 2:
                            break
                    clause = sent.split(';')
                    for c in clause:
                        if contains_procedure(c) == 1:
                            new_proc = parse_step(c)
                            steps.append(new_proc)
                        elif contains_procedure(c) > 1:
                            more_clause = c.split(',')
                            for more_c in more_clause:
                                if contains_procedure(more_c) == 1:
                                    new_proc = parse_step(more_c)
                                    steps.append(new_proc)
                                elif contains_procedure(more_c) > 1:
                                    actions = double_action(more_c)
                                    if actions:
                                        for a in actions:
                                            new_proc = parse_step(a)
                                            steps.append(new_proc)
                                        if contains_procedure(more_c) == 2:
                                            break
                                    else:
                                        new_proc = parse_step(more_c)
                                        steps.append(new_proc)

        original_recipe.in_list = ingredients
        original_recipe.pr_list = steps

    #call transform etc
    reconstruction.reconstruct(original_recipe)
    r = original_recipe
    try:
        transformed_recipe = transform.transform(r)
    except RuntimeError:
        return [original_recipe, Recipe()]

    #if transformed_recipe == original_recipe:
    #    print "There are no changes to be made"
    #else:
    reconstruction.reconstruct(transformed_recipe)
    return [original_recipe, transformed_recipe]



# if __name__ == "__main__":
#     main()
