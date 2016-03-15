'''Version 0.1'''
import scrape
import parser2
from data import *

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    ingredient_strings, step_strings = scrape.scrape(url)
# The ingredient template is 
#   name, quantity, measurement, descriptor, preparation, pre-preparation
    fin_ingredients = []
    for ingredient in ingredient_strings:
        name = unicode(parser.recognize_ingredient(ingredient))
        number = parser.recognize_number(ingredient)
        unit = parser.recognize_unit(ingredient)
        descriptors = [unicode(i) for i in
                parser.recognize_descriptors(ingredient)]
        fin_ingredients.append({"name": name, "quantity": number, "measurement":
            [unicode(unit)], "descriptor": descriptors})

    primary_method = None
    methods = set()
    for method in COOKING_METHODS.keys()[::-1]:
        for variation in COOKING_METHODS[method]:
            for step in step_strings:
                if variation in step:
                    methods.add(unicode(method))
                    primary_method = unicode(method)

    cookware_set = set()
    for cookware in COOKWARE:
        for variation in COOKWARE[cookware]:
            for step in step_strings:
                if variation in step:
                    cookware_set.add(unicode(cookware))

    return {"ingredients": list(fin_ingredients), "cooking methods": list(methods),
            "primary cooking method": primary_method, "cooking tools":
            list(cookware_set)}

def main():
    print autograder('http://allrecipes.com/recipe/8714/baked-lemon-chicken-with-mushroom-sauce/')

if __name__ == "__main__":
    main()
