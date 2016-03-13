import recipe_classes

r = recipe_classes.Recipe('http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/', 'mushroom chicken', 'vegetarian')
execfile('parser.py')
main(r)