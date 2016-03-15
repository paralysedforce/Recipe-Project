#!usr/bin/python

from string import punctuation
import re
from collections import namedtuple
import nltk.corpus

from data import *
import scrape

Quantity = namedtuple('Quantity', ['amount', 'unit'])
Ingredient = namedtuple('Ingredient', ['name', 'quantity', 'descriptors'])

def parse_ingredient(ingredients):
    """ingredients is a string scraped from the web site. This function
    processes the string and returns an ingredient object"""
    number = recognize_number(ingredients)
    unit = recognize_unit(ingredients)
    ingredient_name = recognize_ingredient(ingredients)
    descriptors = recognize_descriptors(ingredients)
    
    quantity = Quantity(number, unit)
    ingredient = Ingredient(ingredient_name, quantity, descriptors)
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
    return 'discrete'

def recognize_ingredient(ingredients):
    # preprocessing
    proc_ingredients = _strip_punctuation(ingredients.lower())
    for ingredient in COMMON_INGREDIENTS:
        if ingredient in proc_ingredients or ingredient in ingredients:
            return ingredient

def recognize_descriptors(ingredients, data = None):
    stopwords = nltk.corpus.stopwords.words('english')
    descriptors = []

    for word in ingredients.split():
        stripped = _strip_punctuation(word).lower()
        no_numerals = all(map(lambda c: c not in '123456789', word))
        no_stopwords = not word.lower() in stopwords 
        no_ingredients = not stripped in COMMON_INGREDIENTS or not word.lower() in COMMON_INGREDIENTS
        no_units = all([stripped not in UNITS[unit] for unit in UNITS])
        if no_numerals and no_stopwords and no_ingredients and no_units:
            descriptors.append(word.lower())
    return descriptors


def recognize_time(step):
    processed_step = _strip_punctuation(step.lower()).split()
    for i in xrange(len(processed_step)):
        word = processed_step[i]
        if word in TIME and i > 0:
            prev_word = processed_step[i-1] 
            if all(map(lambda c: c in '1234567890' or c in punctuation,
                prev_word)):
                return prev_word + ' ' +  word

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

               
def _strip_punctuation(string):
    return "".join(char for char in string if char not in punctuation)


