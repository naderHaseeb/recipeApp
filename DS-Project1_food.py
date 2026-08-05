import streamlit as st
import pandas as pd
from helper import random_meal
from helper import search_meal
from helper import search_mealbying
from helper import save_meal
from helper import shopping_list
from helper import meal_recommend
from helper import scale_recipe
from helper import search_external_recipes
from helper import generate_smart_recipe


CSV_FILE = "Data/meals_recipes.csv"

st.title("CookBook")
st.write("Be Your Best Chef")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #fbfaf4;
        color: #353327;
    }

    section[data-testid="stSidebar"] {
        background-color: #eeeee5;
        border-right: 1px solid #d7d4c8;
    }

    h1, h2, h3 {
        color: #363426;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: #f0eee6;
        color: #333126;
        border: 1px solid #d4d0c4;
        border-radius: 12px;
    }

    .stButton > button {
        background-color: #e8e4d9;
        color: #363426;
        border: 1px solid #d2cec1;
        border-radius: 12px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #dcd7c9;
        color: #252319;
    }
    </style>
    """,
    unsafe_allow_html=True
)

add_radio = st.radio(
    "Choose Your Service",
    (
        "Create New Recipe",
        "Search",
        "Import Recipe from API",
        "Smart Chef",
        "View All recipe",
        "View a random recipe",
        "Meal Recommendation",
        "Shopping List"
    )
)

if add_radio == "Create New Recipe":
    st.subheader(" Add your New Recipe")

    form = st.form("my_form")
    title = form.text_input("Dish Name", "")
    txt_ingredients = form.text_area("Ingredients needed for your dish")
    ptime = form.number_input("Preparation time needed (in minutes)", min_value=0, step=1)
    txt_instructions = form.text_area("How to prepare your dish")

    difficulty = form.selectbox(
        "How difficult is it to prepare the dish?",
        ("Easy", "Medium", "Hard")
    )

    category = form.selectbox(
        "When is this meal prepared for?",
        ("Breakfast", "Lunch", "Dinner", "Dessert")
    )

    rating = form.slider("Rate your dish", 1, 5)

    submitted = form.form_submit_button("Add Recipe")

    if submitted:
        df = pd.read_csv("meals_recipes.csv")
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        if title.strip() == "" or txt_ingredients.strip() == "" or ptime==0 or txt_instructions.strip()=="":
            st.error('Please complete the form', icon="🚨")
        elif title.strip().lower() in df["name"].str.lower().values:
            st.error('Recipe already exist', icon="🚨")
        else:
            save_meal(
                title,
                txt_ingredients,
                ptime,
                txt_instructions,
                difficulty,
                category,
                rating )
            st.success("Recipe added successfully!")
            st.write("### Your added recipe:")
            st.write("**Dish Name:**", title)
            st.write("**Ingredients:**", txt_ingredients)
            st.write("**Preparation Time:**", ptime, "minutes")
            st.write("**Instructions:**", txt_instructions)
            st.write("**Difficulty:**", difficulty)
            st.write("**Category:**", category)
            st.write("**Rating:**", rating)

elif add_radio == "Search":
    st.subheader(" Search Recipes")
    tosearch = st.text_input("Search for the recipe or ingredient:")

    if st.button("Search"):
        if tosearch:
            result = search_mealbying(tosearch)

            if result.empty:
                st.warning("No recipes found.")
            else:
                st.dataframe(result)
        else:
            st.warning("Please enter a recipe name or ingredient.")

elif add_radio == "View All recipe":
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    st.subheader(" View All Recipes")

    add_selectbox = st.selectbox(
        "What meal are you planning to prepare?",
        ("Breakfast", "Lunch", "Dinner", "Dessert")
    )

    filtered_df = df[df["category"] == add_selectbox]
    st.dataframe(filtered_df)

elif add_radio == "Import Recipe from API":
    st.subheader("Import Recipe from TheMealDB")

    search_term = st.text_input(
        "Enter a meal name, for example: Arrabiata, Chicken, or Pasta"
    )

    if st.button("Search Online"):
        if search_term.strip():
            api_recipes = search_external_recipes(search_term)

            if api_recipes.empty:
                st.warning("No online recipes found.")
            else:
                st.session_state["api_recipes"] = api_recipes

        else:
            st.warning("Please enter a meal name.")

    if "api_recipes" in st.session_state:
        api_recipes = st.session_state["api_recipes"]

        for index, recipe in api_recipes.iterrows():
            st.write("---")
            st.subheader(recipe["name"])

            if pd.notna(recipe["image"]):
                st.image(recipe["image"], width=300)

            st.write("**Category:**", recipe["category"])
            st.write("**Cuisine:**", recipe["area"])
            st.write("**Ingredients:**", recipe["ingredients"])
            st.write("**Instructions:**", recipe["instructions"])

            if st.button(
                f"Save {recipe['name']}",
                key=f"save_api_{index}"
            ):
                save_meal(
                    recipe["name"],
                    recipe["ingredients"],
                    30,
                    recipe["instructions"],
                    "Medium",
                    recipe["category"],
                    3
                )

                st.success("Recipe saved to your CSV file.")

elif add_radio == "View a random recipe":
    st.subheader(" Random Recipe")

    if st.button("give me a random meal"):
        st.dataframe(random_meal())
        st.balloons()

elif add_radio == "Meal Recommendation":
    st.subheader("Meal Recommendation")

    if "key" not in st.session_state:
        st.session_state["key"] = 0

    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    if st.button("Recommend me a meal"):
        recommended_meal, next_index = meal_recommend(df, st.session_state["key"])

        if recommended_meal is not None:
            st.session_state["key"] = next_index
            st.write(recommended_meal)
        else:
            st.error("No meals found in the dataset.")

elif add_radio == "Shopping List":
    st.subheader("Know What You Need")

    df = pd.read_csv(CSV_FILE)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    meal_names = df["name"].tolist()

    selected_meal = st.selectbox("Choose a recipe:", meal_names)

    desired_persons = st.number_input(
        "How many persons/servings do you want?",
        min_value=1,
        value=2
    )

    if st.button("Create List"):
        scaled_ingredients = scale_recipe(selected_meal, desired_persons)

        st.write("List for your recipe:")

        for ingredient in scaled_ingredients:
            st.write("- " + ingredient)

elif add_radio == "Smart Chef":
    st.subheader("Smart Chef")

    ingredients = st.text_area("Enter your ingredients")

    diet = st.selectbox(
        "Choose diet",
        ("None", "Vegetarian", "Vegan")
    )

    if st.button("Generate Recipe"):

        if ingredients == "":
            st.warning("Enter some ingredients")

        else:
            api_key = st.secrets["GEMINI_API_KEY"]

            recipe = generate_smart_recipe(
                ingredients,
                diet,
                api_key
            )

            st.write(recipe)


def search_external_recipes(search_term):
    """Search for recipes using TheMealDB."""

    url = "https://www.themealdb.com/api/json/v1/1/search.php"

    try:
        response = requests.get(
            url,
            params={"s": search_term},
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        meals = data.get("meals")

        if meals is None:
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

            recipe = {
                "name": meal.get("strMeal"),
                "ingredients": ", ".join(ingredients),
                "instructions": meal.get("strInstructions"),
                "category": meal.get("strCategory"),
                "area": meal.get("strArea"),
                "image": meal.get("strMealThumb")
            }

            recipes.append(recipe)

        return pd.DataFrame(recipes)

    except requests.exceptions.RequestException:
        return pd.DataFrame()


def generate_smart_recipe(ingredients, diet, api_key):
    """Generate a recipe using Gemini."""

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Create one easy recipe using these ingredients:

    {ingredients}

    Diet preference:
    {diet}

    Include:
    Recipe name
    Preparation time
    Difficulty
    Ingredients
    Instructions
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Error: {error}"
