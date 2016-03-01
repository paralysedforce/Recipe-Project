#!usr/bin/python

from collections import namedtuple, Counter
from string import digits, punctuation
import re
import nltk

Quantity = namedtuple("Quantity", ["value", "unit"])
Ingredient = namedtuple("Ingredient", ['name', 'quantity', 'descriptors'])
Step = namedtuple("Step", ["ingredients", "processes", "cookware"])

def parse_ingredients(ingredients):
    """ingredients is a string scraped from the web site. This function
    processes the string and returns an ingredient object"""
