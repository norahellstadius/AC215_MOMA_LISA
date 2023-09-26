import requests
import yaml
from bs4 import BeautifulSoup
from google.cloud import storage


# ------- HELPER FUNCTIONS ----------
def get_page(url):
    result = requests.get(url)
    assert result.status_code == 200, "GET request failed"
    soup = BeautifulSoup(result.content, "html.parser")
    return soup


def get_meta_data(soup):
    def get_name(x):
        return x.find("h2", class_="heading-4").get_text()

    def get_recipe_url(x):
        return "https://www.bbcgoodfood.com" + x.select_one("a").get("href")

    def get_img_url(x):
        return x.find("img", class_="image__img")["src"]

    dish_list = []
    elements = soup.find_all(class_="dynamic-list__list-item")

    for s in elements:
        d = {}
        d["name"] = get_name(s)
        d["url_img"] = get_img_url(s)
        d["url_recipe"] = get_recipe_url(s)
        d["recipe_page"] = get_page(d["url_recipe"])
        dish_list.append(d)

    return dish_list


def get_ingredients(recipe_page):
    # the ingredients part may contains subparts (e.g ingredients for batter)
    ingredient_section = recipe_page.find("section", class_="recipe__ingredients")
    subsections_ingredients = ingredient_section.find_all("section")
    ul_element_in_sections = [
        section.find("ul", class_="list") for section in subsections_ingredients
    ]
    list_items_per_section = [
        section.find_all("li") for section in ul_element_in_sections
    ]

    ingredients = []
    for ingredient_section in list_items_per_section:
        for item in ingredient_section:
            ingredient_text = item.get_text()
            ingredients.append(ingredient_text)

    return ingredients


def get_recipe(recipe_page):
    method_section = recipe_page.find("section", class_="recipe__method-steps")
    ul_element = method_section.find("ul", class_="list")
    list_items = ul_element.find_all("li")
    steps_in_method = []

    for item in list_items:
        method_text = item.get_text()
        steps_in_method.append(method_text)
    return steps_in_method


def fetch_recipe_data(meta_data_recipes):
    data = [
        {
            "name": dish["name"],
            "url_img": dish["url_img"],
            "ingredients": get_ingredients(dish["recipe_page"]),
            "recipe": get_recipe(dish["recipe_page"]),
        }
        for dish in meta_data_recipes
    ]
    return data


# -------- MAIN CODE -----------

# randomly choosen from bbc
URL = "https://www.bbcgoodfood.com/recipes/collection/all-time-top-20-recipes"

soup = get_page(URL)
meta_data_reciepes = get_meta_data(soup)
data_for_dishes = fetch_recipe_data(meta_data_reciepes)

client = storage.Client()
bucket_name = "cook_this_scrape"
bucket = client.bucket(bucket_name)

# ----- upload data to Google buckets -------
for dish in data_for_dishes:
    try:
        response = requests.get(dish["url_img"])
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            object_name_image = "images/" + dish["name"]

            blob_image = bucket.blob(object_name_image)
            blob_image.upload_from_string(response.content)
        else:
            print("failed to download image")

    except Exception as e:
        print(f"An error occured with image upload: {str(e)}")

    try:
        yaml_content = yaml.dump(dish)
        object_name_text = "text/" + dish["name"]
        blob_text = bucket.blob(object_name_text)
        blob_text.upload_from_string(yaml_content)
    except Exception as e:
        print(f"An error occured with text upload: {str(e)}")
