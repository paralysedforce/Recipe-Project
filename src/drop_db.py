from pymongo import MongoClient

client = MongoClient()
client.drop_database('k_base')