import requests
from bs4 import BeautifulSoup
import time

# ------- HELPER FUNCTIONS ----------
def get_page(url):
    result = requests.get(url)
    assert result.status_code == 200, "GET request failed"
    soup = BeautifulSoup(result.content, 'html.parser')
    return soup

def get_meta_data(soup):
    get_name = lambda x: x.find('h2', class_='heading-4').get_text()
    get_recipe_url = lambda x: 'https://www.bbcgoodfood.com' + x.select_one('a').get('href')
    get_img_url = lambda x: x.find('img', class_='image__img')['src']

    elements = soup.find_all(class_='dynamic-list__list-item')
    dish_list = []

    for s in elements:
        d = {}
        d['name'] = get_name(s)
        d['url_img'] = get_img_url(s)
        d['url_recipe'] = get_recipe_url(s)
        d['recipe_page'] =  get_page(d['url_recipe'])
        dish_list.append(d)
        
    return dish_list

def get_ingredients(recipe_page):
    #the ingredients part may contains subparts (e.g ingredients for batter)
    ingredient_section = recipe_page.find('section', class_='recipe__ingredients')
    subsections_ingredients = ingredient_section.find_all('section') 
    ul_element_in_sections = [section.find('ul', class_='list') for section in subsections_ingredients]
    list_items_per_section = [section.find_all('li') for section in ul_element_in_sections]

    ingredients = []
    for ingredient_section in list_items_per_section:
        for item in ingredient_section:
            ingredient_text = item.get_text()
            ingredients.append(ingredient_text)
    
    return ingredients    

def get_recipe(recipe_page):
    method_section = recipe_page.find('section', class_='recipe__method-steps')
    ul_element = method_section.find('ul', class_='list')
    list_items = ul_element.find_all('li')
    steps_in_method = []
    
    for item in list_items:
        method_text = item.get_text()
        steps_in_method.append(method_text)
    return steps_in_method


def fetch_recipe_data(meta_data_recipes):
    data = [
        {
            'name': dish['name'],
            'url_img': dish['url_img'],
            'ingredients': get_ingredients(dish['recipe_page']),
            'recipe': get_recipe(dish['recipe_page'])
        }
        for dish in meta_data_recipes
    ]
    return data

# -------- MAIN CODE -----------

#randomly choosen from bbc
URL = 'https://www.bbcgoodfood.com/recipes/collection/all-time-top-20-recipes'

soup = get_page(URL)
meta_data_reciepes = get_meta_data(soup)
data_for_dishes = fetch_recipe_data(meta_data_reciepes)
