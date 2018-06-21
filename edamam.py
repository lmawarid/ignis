from secrets import secrets
import http.client
import urllib.parse
import json
import recipe_manager
from textblob import TextBlob, Word
import nltk
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
    lemmatized_words = list(map(lambda w: Word(w).lemmatize(), blob.words))
    ingredients = []

    # This is not super efficient... maybe there'll be a better way to do this later on
    for n in range(ingredient_dict.MAX_LEN, 0, -1):
        lemmatized_words, new_ingredients = __filter_ngrams(lemmatized_words, n)
        ingredients.extend(new_ingredients)

    return ', '.join(ingredients)

def __filter_ngrams(word_list, n):
    ngrams = list(nltk.ngrams(word_list, n))
    num_ngrams = len(word_list) - n + 1
    idx = word_idx = 0

    ingredients = []
    new_word_list = word_list
    while idx < num_ngrams:
        phrase = ' '.join(ngrams[idx])
        if ingredient_dict.find(phrase):
            ingredients.append(phrase)
            new_word_list = new_word_list[:word_idx] + new_word_list[word_idx+n:]
            idx += n
        else:
            idx += 1
            word_idx += 1

    return new_word_list, ingredients
