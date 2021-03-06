#!usr/bin/python

from collections import namedtuple
import requests
from bs4 import BeautifulSoup

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ingredient_strings = [i.text for i in soup("span", {
        "class": "recipe-ingred_txt", "itemprop": "ingredients"
        }) if i.text]
    step_strings = [i.text for i in soup('span', class_ =
        "recipe-directions__list--item") if i.text]

    return [ingredient_strings, step_strings]

    # for ingredient in ingredient_strings:
    # 	cursor = db.ingredients.find({"name":ingredient})
    # 	i = 0
    # 	for document in cursor:
    # 		i += 1
    # 	if i == 0:
    # 		# add to DB
    # 		db.ingredients.insert({"name":ingredient})

    # return step_strings
