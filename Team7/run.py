import recipe_classes
import recipe_db
from pymongo import MongoClient

client = MongoClient()
client.drop_database('k_base')
try:
	execfile('recipe_db.py')
except:
	poo = 1
r = recipe_classes.Recipe('http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/', 'mushroom chicken', 'vegetarian')
execfile('parser.py')
main(r)