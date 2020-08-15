# https://picantecooking.com/ua/recipes/kashi-zlaki-ta-bobovi/?PAGEN_1=2

import requests
from bs4 import BeautifulSoup
import random

def get_meal(uri):
    base = "https://picantecooking.com"
    test = requests.get(uri)

    # test if meals are on multiple pages
    if "?PAGEN_1=" in test.text:
        page = str(random.randint(1,5))
    else:
        page = "1"

    # get final random page
    res = requests.get(uri + "?PAGEN_1=" + page)

    # parse it
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all(class_="recipes-item")

    # get random meal and its description
    item = random.choice(items).find_all('a')
    item_a = list(filter(lambda x: x.string != None, item))[0]

    return str(item_a.string), base + str(item_a.get('href'))

if __name__ == "__main__":
    # res = get_meal("https://picantecooking.com/ua/recipes/kashi-zlaki-ta-bobovi/")
    link, title = get_meal("https://picantecooking.com/ua/recipes/nalisniki/")
    print(link, title)