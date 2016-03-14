
'''Version 0.32'''
import json
import csv
import glob
import sys
import importlib
from pprint import pprint
from collections import Counter

# init is an optional flag to indicate you're starting
# over; old autograder results are written over and column
# headers are printed to the file.
team = "7"
init = False
for arg in sys.argv:
    if arg == "init":
        init = True
#    else:
#        team = arg

api = importlib.import_module("Team%s.recipe_api" % team)


def check_tools(answer, stud):
    score = 0
    expans = dict([[a, a.split()] for a in answer])

    for s in stud:
        if s in answer:
            print s
            score += 1
            answer.remove(s)
            stud.remove(s)

    expans = dict([[a, {'words': a.split(), 'matches': Counter()}] for a in answer])
    expstud = dict([[a, a.split()] for a in stud])

    for s in expstud:
        tmpscore = -1
        for word in expans:
            complement = set(expstud[s]) ^ set(expans[word]['words'])
            intersection = set(expstud[s]) & set(expans[word]['words'])
            newscore = float(len(intersection))/(len(intersection)+len(complement))
            print "%s, %s, %d, %d, %f" % (s, word, len(intersection), len(complement), newscore)
            if newscore > tmpscore:
                tmpscore = newscore
                tmpmatch = word
        if tmpscore > 0:
            expans[tmpmatch]['matches'][s] = tmpscore
            stud.remove(s)

    for word in expans:
        match = expans[word]['matches'].most_common(1)
        if len(match) > 0:
            score += expans[word]['matches'].most_common(1)[0][1]

    return score


def check_ingredients(answer, stud):
    scores = []
    score = 0

    for x in range(min([len(answer), len(stud)])):
        for ind in ['name', 'measurement', 'quantity', 'descriptor', 'preparation', 'prep-description']:
            if ind in stud[x]:
                print "\nYour answer: %s"%str(stud[x][ind])
                print "Valid answers: %s"%str(answer[x][ind])

                if ind == 'quantity':
                    flag = False
                    for val in answer[x][ind]:
                        if type(stud[x][ind]) is str:
                            if val == stud[x][ind]:
                                flag = True
                        elif val == stud[x][ind]:
                            flag = True
                        elif float('%.2f'%stud[x][ind]) == val:
                            flag = True
                        if flag:
                            score += 1
                        else:
                            print "Match!"
                
                elif stud[x][ind] in answer[x][ind]:
                    score += 1

        scores.append(min([score, answer[x]['max']]))
        print "Score: %s\n---"%str(scores[-1])
        score = 0

    return sum(scores)


def get_file(fn):
    with open(fn, 'r') as f:
        answer = json.load(f)
    return answer


def main(team, init=False):
    """Pass 'init' as a command line variable if this is your
    first time running the program and you want it to print the
    column headers to the file."""

    keys = ['ingredients', 'primary cooking method', 'cooking methods', 'cooking tools']

    if init:
        with open('parsegrades.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\t')
            csvwriter.writerow(keys)

    scores = Counter(dict(zip(keys, [0]*len(keys))))

    cnt = 1

    for answer in (get_file(fn) for fn in glob.iglob('Recipes/*.json')):
        stud = getattr(api, "autograder")(answer['url'])
        temp = Counter(dict(zip(keys, [0]*len(keys))))

        if type(stud) == str:
            stud = json.loads(stud)
        if type(stud) == dict:
            temp['cooking tools'] = min([check_tools(answer['cooking tools'], stud['cooking tools']), answer['max']['cooking tools']])/float(answer['max']['cooking tools'])
            temp['cooking methods'] = min([check_tools(answer['cooking methods'], stud['cooking methods']), answer['max']['cooking methods']])/float(answer['max']['cooking methods'])
            if stud['primary cooking method'] == answer['primary cooking method']:
                temp['primary cooking method'] = 1
            stud = stud['ingredients']
            temp['ingredients'] = check_ingredients(answer['ingredients'], stud)/float(answer['max']['ingredients'])
            scores += temp
            print "%s\t%s\t%s\t%s\t%s" % ("Recipe", 'Ingredients', 'Primary Method', 'Methods', 'Tools')
            print "Recipe %d:\t%.3f\t%d\t%.3f\t%.3f" % (cnt, temp['ingredients'], temp['primary cooking method'], temp['cooking methods'], temp['cooking tools'])
            cnt += 1
        else:
            print "student answer formatting error"

    row = ["Team %s" % team]
    row.extend([scores[k] for k in keys])

    with open('parsegrades.csv', 'ab') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        csvwriter.writerow(row)

if __name__ == '__main__':
    main(team, init)
