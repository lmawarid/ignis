from secrets import secrets
import http.client
import urllib.parse
import json
import recipe_manager
from textblob import TextBlob, Word
import ingredient_dict

APP_ID = secrets['edamam']['app_id']
APP_KEY = secrets['edamam']['app_key']
API_BASE = 'api.edamam.com'

def recipes_for(message):
    query_string = __extract_ingredients(message)
    found_new_recipe, recipes = __search(query_string)

    text = ["You asked for recipes that might contain %s. I found some for you:" % (query_string)]
    for recipe in recipes:
        text.append(u"\u2022 %s (%s)" % (recipe.title, recipe.url))
    return found_new_recipe, '\n'.join(text)

def __search(keywords):
    conn = http.client.HTTPSConnection(API_BASE)
    params = { 'q' : keywords, 'app_id' : APP_ID, 'app_key' : APP_KEY }
    url = "/search?%s" % (urllib.parse.urlencode(params))
    conn.request('GET', url)
    response = conn.getresponse()

    data = json.loads(response.read().decode())
    recipes = []
    found_new_recipe = False
    for hit in data['hits']:
        recipe = hit['recipe']
        uri = recipe['uri'].split('edamam.owl#')[1]
        recipe_object = recipe_manager.find_by_recipe_id(uri)
        if not recipe_object:
            found_new_recipe = True
            recipe_object = recipe_manager.write_recipe(recipe)
        recipes.append(recipe_object)

    recipe_manager.save()
    return found_new_recipe, recipes

def __extract_ingredients(message):
    blob = TextBlob(message)
    tagged_nouns = filter(lambda tag: 'NN' in tag[1], blob.tags)
    nouns = map(lambda tag: Word(tag[0]).lemmatize(), tagged_nouns)
    ingredients = list(filter(lambda noun: ingredient_dict.find(noun), nouns))

    return ', '.join(ingredients)
