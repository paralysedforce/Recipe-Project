#!usr/bin/python

from data import UNITS, COMMON_INGREDIENTS

from collections import namedtuple
from string import punctuation, ascii_lowercase
import re
import nltk

Quantity = namedtuple("Quantity", ["value", "unit"])
Ingredient = namedtuple("Ingredient", ['name', 'quantity', 'descriptors'])
Step = namedtuple("Step", ["ingredients", "processes", "cookware"])

#TODO: parse_steps
#TODO: improve recognize_descriptors

def parse_ingredients(ingredients):
    """ingredients is a string scraped from the web site. This function
    processes the string and returns an ingredient object"""
    number = recognize_number(ingredients)
    unit = recognize_unit(ingredients)
    quantity = Quantity(number, unit)

    ingredient_name = recognize_ingredient(ingredients)
    descriptors = recognize_descriptors(ingredients)
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
    return 'unit'



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
        no_ingredients = not (stripped in COMMON_INGREDIENTS or word.lower() in
                COMMON_INGREDIENTS)
        no_units = all([stripped not in UNITS[unit] for unit in UNITS])
        if no_numerals and no_stopwords and no_ingredients and no_units:
            descriptors.append(word.lower())
    return descriptors


## Helper
def _strip_punctuation(string):
    return "".join(char for char in string if char not in punctuation)

def main():
    import scrape
    urls = ['http://allrecipes.com/recipe/easy-meatloaf/',
            'http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/',
            'http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/',
            'http://allrecipes.com/Recipe/Meatball-Nirvana/']
    ingredients, steps =scrape.scrape(urls[3])
    for ingredient in ingredients:
        print parse_ingredients(ingredient)


if __name__ == "__main__":
    main()
