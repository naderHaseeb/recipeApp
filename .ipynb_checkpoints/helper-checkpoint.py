import pandas as pd


def random_meal():
    '''
    This funtion return a random meal
    return is a dataframe
    '''
    df = pd.read_csv('meals_recipes.csv')
    randommeal=df.sample()
    return randommeal

def search_meal(meal_name):

    df= pd.read_csv('Data/meals_recipes.csv')
    result = df[df['name'] == meal_name]
    return result

def search_mealbying(ingredient_name):

    df= pd.read_csv('meals_recipes.csv')
    condition = df['ingredients'].str.contains(ingredient_name,case=False)
    meals= df[condition]
    return meals

def save_meal(title, txt_ingredients, ptime, txt_instructions, difficulty, category, rating):
    df= pd.read_csv('meals_recipes.csv')
    newrow=pd.DataFrame([{'name':title, 
                      'ingredients':txt_ingredients,
                     'prep_time':ptime,
                     'instructions':txt_instructions,
                     'difficulty':difficulty,
                     'category':category,
                     'rating':rating}])
    df=pd.concat([df,newrow])
    df.to_csv('meals_recipes.csv')

def shopping_list(mealnm):
    df = pd.read_csv("meals_recipes.csv")
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
    df = pd.read_csv("meals_recipes.csv")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    meal = df[df["name"] == meal_name]

    if meal.empty:
        return ["Meal not found"]

    ingredients = meal.iloc[0]["ingredients"]

    # Original recipe is assumed to be for 1 person
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
    
    
    