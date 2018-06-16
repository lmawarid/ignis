from secrets import SECRETS
import http.client
import urllib.parse
import json
import recipe_manager

APP_ID = SECRETS['edamam']['app_id']
APP_KEY = SECRETS['edamam']['app_key']
API_BASE = 'api.edamam.com'

def recipes_for(keywords):
    recipes = search(keywords)
    text = ['We found the following recipes for you:']
    for recipe in recipes:
        text.append("- %s (%s)" % (recipe.title, recipe.url))
    return '\n'.join(text)

def search(keywords):
    conn = http.client.HTTPSConnection(API_BASE)
    params = { 'q' : keywords, 'app_id' : APP_ID, 'app_key' : APP_KEY }
    url = "/search?%s" % (urllib.parse.urlencode(params))
    conn.request('GET', url)
    response = conn.getresponse()

    data = json.loads(response.read().decode())
    recipes = []
    for hit in data['hits']:
        recipe = hit['recipe']
        uri = recipe['uri'].split('edamam.owl#')[1]
        recipe_object = recipe_manager.find_by_recipe_id(uri)
        if not recipe_object:
            recipe_object = recipe_manager.write_recipe(recipe)
        recipes.append(recipe_object)

    recipe_manager.save()
    return recipes
