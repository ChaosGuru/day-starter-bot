import requests
import json

def get_meal_plan():
    with open("setup.json") as f:
        setup = json.load(f)
        key = setup["api"]["meal"]

    url = "https://api.spoonacular.com/mealplanner/generate"

    params = {
        "apiKey": key,
        "timeFrame": "week"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, params=params, headers=headers)
    print(response)

    if response:
        return response.json()
    else:
        exit()

def translate(title):
    with open("setup.json") as f:
        setup = json.load(f)
        key = setup["api"]["translate"]

    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    data = {
        "source": "en",
        "q": [title, title],
        "target": "uk"
    }

    headers = {
        'x-rapidapi-host': "google-translate1.p.rapidapi.com",
        'x-rapidapi-key': key,
        'accept-encoding': "application/gzip",
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    if response:
        return response.json()["data"]["translations"][0]["translatedText"]
    else:
        exit()

meals = []
for i in range(1):
    meals.append(get_meal_plan())

for weeks in meals:
    for days in weeks["week"]:
        for meal in weeks["week"][days]["meals"]:
            meal["title2"] = translate(meal["title"])

with open("meal_plan.json", "w", encoding="utf8") as f:
    json.dump(meals, f, ensure_ascii=False)