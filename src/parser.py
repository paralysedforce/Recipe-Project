#!usr/bin/python

from data import *

import scrape
import sys
from collections import namedtuple
from string import punctuation, ascii_lowercase
import re
import nltk
from pymongo import MongoClient
import recipe_classes
import reconstruction
import transform

client = MongoClient()

db = client["k_base"]
ingredients = db["ingredients"]
procedures = db["procedures"]
transformations = db["transformations"]

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
    print ingredients
    ingredient = _strip_punctuation((ingredients.replace('-', ' ')).lower())
    print ingredient

    cursor = db.ingredients.find({"name":ingredient})
    try:
        document = cursor[0]
    except:
        db.ingredients.insert({"name":ingredient, "category":'????', "flags":'none'})
    finally:
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
    cw_cursor = db.cookware.find()
    step = step.lower()
    for document in ing_cursor:
        if isinstance(document['name'], basestring):
            if document['name'] in step:
                step_ingredients.append(document['name'])
    for document in proc_cursor:
        if isinstance(document['name'], basestring):
            print '\n\n\nPASSED TEST: ', step, '\n', document['name'], '\n'
            if document['name'] in step:
                print 'FOUND IN STEP', document['name']
                step_procedures.append(document['name'])
    for document in cw_cursor:
        if isinstance(document['name'], basestring):
            if document['name'] in step:
                step_cookware.append(document['name'])


    #GET TIME AND TEMP FROM STEP
    time = '100 minutes'
    temp = '100F'
    if not step_procedures:
        step_procedures = ['placeholder proc']
    proc = recipe_classes.Procedure(step_procedures[0], step_ingredients, step_cookware, time, temp)
    return proc

# def recognize_time(step):
# def recognize_temp(step):

## Helper
def _strip_punctuation(string):
    return "".join(char for char in string if char not in punctuation)

def main(original_recipe):
    # urls = ['http://allrecipes.com/recipe/easy-meatloaf/',
    #         'http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/',
    #         'http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/',
    #         'http://allrecipes.com/Recipe/Meatball-Nirvana/']
    scraped_info = scrape.scrape(original_recipe.url)
    scraped_ing = scraped_info[0]
    scraped_steps = scraped_info[1]

    # parse ingredient info, create objects
    ingredients = []
    for ingredient in scraped_ing:
        ing_info = ingredient.contents
        new_ing = parse_ingredient(ing_info[0])
        cursor = db.ingredients.find({"name":new_ing.name})
        i = 0
        for document in cursor:
            i += 1
        if i == 0:
            # add to DB
            db.ingredients.insert({"name":new_ing.name})
        ingredients.append(new_ing)

    steps = []
    for step in scraped_steps:
        #SPLIT STEP CONTENTS BEFORE PARSING
        step_info = step.contents
        if not step_info:
            continue # HANDLE EMPTY
        step_sent = nltk.sent_tokenize(step_info[0])
        for sent in step_sent:
            split_step = sent.split(',')
            for clause in split_step:
                clause_step = clause.split(';')
                for s in clause_step:
                    print s
                    new_proc = parse_step(s)
                    steps.append(new_proc)

    original_recipe.in_list = ingredients
    original_recipe.pr_list = steps

    #call transform etc
    reconstruction.reconstruct(original_recipe)
    try:
        transformed_recipe = transform.transform(original_recipe)
    except RuntimeError, e:
        print e
        return original_recipe, Recipe()

    reconstruction.reconstruct(transformed_recipe)
    return original_recipe, transformed_recipe




# if __name__ == "__main__":
#     main()
