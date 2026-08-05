import pandas as pd

CSV_FILE = "Data/meals_recipes.csv"


def random_meal():
    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    randommeal = df.sample()
    return randommeal


def search_meal(meal_name):
    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    result = df[df["name"] == meal_name]
    return result


def search_mealbying(ingredient_name):
    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    condition = (
        df["ingredients"].str.contains(ingredient_name, case=False, na=False) |
        df["name"].str.contains(ingredient_name, case=False, na=False)
    )
    meals = df[condition]
    return meals


def save_meal(title, txt_ingredients, ptime, txt_instructions, difficulty, category, rating):
    df = pd.read_csv(CSV_FILE)

    newrow = pd.DataFrame([{
        "name": title,
        "ingredients": txt_ingredients,
        "prep_time": ptime,
        "instructions": txt_instructions,
        "difficulty": difficulty,
        "category": category,
        "rating": rating
    }])

    df = pd.concat([df, newrow], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)


def shopping_list(mealnm):
    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    meall = df[df["name"] == mealnm]

    if meall.empty:
        return "Recipe not found"

    lst = meall["ingredients"].iloc[0].split(",")
    return lst


def meal_recommend(df, current_index):
    total_meals = len(df)
    recm = df.iloc[current_index]
    next_index = (current_index + 1) % total_meals
    return recm, next_index


def scale_recipe(meal_name, desired_persons):
    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    meal = df[df["name"] == meal_name]

    if meal.empty:
        return ["Meal not found"]

    ingredients = meal.iloc[0]["ingredients"]
    scale_factor = desired_persons

    inglist = ingredients.split(",")
    scaled_list = []

    for item in inglist:
        itemi = item.strip()

        n = ""
        i = ""

        for char in itemi:
            if char.isdigit() or char == ".":
                n += char
            else:
                i = itemi[len(n):]
                break

        if n != "":
            new_amount = float(n) * scale_factor
            scaled_list.append(f"{new_amount:g}{i}")
        else:
            scaled_list.append(itemi)

    return scaled_list

def search_external_recipes(search_term):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"

    response = requests.get(
        url,
        params={"s": search_term},
        timeout=10
    )

    data = response.json()
    meals = data.get("meals")

    if not meals:
        return pd.DataFrame()

    recipes = []

    for meal in meals:
        ingredients = []

        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            amount = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                amount = amount or ""
                ingredients.append(
                    f"{amount.strip()} {ingredient.strip()}".strip()
                )

        recipes.append({
            "name": meal.get("strMeal"),
            "ingredients": ", ".join(ingredients),
            "instructions": meal.get("strInstructions"),
            "category": meal.get("strCategory"),
            "area": meal.get("strArea"),
            "image": meal.get("strMealThumb")
        })

    return pd.DataFrame(recipes)


def generate_smart_recipe(ingredients, diet, api_key):
    client = genai.Client(api_key=api_key)

    prompt = f"""
    Create one easy recipe using these ingredients:
    {ingredients}

    Diet:
    {diet}

    Include recipe name, preparation time, difficulty,
    ingredients, and instructions.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Error: {error}"
    
    
