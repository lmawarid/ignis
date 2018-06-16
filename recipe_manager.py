import json
import MySQLdb
from recipe import Recipe
from secrets import SECRETS

DATABASE_NAME = 'food'
HOST = 'localhost'
USER = SECRETS['database']['username']
PASSWORD = SECRETS['database']['password']
db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE_NAME, charset='utf8')
cursor = db.cursor()

def write_recipe(recipe_json):
    recipe_id = recipe_json['uri'].split('edamam.owl#')[1]
    title = recipe_json['label']
    url = recipe_json['url']
    calories = recipe_json['calories']
    ingredients = recipe_json['ingredients']

    sql = """
    INSERT INTO recipes (recipe_id, title, url, calories, ingredients)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (recipe_id, title, url, calories, json.dumps(ingredients))
    cursor.execute(sql, data)

    return Recipe(recipe_id, title, url, calories, ingredients)

def find_by_recipe_id(uri):
    sql = "SELECT * FROM recipes WHERE recipe_id=%s"
    cursor.execute(sql, (uri,))
    data = cursor.fetchone()
    return __create_recipe_object(data)

def find_by_title(title):
    sql = "SELECT * FROM recipes WHERE title=%s"
    cursor.execute(sql, (title,))
    data = cursor.fetchone()
    return __create_recipe_object(data)

def save():
    db.commit()

def __create_recipe_object(data):
    if not data:
        return data
    return Recipe(data[1], data[2], data[3], data[4], json.loads(data[5]))
