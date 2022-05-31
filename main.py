import json
from collections import Counter

import requests


def get_lists(list_type):
    url = f"""http://www.themealdb.com/api/json/v1/1/list.php?{list_type}=list"""
    x = requests.get(url)
    return json.loads(x.text)


def get_most_recipes_category(json_list):
    categories_dict = {}
    for i in json_list['meals']:
        current_category = i['strCategory']
        url = f"""http://www.themealdb.com/api/json/v1/1/filter.php?c={current_category}"""
        r = requests.get(url)
        current_category_json = json.loads(r.text)
        current_category_entries = len(current_category_json['meals'])
        categories_dict[current_category] = current_category_entries
    print(max(categories_dict, key=categories_dict.get), "has the most recipes per category")


def get_least_used_ingredient_type_area(food_type, area):
    type_recipes = requests.get(f"""http://www.themealdb.com/api/json/v1/1/filter.php?c={food_type}""")
    area_recipes = requests.get(F"http://www.themealdb.com/api/json/v1/1/filter.php?a={area}")
    type_recipes_json = json.loads(type_recipes.text)
    area_recipes_json = json.loads(area_recipes.text)

    type_list = []
    for x in type_recipes_json['meals']:
        type_list.append(x['idMeal'])

    area_list = []
    for x in area_recipes_json['meals']:
        area_list.append(x['idMeal'])

    intersection_recipes = list(set(type_list).intersection(area_list))

    ingredients_list = []
    for x in intersection_recipes:
        current_recipe = requests.get(f"""http://www.themealdb.com/api/json/v1/1/lookup.php?i={x}""")
        current_recipe_json = json.loads(current_recipe.text)
        current_recipe_json_single = current_recipe_json["meals"][0]
        for i in range(1, 21):
            ingredient = current_recipe_json_single['strIngredient' + str(i)]
            if ingredient == '':
                pass
            else:
                ingredients_list.append(current_recipe_json_single['strIngredient'+str(i)])
    counter_dict = dict(Counter(ingredients_list))
    least_counter = min((counter_dict.values()))
    keys = [k for k, v in counter_dict.items() if v == least_counter]
    print(f"""Least used ingredients for {food_type} {area} dishes""",keys)
        #
        #     current_recipe_json_single

        # print(json.dumps(current_recipe_json, indent=4, sort_keys=True))


    # print(json.dumps(json.loads(type_recipes.text), indent=4, sort_keys=True))
    # print(json.dumps(json.loads(area_recipes.text), indent=4, sort_keys=True))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    y = get_lists('c')
    get_most_recipes_category(y)
    get_least_used_ingredient_type_area('Dessert', 'Canadian')

