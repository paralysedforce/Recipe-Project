import sys
from pymongo import MongoClient
'''Inserting going to be manual --> adding everything from the knowledge base'''

client = MongoClient()

db = client["k_base"]
ingredients = db["ingredients"]
procedures = db["procedures"]
transformations = db["transformations"]
cookware = db["cookware"]

kb_item = {}
main = True

ans = raw_input('\nAutomation? [y/n]')
if ans[0].lower() == 'y':
	sys.stdin = open('./input.txt')

while (main):
	item_type = raw_input('\nEnter item type: ')

	if item_type[0].lower() == 'i':
		# get ingredient name, category, and dietary flags
		name = raw_input('\nEnter ingredient name (type exit to leave): ')	
		if (name.upper() == 'EXIT'):
			break	
		cursor = db.ingredients.find({"name":name})
		try:
			if cursor[0] != None:
				print 'Item already in database -- Replacing with new one'
				db.ingredients.remove(cursor[0])
		except Exception, e:
			print str(e)
		category = raw_input('\nEnter ingredient category: ')
		flags = []
		flag_cont = True
		while (flag_cont):
			flag = raw_input('\nEnter ingredient dietary flag (only one - will prompt for more): ')
			flags.append(flag)
			cont = raw_input('\nMore flags? [y/n] ')
			if (cont.upper() == 'N'):
				flag_cont = False
		# insert item in ingredient collection
		kb_item = {'name':name,'category':category,'flags':flags}
		db.ingredients.insert(kb_item)

	elif item_type[0].lower() == 'p':
		# get procedure name, category
		name = raw_input('\nEnter procedure name (type exit to leave): ')	
		if (name.upper() == 'EXIT'):
			break	
		cursor = db.procedures.find({"name":name})
		try:
			if cursor[0] != None:
				print 'Item already in database -- Replacing with new one'
				db.procedures.remove(cursor[0])
		except Exception, e:
			print str(e)
		category = raw_input('\nEnter procedure category: ')
		kb_item = {'name':name,'category':category}
		# insert item in procedure collection
		db.procedures.insert(kb_item)

	elif item_type[0].lower() == 't':
		# get transformation name, type, actions
		name = raw_input('\nEnter transformation name (type exit to leave): ')	
		if (name.upper() == 'EXIT'):
			break	
		cursor = db.transformations.find({"name":name})
		try:
			if cursor[0] != None:
				print 'Item already in database -- Replacing with new one'
				db.transformations.remove(cursor[0])
		except Exception, e:
			print str(e)
		category = raw_input('\nEnter transformation type: ')
		actions = []
		act_cont = True
		while (act_cont):
			action = raw_input('\nEnter transformation action (only one - will prompt for more): ')
			actions.append(action)
			cont = raw_input('\nMore actions? [y/n] ')
			if (cont.upper() == 'N'):
				act_cont = False
		#insert item in transformation collection
		kb_item = {'name':name,'category':category,'actions':actions}
		db.transformations.insert(kb_item)
	else:
		print 'Invalid item type'

	cont = raw_input('\nMore items? [y/n] ')
	if (cont.upper() == 'N'):
		main = False


ingredients = db.ingredients.find()
procedures = db.procedures.find()
transformations = db.transformations.find()

print '\n\n---------------------------------\n\n'

print 'INGREDIENTS:\n'
for record in ingredients:
	print(record['name'] + ',',record['category'] + ',',record['flags'])

print '\nPROCEDURES:\n'
for record in procedures:
	print(record['name'] + ',',record['category'])

print '\nTRANSFORMATIONS:\n'
for record in transformations:
	print(record['name'] + ',',record['category'] + ',',record['actions'])

cont = raw_input('\nAny modifications to be made? [y/n] \n')
if (cont.upper() == 'N'):
	cont = False
else:
	cont = True

while(cont):
	item_type = raw_input('\nItem type to modify: ')

	if item_type[0].lower() == 'i':
		name = raw_input('\ningredient name to modify (exit to leave): ')
		if (name.upper() == 'EXIT'):
			break
		cursor = db.ingredients.find({"name":name})
		document = cursor[0]
		print document
		doc_id = document['_id']
		name = document['name']
		category = document['category']
		flags = document['flags']
		mod = True
		while(mod):
			field = raw_input('\nWhich field would you like to modify? ')
			if field.lower() == 'name':
				name = raw_input('\nNew ingredient name: ')
			elif field.lower() == 'category':
				category = raw_input('\nNew ingredient category: ')
			elif field.lower() == 'flags':
				print 'This will replace all flags - add one by one'
				flags = []
				flag_cont = True
				while (flag_cont):
					flag = raw_input('\nNew ingredient dietary flag: ')
					flags.append(flag)
					cont = raw_input('\nMore flags? [y/n] ')
					if (cont.upper() == 'N'):
						flag_cont = False
			else:
				print 'Invalid field name'

			mod = raw_input('\nAny other field to modify? [y/n] ')
			if mod.lower() == 'n':
				mod = False
		db.ingredients.update_one({"_id":doc_id},
		                          {"$set":
		                          	{
		                          	"name":name,
		                          	"category":category,
		                          	"flags":flags
		                          	}})
		print db.ingredients.find({"_id":doc_id})[0]

	if item_type[0].lower() == 'p':
		name = raw_input('\nProcedure name to modify (exit to leave): ')
		if (name.upper() == 'EXIT'):
			break
		cursor = db.procedures.find({"name":name})
		document = cursor[0]
		print document
		doc_id = document['_id']
		name = document['name']
		category = document['category']
		mod = True
		while(mod):
			field = raw_input('\nWhich field would you like to modify? ')
			if field.lower() == 'name':
				name = raw_input('\nNew procedure name: ')
			elif field.lower() == 'category':
				category = raw_input('\nNew procedure category: ')
			else:
				print 'Invalid field name'

			mod = raw_input('\nAny other field to modify? [y/n] ')
			if mod.lower() == 'n':
				mod = False
		db.ingredients.update_one({"_id":doc_id},
		                          {"$set":
		                          	{
		                          	"name":name,
		                          	"category":category
		                          	}})
		print db.ingredients.find({"_id":doc_id})[0]

	if item_type[0].lower() == 't':
		name = raw_input('\ntransformation name to modify (exit to leave): ')
		if (name.upper() == 'EXIT'):
			break
		cursor = db.transformations.find({"name":name})
		document = cursor[0]
		print document
		doc_id = document['_id']
		name = document['name']
		category = document['category']
		actions = document['actions']
		mod = True
		while(mod):
			field = raw_input('\nWhich field would you like to modify? ')
			if field.lower() == 'name':
				name = raw_input('\nNew transformation name: ')
			elif field.lower() == 'category':
				category = raw_input('\nNew transformation type: ')
			elif field.lower() == 'actions':
				print 'This will replace all actions - add one by one'
				actions = []
				act_cont = True
				while (act_cont):
					action = raw_input('\nNew transformation action: ')
					actions.append(action)
					cont = raw_input('\nMore actions? [y/n] ')
					if (cont.upper() == 'N'):
						act_cont = False
			else:
				print 'Invalid field name'

			mod = raw_input('\nAny other field to modify? [y/n] ')
			if mod.lower() == 'n':
				mod = False
		db.ingredients.update_one({"_id":doc_id},
		                          {"$set":
		                          	{
		                          	"name":name,
		                          	"category":category,
		                          	"actions":actions
		                          	}})
		print db.ingredients.find({"_id":doc_id})[0]

	cont = raw_input('\nModify another item? [y/n] \n')
	if cont.lower() == 'n':
		cont = False
		ingredients = db.ingredients.find()
		procedures = db.procedures.find()
		transformations = db.transformations.find()

		print '\n\n---------------------------------\n\n'

		print 'INGREDIENTS:\n'
		for record in ingredients:
			print(record['name'] + ',',record['category'] + ',',record['flags'])

		print '\nPROCEDURES:\n'
		for record in procedures:
			print(record['name'] + ',',record['category'])

		print '\nTRANSFORMATIONS:\n'
		for record in transformations:
			print(record['name'] + ',',record['category'] + ',',record['actions'])

# close the connection to MongoDB
client.close()






